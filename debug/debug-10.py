"""
A Python Flask app that acts as an API.
It returns a JSON response containing
various mathematical properties of a number,
along with a fun fact retrieved from the Numbers API.
This Flask application also handles
Cross Origin Resource Sharing (CORS).
"""

# Import statements
from flask import Flask, jsonify, request
from flask_cors import CORS
from os import environ
import requests

# Initialize the Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing (CORS)

# Disable key sorting for Flask's JSON encoder
app.json.sort_keys = False


def is_prime(n):
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def is_perfect(n):
    """Check if a number is a perfect number."""
    if n < 1:
        return False
    divisors = [i for i in range(1, n) if n % i == 0]
    return sum(divisors) == n


def is_armstrong(n):
    """Check if a number is an Armstrong number."""
    digits = str(n)
    power = len(digits)
    return sum(int(digit) ** power for digit in digits) == n


def is_float(value):
    """Check if a value is a valid float."""
    try:
        float(value)  # Try converting to float
        return True
    except ValueError:
        return False


def digit_sum(n):
    """Calculate the sum of the digits of a number."""
    return sum(int(digit) for digit in str(abs(n)) if digit.isdigit())


@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    """
    Endpoint to classify a number based on mathematical properties.
    Handles both integers and floating-point numbers.
    """

    # Get the number parameter from the query string
    number_param = request.args.get('number')

    # Validate that the parameter is a number
    if not number_param or (not number_param.lstrip('-').replace('.', '', 1).isdigit()):
        return jsonify({"number": "alphabet", "error": True}), 400

    # Convert to float to handle decimals
    number = float(number_param)

    # Store the original input for response
    original_number = number

    # Convert negative numbers to positive for mathematical checks
    abs_number = abs(number)

    # Convert to integer for properties like prime, perfect, and Armstrong checks
    int_part = int(abs_number)

    # Compute mathematical properties for the integer part
    prime = is_prime(int_part)
    perfect = is_perfect(int_part)
    armstrong = is_armstrong(int_part)
    sum_digits = digit_sum(abs_number)
    parity = "odd" if int_part % 2 != 0 else "even"

    # Build properties list
    properties = []
    if armstrong:
        properties.append("armstrong")
    properties.append(parity)

    # Fetch fun fact from Numbers API using integer part
    api_url = f"http://numbersapi.com/{int_part}/math?json"
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Handle HTTP errors
        data = response.json()
        fun_fact = data.get("text", "")
    except Exception as e:
        fun_fact = f"Could not retrieve fun fact: {str(e)}"

    # Build JSON response
    result = {
        "number": original_number,
        "is_prime": prime,
        "is_perfect": perfect,
        "properties": properties,
        "digit_sum": sum_digits,
        "fun_fact": fun_fact
    }

    return jsonify(result), 200


# Handle undefined routes with a JSON response
@app.errorhandler(404)
def page_not_found(e):
    """Returns a JSON error message for undefined routes."""
    return jsonify({"number": "alphabet", "error": True}), 404


"""
Running the application
"""
if __name__ == "__main__":
    port = int(environ.get("PORT", 5000))  # Default to 5000 if not provided
    app.run(host="0.0.0.0", port=port)  # Listen on all interfaces (0.0.0.0) and use the specified port
