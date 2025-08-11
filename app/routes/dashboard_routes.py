import json
import pandas as pd
from datetime import datetime, timedelta
from urllib.parse import unquote
from flask import render_template, request, Blueprint, jsonify, current_app, session
from sqlalchemy import text
from app.dashboard_functions import insert_filters, get_query_suggestions, get_cache_key_from_query, get_dropbox_token
from random import randint
from cachetools import LRUCache
import dropbox

# Initialize a cache for query results (resets on flask app restart)
query_cache = LRUCache(maxsize=1000)

bp = Blueprint('dashboard_routes', __name__)

# ==== LANDING PAGE ROUTES ====

@bp.route("/")
def index():
    return render_template("landing.html")

@bp.route("/api/overview_stats")
def overview_stats():
    cache = current_app.overview_stats_cache

    # Use a static key since this endpoint has a single payload
    if "stats" in cache:
        return jsonify(cache["stats"])

    engine = current_app.db_engine
    stats = {}

    with engine.connect() as conn:
        total_defects_row = conn.execute(text("SELECT COUNT(*) AS count FROM report_fact")).mappings().fetchone()
        stats["total_defects"] = total_defects_row["count"] if total_defects_row else 0

        most_common_row = conn.execute(text("""
            SELECT cause_of_defect, COUNT(*) as count
            FROM report_fact
            GROUP BY cause_of_defect
            ORDER BY count DESC
            LIMIT 1
        """)).mappings().fetchone()
        stats["most_common_defect"] = most_common_row["cause_of_defect"] if most_common_row else "N/A"

       # hotspot_row = conn.execute(text("""
        #    SELECT l.zone, COUNT(*) as count
         #   FROM report_fact r
          #  JOIN location_dim l ON r.location_key = l.location_id
           # GROUP BY l.zone
            #ORDER BY count DESC
            #LIMIT 1
        #""")).mappings().fetchone()
        #stats["hotspot"] = hotspot_row if hotspot_row else {}

    # Cache the result for future requests
    cache["stats"] = stats

    return jsonify(stats)

# ==== CUSTOM DASHBOARD ROUTES ====

@bp.route("/custom", methods=["GET", "POST"])
def custom():
    error = None
    query = session.get("user_query", "SELECT * FROM report_fact").strip().rstrip(';')

    if request.method == "POST":
        action = request.form.get("action")
        if action == "submit":
            user_query = request.form["sql_query"].strip().rstrip(';')
            user_query = unquote(user_query)
            if user_query.lower().startswith("select"):
                session["user_query"] = user_query
                query = user_query
            else:
                error = "Only SELECT statements are allowed."
        elif action == "reset":
            session["user_query"] = "SELECT * FROM report_fact"
            query = session["user_query"]

    return render_template("custom.html", query=query, error=error)
        
@bp.route("/api/get_viewer_link", methods=["POST"])
def get_viewer_link():
    data = request.get_json()
    file_path = data.get("file_path")
    if not file_path.startswith('/'):
        file_path = '/' + file_path

    print(f"Requesting link for: {file_path}...")

    try:
        dropbox_access_token = get_dropbox_token()
        dbx = dropbox.Dropbox(dropbox_access_token)
        shared_link_metadata = dbx.sharing_create_shared_link_with_settings(path=file_path)
        return jsonify({"url": shared_link_metadata.url})

    except dropbox.exceptions.ApiError as e:
        if e.error.is_shared_link_already_exists():
            print("  -> Link already exists. Fetching existing link...")
            links = dbx.sharing_list_shared_links(path=file_path).links
            if links:
                return jsonify({"url": links[0].url})
            else:
                error_msg = f"Could not fetch existing link for {file_path}"
                return jsonify({"error": error_msg}), 404
        else:
            error_msg = f"Unexpected Dropbox API error: {e}"
            print("  ->", error_msg)
            return jsonify({"error": error_msg}), 500

