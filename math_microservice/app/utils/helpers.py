import json

from app.models.database_model import OperationRequest
from app.extensions import db


def save_request(operation, input_data, result):
    """
    Save the operation request and result to the database.

    :param operation: Type of operation ('pow', 'fibonacci', 'factorial').
    :param input_data: The input data for the operation.
    :param result: The result of the operation."""
    entry = OperationRequest(
        operation=operation,
        input_data=json.dumps(input_data),
        result=str(result)
    )

    db.session.add(entry)
    db.session.commit()
