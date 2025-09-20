# run_gui.py — reliable launcher, logs, waits for Flask, then opens & maximizes webview window
import threading
import time
import webview
import requests
import sys
import os
import logging
from app import app

# --- resource helper for PyInstaller compatibility ---
def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)

# --- logging setup ---
log_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "run_gui.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler(log_file, encoding="utf-8")]
)

def excepthook(exc_type, exc, tb):
    logging.exception("Uncaught exception:", exc_info=(exc_type, exc, tb))
sys.excepthook = excepthook

logging.info("Heart Disease Predictor launcher starting...")

# --- server waiting config ---
HOST = "127.0.0.1"
PORT = 5000
URL = f"http://{HOST}:{PORT}/"
POLL_INTERVAL = 0.25
POLL_TIMEOUT = 60.0  # allow longer model load times

def run_flask():
    try:
        # IMPORTANT: disable reloader so we don't spawn a second Python process
        app.run(host=HOST, port=PORT, debug=False, threaded=True, use_reloader=False)
    except Exception:
        logging.exception("Flask failed to start.")

def wait_for_server(url, timeout=POLL_TIMEOUT, interval=POLL_INTERVAL):
    start = time.time()
    while True:
        try:
            r = requests.get(url, timeout=1.0)
            if r.status_code == 200:
                logging.info("Server is ready.")
                return True
        except Exception:
            pass
        if time.time() - start > timeout:
            logging.warning("Server did not become ready within timeout.")
            return False
        time.sleep(interval)

# callback to run in webview GUI thread after window is created
def on_gui_ready():
    try:
        # maximize the first (and only) window
        if webview.windows:
            try:
                webview.windows[0].maximize()
                logging.info("Window maximized via webview API.")
            except Exception as e:
                logging.warning(f"Failed to maximize via webview.windows[0].maximize(): {e}")
    except Exception:
        logging.exception("Exception in on_gui_ready.")

if __name__ == "__main__":
    # start flask in background
    t = threading.Thread(target=run_flask, daemon=True)
    t.start()

    # wait until server responds
    server_ready = wait_for_server(URL)

    # note: we don't pass icon= to create_window because pywebview v6 doesn't accept it.
    # Set the exe icon via PyInstaller (--icon "icon.ico") when building.
    try:
        webview.create_window(
            "Heart Disease Predictor",
            URL,
            width=1200,
            height=800,
            resizable=True
        )
        # webview.start accepts a callable to run in the GUI thread once the loop starts;
        # we use it to maximize the window.
        webview.start(func=on_gui_ready)
    except Exception:
        logging.exception("Failed to create or start webview.")
    logging.info("Heart Disease Predictor launcher exiting.")