from app import create_app
from app.worker import Worker
import threading
import logging

app = create_app()

# Create a global worker instance
worker = Worker()
worker.set_flask_app(app)

app.worker = worker

# Launch the worker in a background thread
threading.Thread(target=worker.start, daemon=True).start()

# Optional logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Worker thread started. App running at http://localhost:5000")

if __name__ == "__main__":
    app.run(debug=True)
