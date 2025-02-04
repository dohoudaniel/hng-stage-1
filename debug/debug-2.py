from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from os import environ
from datetime import datetime

app = Flask(__name__)
CORS(app)

def validate_integer(input_str):
    """Validate if input is a valid integer (positive or negative)"""
    try:
        return int(input_str)
    except ValueError:
        # Check for negative numbers with extra characters
        if input_str.startswith('-'):
            remaining = input_str[1:].strip()
            if remaining.isdigit():
                return -int(remaining)
        return None

def check_prime(n):
    """Check if a number is prime (works for negative numbers)"""
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(abs(n)**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def check_perfect(n):
    """Check if a number is perfect (only valid for positive numbers)"""
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
    """Check Armstrong number (valid for positive numbers only)"""
    if n < 0:
        return False
    digits = str(n)
    length = len(digits)
    return sum(int(d)**length for d in digits) == n

def sum_digits(n):
    """Calculate sum of absolute value's digits"""
    return sum(int(d) for d in str(abs(n)))

def get_fun_fact(n):
    """Get math fact for any integer (positive or negative)"""
    try:
        response = requests.get(
            f"http://numbersapi.com/{n}/math",
            timeout=3,
            headers={'Accept': 'text/plain'}
        )
        return response.text.strip() if response.status_code == 200 else "No fun fact available"
    except (requests.exceptions.RequestException, ValueError):
        return "No fun fact available"

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number_param = request.args.get('number', '').strip()
    
    if not number_param:
        return jsonify({"number": None, "error": True}), 400
    
    # Enhanced integer validation
    number = validate_integer(number_param)
    if number is None:
        return jsonify({"number": number_param, "error": True}), 400

    # Mathematical properties calculation
    is_armstrong = check_armstrong(number)
    parity = 'even' if number % 2 == 0 else 'odd'
    
    properties = []
    if is_armstrong:
        properties.append('armstrong')
    properties.append(parity)

    return jsonify({
        "number": number,
        "is_prime": check_prime(number),
        "is_perfect": check_perfect(abs(number)) if number > 0 else False,
        "properties": properties,
        "digit_sum": sum_digits(number),
        "fun_fact": get_fun_fact(number)
    })

if __name__ == '__main__':
    port = int(environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)