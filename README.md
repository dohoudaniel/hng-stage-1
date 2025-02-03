# Number Classification API - HNG Stage 1

## Overview

This project is a simple Python Flask backend API that classifies numbers based on several mathematical properties, including whether they are prime, perfect, Armstrong, or even/odd. Additionally, it retrieves a fun fact about the number using the [Numbers API](http://numbersapi.com/#42).

The API is designed to handle Cross-Origin Resource Sharing (CORS) requests and provide the result in JSON format.

## Table of Contents

- [Number Classification API - HNG Stage 1](#number-classification-api---hng-stage-1)
  - [Overview](#overview)
  - [Table of Contents](#table-of-contents)
  - [Project Requirements](#project-requirements)
  - [API Specification](#api-specification)
    - [Successful Response (200 OK)](#successful-response-200-ok)
    - [Error Response (400 Bad Request)](#error-response-400-bad-request)
    - [Response Details](#response-details)
  - [Endpoints](#endpoints)
    - [`GET /api/classify-number?number=<number>`](#get-apiclassify-numbernumbernumber)
    - [Example Request:](#example-request)
    - [Example Response:](#example-response)
  - [How to Use](#how-to-use)
    - [Example:](#example)
  - [Error Handling](#error-handling)
  - [Deployment](#deployment)
  - [Running the Application Locally](#running-the-application-locally)
    - [Prerequisites:](#prerequisites)
    - [Steps:](#steps)
  - [License](#license)

## Project Requirements

- **Technology Stack**: Python (Flask), CORS
- **Deployment**: Publicly accessible API (deployed on [Render](https://ddf-hng-stage-0.onrender.com))
- **Functionality**:
  - Accepts GET requests with a `number` query parameter.
  - Returns properties such as prime, perfect, Armstrong, and even/odd.
  - Fetches a fun fact about the number from the Numbers API.
  - Returns the result in JSON format.
  - Includes appropriate error handling for invalid inputs.
- **Version Control**: The project is hosted on GitHub and includes a public repository.
- **API Format**: JSON

## API Specification

**Endpoint**: `GET /api/classify-number?number=<number>`

### Successful Response (200 OK)
```json
{
    "number": 371,
    "is_prime": false,
    "is_perfect": false,
    "properties": ["armstrong", "odd"],
    "digit_sum": 11,
    "fun_fact": "371 is an Armstrong number because 3^3 + 7^3 + 1^3 = 371"
}
```

### Error Response (400 Bad Request)
```json
{
    "number": "alphabet",
    "error": true
}
```

### Response Details

- `number`: The number passed to the API.
- `is_prime`: A boolean indicating if the number is prime.
- `is_perfect`: A boolean indicating if the number is perfect.
- `properties`: A list containing properties such as "armstrong" and either "odd" or "even".
- `digit_sum`: The sum of the digits of the number.
- `fun_fact`: A fun fact retrieved from the Numbers API.

## Endpoints

### `GET /api/classify-number?number=<number>`
- **Parameters**: 
  - `number`: The number to classify (integer).
- **Response**:
  - JSON response with the classification details.
  
### Example Request:
```
GET http://your-domain.com/api/classify-number?number=371
```

### Example Response:
```json
{
    "number": 371,
    "is_prime": false,
    "is_perfect": false,
    "properties": ["armstrong", "odd"],
    "digit_sum": 11,
    "fun_fact": "371 is an Armstrong number because 3^3 + 7^3 + 1^3 = 371"
}
```

## How to Use

1. **Send a GET request** to the endpoint `/api/classify-number?number=<number>`.
2. **Provide a valid number** as the query parameter.
3. The response will include classification details and a fun fact about the number.

### Example:

Request:
```
GET http://your-domain.com/api/classify-number?number=371
```

Response:
```json
{
    "number": 371,
    "is_prime": false,
    "is_perfect": false,
    "properties": ["armstrong", "odd"],
    "digit_sum": 11,
    "fun_fact": "371 is an Armstrong number because 3^3 + 7^3 + 1^3 = 371"
}
```

## Error Handling

- **Invalid Number**: If the `number` parameter is not a valid integer or is missing, the API will respond with a `400 Bad Request` status code and an appropriate error message in JSON format.
  
  Example:
  ```json
  {
      "number": "alphabet",
      "error": true
  }
  ```

- **Undefined Route**: If a user accesses an undefined route, a `404 Not Found` error will be returned with a JSON error message.
  
  Example:
  ```json
  {
      "number": "alphabet",
      "error": true
  }
  ```

## Deployment

This API is hosted on a publicly accessible platform of your choice ([Render](https://ddf-hng-stage-1.onrender.com)). It supports **CORS** (Cross-Origin Resource Sharing), allowing access from different domains.

The API is optimized for a fast response time (less than 500ms).

## Running the Application Locally

### Prerequisites:
- Python 3.x
- pip (Python package installer)

### Steps:

1. **Clone the repository**:
   ```
   git clone https://github.com/your-username/number-classification-api.git
   ```

2. **Navigate to the project directory**:
   ```
   cd number-classification-api
   ```

3. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Run the Flask application**:
   ```
   python app.py
   ```

5. **Access the API locally** at `http://127.0.0.1:5000/api/classify-number?number=<number>`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
