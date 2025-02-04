from flask import Flask, request, jsonify
import requests
import math
import os

app = Flask(__name__)

def is_armstrong(num):
    original_num = num
    num_digits = len(str(abs(num)))  # Handle negative numbers
    sum_of_powers = 0
    temp_num = abs(num) # work with absolute value
    while temp_num > 0:
        digit = temp_num % 10
        sum_of_powers += digit ** num_digits
        temp_num //= 10
    return sum_of_powers == original_num and num > 0 # Negative numbers cannot be Armstrong


def is_prime(num):
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True and num > 0 #Negative numbers cannot be prime

def is_perfect(num):
    if num <= 0:
        return False
    sum_of_divisors = 0
    for i in range(1, abs(num)): #check up to the absolute value
        if num % i == 0:
            sum_of_divisors += i
    return sum_of_divisors == abs(num) and num > 0  #Negative numbers cannot be perfect

def digit_sum(num):
    s = 0
    for digit in str(abs(num)): #work with absolute value
        s += int(digit)
    return s

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    try:
        num = int(request.args.get('number'))

        if not isinstance(num, int):
            raise ValueError("Invalid input. Number must be an integer.")

        is_prime_num = is_prime(num)
        is_perfect_num = is_perfect(num)
        is_armstrong_num = is_armstrong(num)

        properties = []
        if is_armstrong_num:
            properties.append("armstrong")
        if num % 2 == 0:
            properties.append("even")
        else:
            properties.append("odd")

        try:
            fun_fact_response = requests.get(f"http://numbersapi.com/{num}/math")
            fun_fact_response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            fun_fact = fun_fact_response.text.strip()
        except requests.exceptions.RequestException as e:
            fun_fact = f"Could not retrieve fun fact: {e}"


        response = {
            "number": num,
            "is_prime": is_prime_num,
            "is_perfect": is_perfect_num,
            "properties": properties,
            "digit_sum": digit_sum(num),
            "fun_fact": fun_fact
        }
        return jsonify(response), 200

    except ValueError as e:
        return jsonify({"number": request.args.get('number'), "error": True}), 400
    except Exception as e:
        return jsonify({"number": request.args.get('number'), "error": True, "message": str(e)}), 500 # More detailed error for debugging


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) # Get port from environment or default to 5000