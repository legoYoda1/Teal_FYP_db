import json
import os
import threading
import time
import tkinter as tk
from tkinter import filedialog

from flask import Blueprint, Flask, Response, current_app, jsonify, request

from app import socketio

bp = Blueprint('report_uploads_routes', __name__)

selected_folder = None
dialog_done = False
etl_done = False
batch_upload_status = {
    'batch_no': 0,
    'total_batches': 0
}

def open_file_dialog():
    global selected_folder, dialog_done

    dialog_done = False
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    root.lift()
    root.focus_force()

    folder_path = filedialog.askdirectory(
        title="Select Folder Containing PDF Files"
    )

    selected_folder = folder_path
    dialog_done = True  
    root.destroy()
    
    socketio.emit('dialog_close', {'folder': selected_folder})
    
@bp.route('/open_dialog', methods=['POST'])
def open_dialog():
    thread = threading.Thread(target=open_file_dialog)
    thread.start()
    return jsonify({"status": "dialog opened"})

###############################################################
from etl.test import etl


def batch_upload_reports(batch_size=1):
    etl(selected_folder, batch_size, socketio)

# this api polls every interval until tkinter dialog is closed
@bp.route('/start_etl', methods=['POST'])
def start_etl():
    
    if selected_folder == '':
        return jsonify({"message": "No folder selected"}), 200
    
    data = request.get_json()  # Parse JSON body
    batch_size = data.get('batch_size')  # Get the number field
    
    print("ETL STARTED")

    threading.Thread(target=batch_upload_reports, args=(batch_size,)).start()
    return jsonify({"message": "ETl started"}), 200