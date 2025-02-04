from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    # Get the 'number' parameter from the query string
    number_param = request.args.get('number')

    # Validate the parameter
    if not number_param or not number_param.isdigit():
        return jsonify({
            "number": number_param,
            "error": True
        }), 400

    # Convert the parameter to an integer
    number = int(number_param)

    # Now you can proceed with your logic (e.g., classification, fun fact retrieval)
    # For demonstration, let's just return the number:
    return jsonify({
        "number": number,
        # ... additional fields to be added after classification ...
    })

if __name__ == '__main__':
    app.run(debug=True)
