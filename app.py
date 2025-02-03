"""
A Python Flask app that acts as an API.
It returns a JSON response containing
my email, the current datetime, and
my GitHub URL.
This Flask application also handles
Cross Origin Resource Sharing (CORS)
issues and requests.
"""
# Import statements
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from os import environ

# Initialize the Flask app
app = Flask(__name__)
CORS(app)

# Disable key sorting for Flask's JSON encoder (as requested in requirements)
app.json.sort_keys = False


def check_prime(n):
    """
    A function to check if a number is prime.
    """
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def check_perfect(n):
    """
    A function to check if a number is perfect.
    """
    if n <= 1:
        return False
    total = 1
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            total += i
            if i != n // i:
                total += n // i
    return total == n


def check_armstrong(n):
    """
    A function to check if a number is an Armstrong number.
    """
    digits = list(str(n))
    length = len(digits)
    total = sum(int(d)**length for d in digits)
    return total == n


def sum_digits(n):
    """
    A function to calculate the sum of the digits of a number.
    """
    return sum(int(d) for d in str(abs(n)))


def get_fun_fact(n):
    """
    A function to get a fun fact about a number
    using the Numbers API.
    """
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math", timeout=3)
        if response.status_code == 200:
            return response.text.strip()
        return "No fun fact available"
    except (requests.exceptions.RequestException, ValueError):
        return "No fun fact available"

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    """
    Checks the mathematical properties of a number,
    and returns a JSON response containing the number,
    its properties, and a fun fact about the number
    from the Numbers API.
    """
    # Get the number parameter from the query string
    number_param = request.args.get('number')

    if not number_param:
        return jsonify({"number": None, "error": True}), 400

    try:
        number = int(number_param)
    except ValueError:
        return jsonify({"number": number_param, "error": True}), 400

    properties = []
    is_armstrong = check_armstrong(number)
    parity = 'even' if number % 2 == 0 else 'odd'

    if is_armstrong:
        properties.append('armstrong')
    properties.append(parity)

    return jsonify({
        "number": number,
        "is_prime": check_prime(number),
        "is_perfect": check_perfect(number),
        "properties": properties,
        "digit_sum": sum_digits(number),
        "fun_fact": get_fun_fact(number)
    })


# Running the Flask app
if __name__ == '__main__':
    port = int(environ.get("PORT", 5000))  # Default to 5000 if not provided
    app.run(host="0.0.0.0", port=port)  # Listen on all interfaces (0.0.0.0) and use the specified port