@bp.route("/api/custom_query_data", methods=["POST"])
def custom_query_data():
    try:
        draw = int(request.form.get("draw", 1))
        start = int(request.form.get("start", 0))
        length = int(request.form.get("length", 10))
        base_query = session.get("user_query", "SELECT * FROM report_fact").strip().rstrip(';')

        if not base_query or not base_query.strip().lower().startswith("select"):
            return jsonify({
                "draw": draw, "recordsTotal": 0, "recordsFiltered": 0,
                "data": [], "columns": [], "error": "No valid SELECT query in session"
            })

        cache_key = get_cache_key_from_query(base_query)
        page_key = f"{cache_key}:{start}:{length}"
        if page_key in query_cache:
            return jsonify(query_cache[page_key])

        engine = current_app.db_engine
        with engine.connect() as conn:
            count_query = f"SELECT COUNT(*) FROM ({base_query}) as sub"
            total_records = conn.execute(text(count_query)).scalar()

            paginated_query = f"SELECT * FROM ({base_query}) as sub LIMIT :limit OFFSET :offset"
            df = pd.read_sql_query(text(paginated_query), conn, params={"limit": length, "offset": start})

        if "url_path" in df.columns:
            df["report"] = df["url_path"].apply(
                lambda x: f'<button onclick="requestViewerLink(\'{x}\')" style="padding:5px 10px; background-color:#1b64ef; color:white; border:none; border-radius:5px; font-weight:bold;">View</button>' if pd.notnull(x) else "N/A"
            )
            df.drop("url_path", axis=1, inplace=True)

        response = {
            "draw": draw, "recordsTotal": total_records, "recordsFiltered": total_records,
            "data": df.to_dict(orient="records"), "columns": df.columns.tolist()
        }

        query_cache[page_key] = response
        return jsonify(response)

    except Exception as e:
        return jsonify({
            "draw": 1, "recordsTotal": 0, "recordsFiltered": 0,
            "data": [], "columns": [], "error": str(e)
        })

def random_rgba():
    return f'rgba({randint(0,255)}, {randint(0,255)}, {randint(0,255)}, 0.6)'

@bp.route("/api/generate_chartjs_data", methods=["POST"])
def generate_chartjs_data():
    try:
        chart_type = request.json.get("chart_type")
        x_axis = request.json.get("x_axis")
        agg_func = request.json.get("agg_func", "count")
        agg_col = request.json.get("agg_col")
        mixed_1 = request.json.get("mixed_type_1")
        mixed_2 = request.json.get("mixed_type_2")

        query = session.get("user_query", "SELECT * FROM report_fact")
        engine = current_app.db_engine
        with engine.connect() as conn:
            df = pd.read_sql_query(text(query), conn)

        if x_axis not in df.columns:
            return jsonify({"success": False, "error": f"Invalid x-axis column: {x_axis}."})

        if agg_func == "count":
            grouped = df.groupby(x_axis).size().reset_index(name="value")
        elif agg_func == "sum":
            if not agg_col or agg_col not in df.columns:
                return jsonify({"success": False, "error": f"Invalid sum column: {agg_col}."})
            grouped = df.groupby(x_axis)[agg_col].sum().reset_index(name="value")
        else:
            return jsonify({"success": False, "error": f"Unsupported aggregation: {agg_func}"})

        labels = grouped[x_axis].astype(str).tolist()
        values = grouped["value"].tolist()
        colors = [random_rgba() for _ in values]

        if chart_type == "mixed":
            config = {
                "type": "bar",  # base type
                "data": {
                    "labels": labels,
                    "datasets": [
                        {
                            "type": mixed_1,
                            "label": f"{mixed_1.upper()} - {agg_func}",
                            "data": values,
                            "backgroundColor": colors,
                            "borderColor": colors,
                            "borderWidth": 2
                        },
                        {
                            "type": mixed_2,
                            "label": f"{mixed_2.upper()} - {agg_func}",
                            "data": values,
                            "backgroundColor": "transparent",
                            "borderColor": "rgba(255, 99, 132, 1)",
                            "borderWidth": 2,
                            "fill": False
                        }
                    ]
                },
                "options": {
                    "responsive": True,
                    "scales": { "y": { "beginAtZero": True } }
                }
            }
        else:
            config = {
                "type": chart_type,
                "data": {
                    "labels": labels,
                    "datasets": [{
                        "label": f"{agg_func.upper()} by {x_axis}",
                        "data": values,
                        "backgroundColor": colors,
                        "borderColor": colors,
                        "borderWidth": 1
                    }]
                },
                "options": {
                    "responsive": True,
                    "scales": { "y": { "beginAtZero": True } } if chart_type in ["bar", "line"] else {}
                }
            }

        return jsonify(config)

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@bp.route("/api/generate_query", methods=["POST"])
def generate_query():
    try:
        prompt = request.json.get("prompt")
        query = get_query_suggestions(prompt)
        return jsonify({"success": True, "query": query})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
    

