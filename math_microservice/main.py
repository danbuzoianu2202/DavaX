from app import create_app
from app.worker import start_worker, set_flask_app
import threading
import logging

app = create_app()
set_flask_app(app)  # Pass the app to the worker module

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting worker thread...")
    thread = threading.Thread(target=start_worker, daemon=True)
    thread.start()

    logger.info("Starting Flask app on http://localhost:5000 ...")
    app.run(debug=True)
