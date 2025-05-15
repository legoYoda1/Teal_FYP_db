from flask import Flask, render_template, request
import sqlite3
import pandas as pd
from datetime import datetime, timedelta

app = Flask(__name__, template_folder="templates", static_folder="static")
DB_PATH = "data/test.db"

@app.route("/", methods=["GET", "POST"])
def index():
    query = "SELECT * FROM report_fact"
    error = None
    if request.method == "POST":
        user_query = request.form["sql_query"]
        if user_query.strip().lower().startswith("select"):
            query = user_query
        else:
            error = "Only SELECT statements are allowed."

    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(query, conn)
        conn.close()
        table_html = df.to_html(classes="data-table", index=False)
    except Exception as e:
        table_html = ""
        error = str(e)

    return render_template("index.html", table=table_html, error=error)

@app.route("/dumb", methods=["GET", "POST"])
def dumb():
    query = "SELECT * FROM report_fact"
    error = None
    filters = []
    params = {}
    search_date = None

    if request.method == "POST":
        time_interval = request.form.get("time_interval")
        start_date = request.form.get("start_date", "")
        end_date = request.form.get("end_date", "")
        repeated_defect = request.form.get("repeated_defect")

        if time_interval:
            today = datetime.today()
            if time_interval == "last_7_days":
                search_date = today - timedelta(days=7)
            elif time_interval == "last_30_days":
                search_date = today - timedelta(days=30)
            elif time_interval == "this_year":
                search_date = datetime(today.year, 1, 1)
            elif time_interval == "custom" and start_date and end_date:
                filters.append("date_id BETWEEN :start_date AND :end_date")
                # Convert string dates to datetime objects and remove time part
                start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y%m%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime('%Y%m%d')
                params["start_date"] = start_date
                params["end_date"] = end_date
            else:
                search_date = None

            if search_date:
                filters.append("date_id >= :search_date")
                params["search_date"] = search_date.strftime('%Y-%m-%d')

        if repeated_defect in ["0", "1"]:
            filters.append("repeated_defect = :repeated_defect")
            params["repeated_defect"] = int(repeated_defect)

        if filters:
            query += " WHERE " + " AND ".join(filters)

    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        table_html = df.to_html(classes="data-table", index=False)
    except Exception as e:
        table_html = ""
        error = str(e)

    return render_template("dumb.html", table=table_html, error=error)

if __name__ == "__main__":
    app.run(debug=True)
