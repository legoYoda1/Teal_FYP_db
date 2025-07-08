import os
import sqlite3
from datetime import datetime, timedelta
from flask import render_template, request, url_for
from flask import Blueprint, jsonify, current_app, session
from app.dashboard_functions import insert_filters, get_chart_suggestions, convert_ndarrays, get_query_suggestions
import json
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from urllib.parse import unquote

bp = Blueprint('dashboard_routes', __name__)

@bp.route("/")
def index():
    return render_template("landing.html")

@bp.route("/generate_query", methods=["POST"])
def generate_query():
    try:
        prompt = request.json.get("prompt")
        query = get_query_suggestions(prompt)

        return jsonify({"success": True, "query": query})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
    
@bp.route("/generate_charts", methods=["POST"])
def generate_charts():
    try:
        query = request.json.get("sql_query", "SELECT * FROM report_fact")
        conn = sqlite3.connect(current_app.config["DB_PATH"])
        df = pd.read_sql_query(query, conn)
        conn.close()

        suggestion = get_chart_suggestions(df, query)

        # Parse JSON from model
        parsed = json.loads(suggestion)

        # Dynamically evaluate the code safely
        local_vars = {"df": df, "px": px, "go": go}
        exec(parsed["code"], {}, local_vars)
        fig = local_vars.get("fig")
        fig_dict = convert_ndarrays(fig.to_dict())

        return jsonify({"success": True, "title": parsed["title"], "chart": fig_dict})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@bp.route("/report_upload", methods=["GET", "POST"])
def report_upload_page():
    return render_template('report_upload.html')

# ==== CUSTOM DASHBOARD ROUTES ====

@bp.route("/custom", methods=["GET", "POST"])
def custom():
    error = None
    query = session.get("user_query", "SELECT * FROM report_fact")

    if request.method == "POST":
        action = request.form.get("action")
        if action == "submit":
            user_query = request.form["sql_query"].strip()
            if user_query.lower().startswith("select"):
                session["user_query"] = user_query
                query = user_query
            else:
                error = "Only SELECT statements are allowed."
        elif action == "reset":
            session["user_query"] = "SELECT * FROM report_fact"
            query = session["user_query"]

    return render_template("custom.html", query=query, error=error)

@bp.route("/api/custom_query_data", methods=["POST"])
def custom_query_data():
    try:
        draw = int(request.form.get("draw", 1))
        start = int(request.form.get("start", 0))
        length = int(request.form.get("length", 10))
        base_query = session.get("user_query")

        if not base_query or not base_query.strip().lower().startswith("select"):
            return jsonify({
                "draw": draw,
                "recordsTotal": 0,
                "recordsFiltered": 0,
                "data": [],
                "columns": [],
                "error": "No valid SELECT query in session"
            })

        conn = sqlite3.connect(current_app.config["DB_PATH"])
        conn.row_factory = sqlite3.Row

        # Count total records
        count_query = f"SELECT COUNT(*) FROM ({base_query}) as sub"
        total_records = conn.execute(count_query).fetchone()[0]

        # Get current page
        paginated_query = f"""
            SELECT * FROM ({base_query}) as sub
            LIMIT ? OFFSET ?
        """
        df = pd.read_sql_query(paginated_query, conn, params=(length, start))

        conn.close()

        if "report_path" in df.columns:
            df["report"] = df["report_path"].apply(
                lambda x: f'<a href="static/reports/{x}" target="_blank" style="padding:5px 10px; background-color:#1b64ef; color:white; border:none; border-radius:5px; text-decoration:none; font-weight:bold;">View</a>' if pd.notnull(x) else "N/A"
            )
            df.drop("report_path", axis=1, inplace=True)
        column_names = df.columns.tolist()

        return jsonify({
            "draw": draw,
            "recordsTotal": total_records,
            "recordsFiltered": total_records,
            "data": df.to_dict(orient="records"),
            "columns": column_names
        })

    except Exception as e:
        return jsonify({
            "draw": 1,
            "recordsTotal": 0,
            "recordsFiltered": 0,
            "data": [],
            "columns": [],
            "error": str(e)
        })
    
# ==== ASSIST DASHBOARD ROUTES ====    

@bp.route("/assist", methods=["GET", "POST"])
def assist():
    error = None

    if request.method == "POST":
        raw_query = request.form.get("editable_query", "SELECT * FROM report_fact")
        editable_query = unquote(raw_query) if raw_query else "SELECT * FROM report_fact"
        session["assist_query"] = editable_query

        session["assist_time_interval"] = request.form.get("time_interval")
        session["assist_start_date"] = request.form.get("start_date")
        session["assist_end_date"] = request.form.get("end_date")
        session["assist_repeated_defect"] = request.form.get("repeated_defect")
        session["assist_zone"] = request.form.get("zone")

    return render_template("assist.html", error=error)

