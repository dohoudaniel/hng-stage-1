from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from os import environ

app = Flask(__name__)
CORS(app)

def validate_integer(input_str):
    """Robust integer validation for all integer formats"""
    cleaned = input_str.strip().lstrip('+')
    if not cleaned:
        return None
    
    negative = False
    if cleaned.startswith('-'):
        negative = True
        cleaned = cleaned[1:].strip()
    
    if not cleaned.isdigit():
        return None
    
    try:
        value = int(cleaned)
        return -value if negative else value
    except ValueError:
        return None

def check_prime(n):
    """Prime check valid for all integers"""
    if n <= 1:
        return False
    n = abs(n)  # Primes are absolute
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def check_perfect(n):
    """Perfect number check (positive numbers only)"""
    if n <= 0:
        return False
    total = 1
    sqrt_n = int(n**0.5)
    for i in range(2, sqrt_n + 1):
        if n % i == 0:
            total += i
            if i != n // i:
                total += n // i
    return total == n

def check_armstrong(n):
    """Armstrong number check valid for all integers"""
    try:
        num_str = str(abs(n))
        length = len(num_str)
        return sum(int(d)**length for d in num_str) == abs(n)
    except:
        return False

def sum_digits(n):
    """Digit sum works for negative numbers"""
    return sum(int(d) for d in str(abs(n)))

def get_fun_fact(n):
    """Enhanced Numbers API call with error handling"""
    try:
        url = f"http://numbersapi.com/{n}/math"
        response = requests.get(url, timeout=3, params={'json': True})
        if response.status_code == 200:
            return response.json().get('text', 'No fun fact available')
        return "No fun fact available"
    except Exception as e:
        print(f"Error fetching fun fact: {e}")
        return "No fun fact available"

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number_param = request.args.get('number', '')
    
    # Validate input
    validation = validate_integer(number_param)
    if validation is None:
        return jsonify({
            "number": number_param,
            "error": True
        }), 400
    
    number = validation
    abs_number = abs(number)
    
    # Calculate properties
    is_armstrong = check_armstrong(number)
    parity = 'even' if number % 2 == 0 else 'odd'
    
    properties = []
    if is_armstrong:
        properties.append('armstrong')
    properties.append(parity)
    
    # Build response
    return jsonify({
        "number": number,
        "is_prime": check_prime(number),
        "is_perfect": check_perfect(abs_number) if number > 0 else False,
        "properties": properties,
        "digit_sum": sum_digits(number),
        "fun_fact": get_fun_fact(number)
    })

if __name__ == '__main__':
    port = int(environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)