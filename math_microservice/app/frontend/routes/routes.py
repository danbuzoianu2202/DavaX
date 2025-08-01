import requests
from flask import Blueprint, render_template, request


class UIController:
    """
    Controller for handling UI routes and rendering templates.
    This class defines the routes for the frontend application,
    including the home page and the compute operation.
    """
    def __init__(self, name="ui", template_folder="templates"):
        """
        Initialize the UIController with a Flask Blueprint.

        :param name: Name of the blueprint.
        :param template_folder: Folder where templates are stored.
        """
        self.bp = Blueprint(name, __name__, template_folder=template_folder)
        self._register_routes()

    def _register_routes(self):
        self.bp.add_url_rule("/", view_func=self.home)
        self.bp.add_url_rule("/compute",
                             view_func=self.compute,
                             methods=["POST"])

    def home(self):
        """
        Render the home page with default form inputs.
        """
        return render_template(
            "index.html",
            result=None,
            error=None,
            selected="pow",
            base="",
            exponent="",
            n=""
        )

    def compute(self):
        """
        Handle the form submission and call the API accordingly.
        """
        operation = request.form.get("operation")
        base = request.form.get("base", "")
        exponent = request.form.get("exponent", "")
        n = request.form.get("n", "")

        payload = {}
        result = None
        error = None

        try:
            if operation == "pow":
                if not base or not exponent:
                    raise ValueError("Base and exponent are required.")
                payload = {"base": int(base), "exponent": int(exponent)}

            elif operation == "fibonacci":
                if not n:
                    raise ValueError("N is required for Fibonacci.")
                payload = {"n": int(n)}

            elif operation == "factorial":
                if not n:
                    raise ValueError("N is required for Factorial.")
                payload = {"n": int(n)}

            response = \
                requests.post(f"http://localhost:5000/api/v1/{operation}",
                              json=payload)
            json_data = response.json()

            if "result" in json_data:
                result = json_data["result"]
            elif "status" in json_data:
                error = json_data["status"]
            else:
                error = "Unknown response format."

        except ValueError as e:
            error = str(e)
        except Exception:
            error = "Internal error occurred."

        return render_template(
            "index.html",
            result=result,
            error=error,
            selected=operation,
            base=base,
            exponent=exponent,
            n=n
        )