@bp.route("/api/assist_query_data", methods=["POST"])
def assist_query_data():
    try:
        draw = int(request.form.get("draw", 1))
        start = int(request.form.get("start", 0))
        length = int(request.form.get("length", 10))

        editable_query = session.get("assist_query", "SELECT * FROM report_fact").strip().rstrip(";")
        time_interval = session.get("assist_time_interval")
        start_date = session.get("assist_start_date")
        end_date = session.get("assist_end_date")
        repeated_defect = session.get("assist_repeated_defect")
        zone = session.get("assist_zone")

        params = {}
        filter_clauses = []
        today = datetime.today()

        if time_interval:
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
            if 'search_date' in locals():
                params["search_date"] = search_date.strftime('%Y%m%d')
                filter_clauses.append("date_id >= :search_date")

        if repeated_defect in ["0", "1"]:
            params["repeated_defect"] = int(repeated_defect)
            filter_clauses.append("repeated_defect = :repeated_defect")

        if zone:
            params["zone"] = zone
            filter_clauses.append("location_id IN (SELECT location_id FROM location_dim WHERE zone LIKE '%' || :zone || '%')")

        filters_sql = " AND ".join(filter_clauses)
        query = insert_filters(editable_query, filters_sql) if filters_sql else editable_query

        conn = sqlite3.connect(current_app.config["DB_PATH"])
        conn.row_factory = sqlite3.Row

        count_query = f"SELECT COUNT(*) FROM ({query}) AS sub"
        total_records = conn.execute(count_query, params).fetchone()[0]

        paginated_query = f"SELECT * FROM ({query}) AS sub LIMIT :limit OFFSET :offset"
        df = pd.read_sql_query(paginated_query, conn, params={**params, "limit": length, "offset": start})
        conn.close()

        if "report_path" in df.columns:
            df["report"] = df["report_path"].apply(
                lambda x: f'<a href="static/reports/{x}" target="_blank" style="padding:5px 10px; background-color:#1b64ef; color:white; border:none; border-radius:5px; text-decoration:none; font-weight:bold;">View</a>' if pd.notnull(x) else "N/A"
            )
            df.drop("report_path", axis=1, inplace=True)

        return jsonify({
            "draw": draw,
            "recordsTotal": total_records,
            "recordsFiltered": total_records,
            "data": df.to_dict(orient="records"),
            "columns": df.columns.tolist()
        })

    except Exception as e:
        return jsonify({
            "draw": 1,
            "recordsTotal": 0,
            "recordsFiltered": 0,
            "data": [],
            "columns": [],
            "error": str(e)
        })


@bp.route("/api/saved_queries", methods=["GET"])
def get_saved_queries():
    conn = sqlite3.connect(current_app.config["QUERY_DB_PATH"])
    conn.row_factory = sqlite3.Row
    queries = conn.execute("SELECT * FROM saved_queries").fetchall()
    conn.close()
    return jsonify([dict(q) for q in queries])

@bp.route("/api/saved_queries", methods=["POST"])
def save_query():
    data = request.json
    label = data.get("label")
    sql_query = data.get("sql_query")
    chart_code = data.get("chart_code", "")

    conn = sqlite3.connect(current_app.config["QUERY_DB_PATH"])
    conn.execute("INSERT INTO saved_queries (label, sql_query, chart_code) VALUES (?, ?, ?)",
                 (label, sql_query, chart_code))
    conn.commit()
    conn.close()

    return jsonify({"success": True})

@bp.route("/api/saved_queries/<int:id>", methods=["PATCH"])
def update_query(id):
    data = request.json
    label = data.get("label")
    sql_query = data.get("sql_query")
    chart_code = data.get("chart_code", "")

    conn = sqlite3.connect(current_app.config["QUERY_DB_PATH"])
    conn.execute("UPDATE saved_queries SET label = ?, sql_query = ?, chart_code = ? WHERE id = ?",
                 (label, sql_query, chart_code, id))
    conn.commit()
    conn.close()

    return jsonify({"success": True})

@bp.route("/api/saved_queries/<int:id>", methods=["DELETE"])
def delete_query(id):
    conn = sqlite3.connect(current_app.config["QUERY_DB_PATH"])
    conn.execute("DELETE FROM saved_queries WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True})