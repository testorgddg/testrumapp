import time
import random
import requests
from flask import Flask, jsonify, request
from ddtrace import tracer


app = Flask(__name__)


@app.route("/")
def index():
    """Return a welcome message with available endpoints."""
    return jsonify({
        "service": "test-rum-app",
        "endpoints": [
            {"path": "/", "description": "This help message"},
            {"path": "/hello", "description": "Simple traced endpoint"},
            {"path": "/slow", "description": "Simulates a slow request"},
            {"path": "/external", "description": "Makes an external HTTP call"},
            {"path": "/chain", "description": "Chains multiple operations with custom spans"},
            {"path": "/error", "description": "Triggers an error for error tracking"},
            {"path": "/health", "description": "Health check"},
        ],
    })


@app.route("/hello")
def hello():
    """Return a simple greeting."""
    return jsonify({"message": "Hello from Datadog APM!", "traced": True})


@app.route("/slow")
def slow():
    """Simulate a slow endpoint with a random delay between 0.5 and 2 seconds."""
    delay = random.uniform(0.5, 2.0)
    time.sleep(delay)
    return jsonify({"message": "Slow response completed", "delay_seconds": round(delay, 2)})


@app.route("/external")
def external_call():
    """Make an HTTP GET request to httpbin to demonstrate distributed tracing across HTTP calls."""
    with tracer.trace("external.httpbin", service="httpbin-client"):
        response = requests.get("https://httpbin.org/delay/1", timeout=10)
    return jsonify({
        "message": "External call completed",
        "status_code": response.status_code,
        "remote_url": "https://httpbin.org/delay/1",
    })


@app.route("/chain")
def chain():
    """Execute a chain of three custom-traced operations to demonstrate nested spans."""
    results = []

    with tracer.trace("chain.step_1", service="test-rum-app", resource="validate_input"):
        time.sleep(random.uniform(0.05, 0.15))
        results.append("step_1: input validated")

    with tracer.trace("chain.step_2", service="test-rum-app", resource="process_data"):
        time.sleep(random.uniform(0.1, 0.3))
        results.append("step_2: data processed")

    with tracer.trace("chain.step_3", service="test-rum-app", resource="format_output"):
        time.sleep(random.uniform(0.02, 0.1))
        results.append("step_3: output formatted")

    return jsonify({"chain_results": results})


@app.route("/error")
def trigger_error():
    """Deliberately raise an exception to demonstrate error tracking in Datadog APM."""
    error_type = request.args.get("type", "value")
    if error_type == "value":
        raise ValueError("This is a deliberate ValueError for testing Datadog error tracking")
    elif error_type == "runtime":
        raise RuntimeError("This is a deliberate RuntimeError for testing Datadog error tracking")
    elif error_type == "zero":
        return jsonify({"result": 1 / 0})
    raise Exception("Generic test exception for Datadog error tracking")


@app.route("/health")
def health():
    """Return the health status of the app."""
    return jsonify({"status": "healthy"}), 200


@app.errorhandler(Exception)
def handle_exception(e):
    """Catch unhandled exceptions, set the error on the active Datadog span, and return a JSON error response."""
    span = tracer.current_span()
    if span:
        span.set_tag("error", True)
        span.set_tag("error.message", str(e))
        span.set_tag("error.type", type(e).__name__)
    return jsonify({"error": type(e).__name__, "message": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