@bp.route("/api/saved_queries", methods=["GET"])
def get_saved_queries():
    engine = current_app.query_db_engine
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM saved_queries"))
        queries = [dict(row._mapping) for row in result]
    return jsonify(queries)


@bp.route("/api/saved_queries", methods=["POST"])
def save_query():
    data = request.json
    label = data.get("label")
    sql_query = data.get("sql_query")

    engine = current_app.query_db_engine
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO saved_queries (label, sql_query)
                VALUES (:label, :sql_query)
            """),
            {"label": label, "sql_query": sql_query}
        )

        # Cache the result
        try:
            warehouse_engine = current_app.db_engine
            with warehouse_engine.connect() as warehouse_conn:
                result = warehouse_conn.execute(text(sql_query)).fetchall()
                rows = [dict(row._mapping) for row in result]
                current_app.saved_query_button_cache[label] = rows
        except Exception as e:
            print(f"Failed to cache saved query '{label}': {e}")


    return jsonify({"success": True})


@bp.route("/api/saved_queries/<int:id>", methods=["PATCH"])
def update_query(id):
    data = request.json
    label = data.get("label")
    sql_query = data.get("sql_query")

    engine = current_app.query_db_engine
    with engine.begin() as conn:
        conn.execute(
            text("""
                UPDATE saved_queries
                SET label = :label, sql_query = :sql_query
                WHERE id = :id
            """),
            {"label": label, "sql_query": sql_query, "id": id}
        )

        # Invalidate + re-cache
        current_app.saved_query_button_cache.pop(label, None)
        try:
            warehouse_engine = current_app.db_engine
            with warehouse_engine.connect() as warehouse_conn:
                result = warehouse_conn.execute(text(sql_query)).fetchall()
                rows = [dict(row._mapping) for row in result]
                current_app.saved_query_button_cache[label] = rows
        except Exception as e:
            print(f"Failed to re-cache saved query '{label}': {e}")


    return jsonify({"success": True})


@bp.route("/api/saved_queries/<int:id>", methods=["DELETE"])
def delete_query(id):
    engine = current_app.query_db_engine
    with engine.begin() as conn:
        # Get label before deletion
        result = conn.execute(text("SELECT label FROM saved_queries WHERE id = :id"), {"id": id}).first()
        if result:
            label = result._mapping["label"]
            current_app.saved_query_button_cache.pop(label, None)

        conn.execute(text("DELETE FROM saved_queries WHERE id = :id"), {"id": id})
    return jsonify({"success": True})



# ==== ASSIST DASHBOARD ROUTES ====

@bp.route("/assist", methods=["GET", "POST"])
def assist():
    error = None
    if request.method == "POST":
        session["assist_query"] = "SELECT * FROM report_fact"
        session["assist_time_interval"] = request.form.get("time_interval")
        session["assist_start_date"] = request.form.get("start_date")
        session["assist_end_date"] = request.form.get("end_date")
        session["assist_repeated_defect"] = request.form.get("repeated_defect")
        session["assist_zone"] = request.form.get("zone")
    return render_template("assist.html", error=error)

@bp.route("/api/assist_query_data", methods=["POST"])
def assist_query_data():
    filters = {
        "time_interval": request.form.get("time_interval"),
        "start_date": request.form.get("start_date"),
        "end_date": request.form.get("end_date"),
        "repeated_defect": request.form.get("repeated_defect"),
        "zone": request.form.get("zone"),
    }

    where_clauses = []
    params = {}

    # Time filter
    if filters["time_interval"] == "last_7_days":
        db_format_date = (datetime.today() - timedelta(days=7)).strftime("%Y%m%d")
        where_clauses.append("date_key >= :start_date")
        params["start_date"] = int(db_format_date)  # Convert to integer
    elif filters["time_interval"] == "last_30_days":
        db_format_date = (datetime.today() - timedelta(days=30)).strftime("%Y%m%d")
        where_clauses.append("date_key >= :start_date")
        params["start_date"] = int(db_format_date)  # Convert to integer
    elif filters["time_interval"] == "this_month":
        today = datetime.today()
        db_format_date = datetime(today.year, today.month, 1).strftime("%Y-%m-%d")
        where_clauses.append("date_key >= :start_date")
        params["start_date"] = int(db_format_date)  # Convert to integer
    elif filters["time_interval"] == "custom" and filters["start_date"] and filters["end_date"]:
        start_int = int(filters["start_date"].replace("-", ""))
        end_int = int(filters["end_date"].replace("-", ""))
        where_clauses.append("date_key BETWEEN :start_date AND :end_date")
        params["start_date"] = start_int
        params["end_date"] = end_int

    if filters["repeated_defect"] in ("0", "1"):
        where_clauses.append("is_repeated = :repeated_defect")
        params["repeated_defect"] = filters["repeated_defect"]

    if filters["zone"]:
        where_clauses.append("zone = :zone")
        params["zone"] = filters["zone"]

    where_clause = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""

    pie_sql = f"""
        SELECT i.inspector_name, r.inspector_key, COUNT(r.report_fact_id) AS count
        FROM report_fact as r JOIN inspector_dim as i
        ON r.inspector_key = i.inspector_id
        {where_clause}
        GROUP BY r.inspector_key, i.inspector_name
    """

    bar_sql = f"""
        SELECT cause_of_defect, COUNT(report_fact_id) AS count
        FROM report_fact
        {where_clause}
        GROUP BY cause_of_defect
    """

    timeseries_sql = f"""
        SELECT date_key, cause_of_defect, COUNT(report_fact_id) AS count
        FROM report_fact
        {where_clause}
        GROUP BY date_key, cause_of_defect
        ORDER BY date_key
    """

    totaldefects_sql = f"""
        SELECT COUNT(report_fact_id) AS total_defects
        FROM report_fact
        {where_clause}
    """

    commondefects_sql = f"""
        SELECT cause_of_defect, COUNT(report_fact_id) AS count
        FROM report_fact
        {where_clause}
        GROUP BY cause_of_defect
        ORDER BY count DESC
        LIMIT 1
    """

    engine = current_app.db_engine
    with engine.connect() as conn:
        pie_data = [dict(row._mapping) for row in conn.execute(text(pie_sql), params).fetchall()]
        bar_data = [dict(row._mapping) for row in conn.execute(text(bar_sql), params).fetchall()]
        timeseries_data = [dict(row._mapping) for row in conn.execute(text(timeseries_sql), params).fetchall()]
        total_defects = conn.execute(text(totaldefects_sql), params).scalar()
        most_common_defect = conn.execute(text(commondefects_sql), params).scalar()


    return jsonify({
        "pie_data": pie_data,
        "bar_data": bar_data,
        "timeseries_data": timeseries_data,
        "total_defects": total_defects,
        "most_common_defect": most_common_defect if most_common_defect else "N/A"
    })