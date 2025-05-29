import os
import sqlite3
from datetime import datetime, timedelta

import pandas as pd
from flask import render_template, request, url_for
from flask import Blueprint, jsonify, current_app
from app.dashboard_functions import insert_filters

bp = Blueprint('dashboard_routes', __name__)

@bp.route("/")
def index():
    return render_template("landing.html")

@bp.route("/custom", methods=["GET", "POST"])
def custom():
    default_query = "SELECT * FROM report_fact"
    query = default_query
    error = None

    if request.method == "POST":
        action = request.form.get("action")

        if action == "submit":
            user_query = request.form["sql_query"]
            if user_query.strip().lower().startswith("select"):
                query = user_query
            else:
                error = "Only SELECT statements are allowed."
        elif action == "reset":
            query = default_query  # reset to default

    try:
        conn = sqlite3.connect(current_app.config["DB_PATH"])
        df = pd.read_sql_query(query, conn)
        conn.close()

        if "report_path" in df.columns:
            df["report"] = df["report_path"].apply(
                lambda x: f'<a href="{url_for("static", filename=f"reports/{x}")}" target="_blank">View</a>' if pd.notnull(x) else "N/A"
            )
            df.drop("report_path", axis=1, inplace=True)

        table_html = df.to_html(classes="data-table", index=False, escape=False)
    except Exception as e:
        table_html = ""
        error = str(e)

    return render_template("custom.html", table=table_html, error=error)

@bp.route("/report_upload", methods=["GET", "POST"])
def report_upload_page():
    return render_template('report_upload.html')

@bp.route("/assist", methods=["GET", "POST"])
def dumb():
    base_query = "SELECT * FROM report_fact"
    editable_query = None
    time_interval = None
    start_date = None
    end_date = None
    repeated_defect = None
    zone = None
    error = None
    filters = []
    params = {}
    search_date = None

    if request.method == "POST":
        custom_query = request.form.get("custom_query")
        editable_query = request.form.get("editable_query")
        time_interval = request.form.get("time_interval")
        start_date = request.form.get("start_date", "")
        end_date = request.form.get("end_date", "")
        repeated_defect = request.form.get("repeated_defect")
        zone = request.form.get("zone")

    if editable_query:
        base_query = editable_query.strip()

    # Prepare filters as before
    filter_clauses = []

    if time_interval:
        today = datetime.today()
        if time_interval == "last_7_days":
            search_date = today - timedelta(days=7)
        elif time_interval == "last_30_days":
            search_date = today - timedelta(days=30)
        elif time_interval == "this_month":
            search_date = datetime(today.year, today.month, 1)
        elif time_interval == "custom" and start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y%m%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime('%Y%m%d')
            params["start_date"] = start_date
            params["end_date"] = end_date
            filter_clauses.append("date_id BETWEEN :start_date AND :end_date")
        if search_date:
            params["search_date"] = search_date.strftime('%Y%m%d')
            filter_clauses.append("date_id >= :search_date")

    if repeated_defect in ["0", "1"]:
        params["repeated_defect"] = int(repeated_defect)
        filter_clauses.append("repeated_defect = :repeated_defect")

    if zone:
        params["zone"] = zone
        filter_clauses.append("location_id in (SELECT location_id FROM location_dim WHERE zone LIKE '%' || :zone || '%')")
        

    # Combine filters into SQL string
    filters_sql = " AND ".join(filter_clauses)

    # Use the safe insertion function
    if filters_sql:
        query = insert_filters(base_query, filters_sql)
    else:
        query = base_query

    try:
        conn = sqlite3.connect(current_app.config["DB_PATH"])
        conn.row_factory = sqlite3.Row
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        table_html = df.to_html(classes="data-table", index=False)
    except Exception as e:
        table_html = ""
        error = str(e)

    return render_template("assist.html", table=table_html, error=error)
