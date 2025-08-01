import time
import queue
import logging

from app.core.services import Services
from app.utils.request_logger import RequestLogger

logger = logging.getLogger(__name__)


class Worker:
    def __init__(self):
        self.task_queue = queue.Queue()
        self.result_store = {}
        self.app = None

    def set_flask_app(self, flask_app):
        """
        Set the Flask app context to allow DB access and config usage.

        :param flask_app: Flask app instance.
        :raises RuntimeError: If the app is already set.
        """
        if self.app is not None:
            raise RuntimeError("Flask app already set.")
        self.app = flask_app

    def enqueue_task(self, task):
        """
        Add a task to the queue.

        :param task: A dict containing task_id, operation, and data.
        """
        self.task_queue.put(task)

    def get_result(self, task_id):
        """
        Retrieve the result of a completed task.

        :param task_id: The unique identifier for the task.
        :return: The result if available, otherwise None.
        """
        return self.result_store.get(task_id)

    def _process_task(self, task):
        """
        Internal method to process a single task.

        :param task: Dict with keys: task_id, operation, data.
        """
        if self.app is None:
            raise RuntimeError("Flask app is not set in worker module.")

        with self.app.app_context():
            task_id = task["task_id"]
            operation = task["operation"]
            data = task["data"]

            client_ip = task.get("client_ip")
            user_agent = task.get("user_agent")

            logger.info(f"Processing task: {operation} with data {data}")

            start_time = time.time()

            try:
                if operation == "pow":
                    result = Services.calculate_power(data["base"],
                                                      data["exponent"])
                elif operation == "fibonacci":
                    result = Services.calculate_fibonacci(data["n"])
                elif operation == "factorial":
                    result = Services.calculate_factorial(data["n"])
                else:
                    result = "Invalid operation"

                logger.info(f"Result: {result}")
                execution_time_ms = int((time.time() - start_time) * 1000)
                RequestLogger.save(
                    operation, data,
                    result=result,
                    status="success",
                    execution_time_ms=execution_time_ms,
                    client_ip=client_ip,
                    user_agent=user_agent
                )
            except Exception as e:
                logger.error(f"Error processing task: {e}")
                execution_time_ms = int((time.time() - start_time) * 1000)

                RequestLogger.save(operation,
                                   data,
                                   result=None,
                                   status="error",
                                   error_message=str(e),
                                   execution_time_ms=execution_time_ms,
                                   client_ip=client_ip,
                                   user_agent=user_agent)
                result = f"Error: {e}"

            self.result_store[task_id] = result

    def start(self):
        """
        Continuously process tasks from the queue.
        This is typically run in a separate thread or background process.
        """
        while True:
            try:
                task = self.task_queue.get(timeout=1)
                self._process_task(task)
                self.task_queue.task_done()
            except queue.Empty:
                time.sleep(0.1)
