from datetime import datetime

from app.extensions import db


class OperationRequest(db.Model):
    """
    Model to store operation requests and results.
    Contains fields for operation type, input data, result, and timestamp.
    """
    id = db.Column(db.Integer, primary_key=True)
    operation = db.Column(db.String(50), nullable=False)
    input_data = db.Column(db.Text, nullable=False)
    result = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        """
        String representation of the OperationRequest model.
        Returns a string with the operation type and timestamp.
        """
        return f"<Request {self.operation} @ {self.timestamp}>"
