from flask import Flask, jsonify, request
from flask_cors import CORS
from os import environ
import requests

# Initialize the Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross Origin Resource Sharing (CORS)

# Disable key sorting for Flask's JSON encoder (as requested in requirements)
app.json.sort_keys = False


def is_prime(n):
    """
    A function to check if a number is prime.
    """
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def is_perfect(n):
    """
    A function to check if a number is perfect.
    """
    if n < 1:
        return False
    divisors = [i for i in range(1, n) if n % i == 0]
    return sum(divisors) == n


def is_armstrong(n):
    """
    A function to check if a number is an Armstrong number.
    """
    digits = str(n)
    power = len(digits)
    return sum(int(digit) ** power for digit in digits) == n


def is_float(value):
    """
    A function to check if a value is a valid float.
    """
    try:
        float(value)  # Try to convert to float
        return True
    except ValueError:
        return False


def digit_sum(n):
    """
    A function to calculate the sum of the digits of a number.
    """
    return sum(int(digit) for digit in str(abs(n)))


@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    """
    Checks the mathematical properties of a number,
    and returns a JSON response containing the number,
    its properties, and a fun fact about the number
    from the Numbers API.
    """
    # Get the number parameter from the query string
    number = request.args.get('number')

    # Check if the number is valid (either an integer or float)
    if not number or (not number.lstrip('-').isdigit() and not is_float(number)):
        data = {
            "number": "alphabet",
            "error": True
        }
        return jsonify(data), 400

    # Convert the number to a float
    number = float(number)

    # Work with the absolute value for mathematical checks
    abs_number = abs(number)

    # Convert the absolute number to an integer for checking properties
    int_number = int(abs_number)
    print(int_number)

    # Checking the mathematical properties of the integer portion
    prime = is_prime(int_number)
    perfect = is_perfect(int_number)
    armstrong = is_armstrong(int_number)
    sum_digits = digit_sum(int_number)
    parity = "odd" if int_number % 2 != 0 else "even"

    properties = []
    if armstrong:
        properties.append("armstrong")
    properties.append(parity)

    # Fetch the fun fact from the Numbers API using the math endpoint
    api_url = f"http://numbersapi.com/{int_number}/math?json"
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        fun_fact = data.get("text", "")
    except Exception as e:
        fun_fact = f"Could not retrieve fun fact: {str(e)}"

    # Build the JSON response
    data = {
        "number": number,
        "is_prime": prime,
        "is_perfect": perfect,
        "properties": properties,
        "digit_sum": sum_digits,
        "fun_fact": fun_fact
    }
    return jsonify(data), 200  # Return the JSON response with status 200


# Handling error pages and wrong redirections
@app.errorhandler(404)
def page_not_found(e):
    """
    Returns an error message in JSON
    when the user tries to access
    a invalid or undefined route.
    """
    data = {
        "number": "alphabet",
        "error": True
    }
    return jsonify(data), 404


"""
Running the application
"""
if __name__ == "__main__":
    port = int(environ.get("PORT", 5000))  # Default to 5000 if not provided
    app.run(host="0.0.0.0", port=port)  # Listen on all interfaces (0.0.0.0) and use the specified port
