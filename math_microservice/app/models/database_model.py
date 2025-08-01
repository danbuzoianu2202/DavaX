from datetime import datetime

from app.extensions import db


class OperationRequest(db.Model):
    """
    Model representing a mathematical operation request.
    This model stores details about the operation, input data, result,
    status, and metadata such as timestamps and client information.

    Attributes:
        id (int): Primary key for the request.
        operation (str): Type of operation.
        input_data (str): JSON string containing the input data.
        result (str): Result of the operation, if available.
        status (str): Status of the request (e.g., 'success', 'error').
        error_message (str): Error message if the operation failed.
        execution_time_ms (int): Execution time in milliseconds.
        client_ip (str): IP address of the client making the request.
        user_agent (str): User agent string of the client.
        timestamp (datetime): Timestamp when the request was created.
    """
    id = db.Column(db.Integer, primary_key=True)
    operation = db.Column(db.String(50), nullable=False)
    input_data = db.Column(db.Text, nullable=False)
    result = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(20), nullable=False, default="success")
    error_message = db.Column(db.Text, nullable=True)
    execution_time_ms = db.Column(db.Integer, nullable=True)
    client_ip = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        """
        String representation of the OperationRequest model.
        :return: A string representation of the request.
        """
        return f"<Request {self.operation} [{self.status}] @ {self.timestamp}>"
