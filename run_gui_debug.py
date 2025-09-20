# run_gui_debug.py - launcher with extra debug traces around webview calls
import threading, time, webview, requests, sys, os, logging
from app import app

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)

# logging to file and console
log_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "run_gui_debug.log")

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler(log_file, encoding="utf-8"), logging.StreamHandler(sys.stdout)]
)

def excepthook(exc_type, exc, tb):
    logging.exception("Uncaught exception:", exc_info=(exc_type, exc, tb))
sys.excepthook = excepthook

HOST = "127.0.0.1"
PORT = 5000
URL = f"http://{HOST}:{PORT}/"

def run_flask():
    try:
        app.run(host=HOST, port=PORT, debug=False, threaded=True, use_reloader=False)
    except Exception:
        logging.exception("Flask failed to start.")

def wait_for_server(url, timeout=30.0, interval=0.25):
    start = time.time()
    while True:
        try:
            r = requests.get(url, timeout=1.0)
            if r.status_code == 200:
                logging.info("Server responded 200 OK.")
                return True
        except Exception as e:
            logging.debug(f"Server not ready yet: {e}")
        if time.time() - start > timeout:
            logging.warning("Server wait timed out.")
            return False
        time.sleep(interval)

if __name__ == "__main__":
    logging.info("DEBUG launcher starting...")
    t = threading.Thread(target=run_flask, daemon=True)
    t.start()

    ready = wait_for_server(URL)
    logging.info(f"Server ready: {ready}")

    icon_path = resource_path("icon.ico")
    logging.info(f"Icon path resolved to: {icon_path}, exists: {os.path.exists(icon_path)}")

    try:
        logging.info("About to call webview.create_window(...)")
        webview.create_window("Heart Disease Predictor (DEBUG)", URL, icon=icon_path, width=1200, height=800, resizable=True)
        logging.info("webview.create_window returned (no exception). Now calling webview.start()")
        webview.start()
        logging.info("webview.start() returned (window closed).")
    except Exception:
        logging.exception("Exception while creating/starting webview.")

