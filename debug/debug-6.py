from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

def check_prime(n):
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
    digits = list(str(n))
    length = len(digits)
    total = sum(int(d)**length for d in digits)
    return total == n

def sum_digits(n):
    return sum(int(d) for d in str(abs(n)))

def get_fun_fact(n):
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math", timeout=3)
        if response.status_code == 200:
            return response.text.strip()
        return "No fun fact available"
    except (requests.exceptions.RequestException, ValueError):
        return "No fun fact available"

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)