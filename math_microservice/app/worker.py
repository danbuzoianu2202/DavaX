import time
import queue
import logging

from app.core.services import Services
from app.utils.helpers import save_request

logger = logging.getLogger(__name__)
TASK_QUEUE = queue.Queue()

app = None
result_store = dict()


def set_flask_app(flask_app):
    """
    Set the Flask app instance for the worker module.

    :param flask_app: The Flask app instance to set.
    :raises RuntimeError: If the Flask app is already set.
    """
    global app
    app = flask_app


def process_task(task):
    """"Process a task from the queue.
    This function retrieves the task from the queue,
    processes it based on the operation type,
    and saves the result to the database.

    :param task: Dict containing the operation type, input data, and task ID.
    """
    if app is None:
        raise RuntimeError("Flask app is not set in worker module.")

    with app.app_context():
        task_id = task["task_id"]
        operation = task["operation"]
        data = task["data"]
        logger.info(f"Processing task: {operation} with data {data}")

        if operation == "pow":
            result = Services.calculate_power(data["base"], data["exponent"])
        elif operation == "fibonacci":
            result = Services.calculate_fibonacci(data["n"])
        elif operation == "factorial":
            result = Services.calculate_factorial(data["n"])
        else:
            result = "Invalid operation"

        logger.info(f"Result: {result}")
        save_request(operation, data, result)

        result_store[task_id] = result


def start_worker():
    """
    Start the worker to process tasks from the queue.
    This function runs in an infinite loop,
    continuously checking for tasks in the queue and processing them.
    """
    while True:
        try:
            task = TASK_QUEUE.get(timeout=1)
            process_task(task)
            TASK_QUEUE.task_done()
        except queue.Empty:
            time.sleep(0.1)
