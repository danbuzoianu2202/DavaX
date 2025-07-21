import requests

from flask import Blueprint, render_template, request


ui_bp = Blueprint("ui", __name__, template_folder="templates")


@ui_bp.route("/")
def home():
    """
    Render the home page with a form for operations.

    :return: Rendered HTML template for the home page.
    """
    return render_template(
        "index.html",
        result=None,
        error=None,
        selected="pow",  # default operation
        base="",
        exponent="",
        n=""
    )


@ui_bp.route("/compute", methods=["POST"])
def compute():
    """
    Handle the form submission for operations.
    Extracts the operation type and parameters from the form,
    sends a request to the API, and renders the result.

    :return: Rendered HTML template with the result or error."""
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

        response = requests.post(f"http://localhost:5000/api/v1/{operation}",
                                 json=payload)
        result = response.json().get("result")

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
