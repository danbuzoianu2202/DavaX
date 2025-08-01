import json

from app.models.database_model import OperationRequest
from app.extensions import db


class RequestLogger:
    @staticmethod
    def save(operation,
             input_data,
             result=None,
             status="success",
             error_message=None,
             execution_time_ms=None,
             client_ip=None,
             user_agent=None):
        """
        Save a mathematical operation request to the database.

        Save a mathematical operation request to the database.

        :param operation: The type of operation performed.
        :param input_data: The input data for the operation, as a dict.
        :param result: The result of the operation, if available.
        :param status: The status of the request (default is "success").
        :param error_message: An error message if the operation failed.
        :param execution_time_ms: The execution time in milliseconds.
        :param client_ip: The IP address of the client making the request.
        :param user_agent: The user agent string of the client.
        """
        entry = OperationRequest(
            operation=operation,
            input_data=json.dumps(input_data),
            result=str(result) if result is not None else None,
            status=status,
            error_message=error_message,
            execution_time_ms=execution_time_ms,
            client_ip=client_ip,
            user_agent=user_agent
        )

        db.session.add(entry)
        db.session.commit()
