
import logging
import time
import uuid

from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from app.schemas.operation import \
    PowRequest, FibonacciRequest, FactorialRequest
from app.worker import TASK_QUEUE, result_store


api_bp = Blueprint("api", __name__)
logger = logging.getLogger(__name__)


def enqueue_and_wait(operation: str, data_dict: dict):
    """
    Enqueue a task and wait for its result.
    This function puts a task into the task queue and waits for the result
    for a specified timeout period.

    :param operation: The type of operation to perform.
    :param data_dict: The data to be processed by the operation.
    :return: A dict containing the task ID and the result or a status message.
    """
    task_id = str(uuid.uuid4())
    TASK_QUEUE.put({"operation": operation,
                    "data": data_dict,
                    "task_id": task_id})
    logger.info(f"Queued {operation} task {task_id}")

    timeout = 5  # seconds
    interval = 0.1
    waited = 0

    while waited < timeout:
        if task_id in result_store:
            return {"task_id": task_id, "result": result_store[task_id]}
        time.sleep(interval)
        waited += interval

    return {"task_id": task_id, "status": "Still processing"}


@api_bp.route("/pow", methods=["POST"])
def pow_endpoint():
    """Endpoint to handle power calculations.
    Expects a JSON body with 'base' and 'exponent' fields.

    :return: A JSON response with the task ID and result."""
    try:
        data = PowRequest(**request.json)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    result = enqueue_and_wait("pow", data.model_dump())
    return jsonify(result)


@api_bp.route("/fibonacci", methods=["POST"])
def fibonacci_endpoint():
    """Endpoint to handle Fibonacci calculations.
    Expects a JSON body with 'n' field.

    :return: A JSON response with the task ID and result."""
    try:
        data = FibonacciRequest(**request.json)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    result = enqueue_and_wait("fibonacci", data.model_dump())
    return jsonify(result)


@api_bp.route("/factorial", methods=["POST"])
def factorial_endpoint():
    """Endpoint to handle factorial calculations.
    Expects a JSON body with 'n' field.

    :return: A JSON response with the task ID and result."""
    try:
        data = FactorialRequest(**request.json)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    result = enqueue_and_wait("factorial", data.model_dump())
    return jsonify(result)


@api_bp.route("/result/<task_id>", methods=["GET"])
def get_result(task_id):
    """
    Endpoint to retrieve the result of a task by its ID.
    Returns a JSON response with the task ID and result if available,
    or a status message if the task is still processing.

    :param task_id: The ID of the task to retrieve the result for.
    :return: A JSON response with the task ID and result or status message."""
    if task_id in result_store:
        return jsonify({"task_id": task_id, "result": result_store[task_id]})
    return jsonify({"status": "Processing or task ID not found"}), 202
