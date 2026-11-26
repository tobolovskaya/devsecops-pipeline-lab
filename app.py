"""Small Flask app used to demonstrate a DevSecOps pipeline."""
import ast

from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/health")
def health():
    return {"status": "ok"}


@app.route("/execute")
def execute_code():
    """Evaluate a Python literal (number, string, list...), never code.

    eval() here would be code injection (Bandit B307). ast.literal_eval
    only accepts literals, and the result is HTML-escaped so a string
    such as "<script>" cannot run in the browser.
    """
    code = request.args.get("code")
    if not code:
        return "<p>No code to execute.</p>"
    try:
        result = ast.literal_eval(code)
    except (ValueError, SyntaxError):
        return "Error: Invalid input. Only literal values allowed."
    return f"<p>Result of execution: {escape(str(result))}</p>"
