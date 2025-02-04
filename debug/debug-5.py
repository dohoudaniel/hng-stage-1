from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def check_prime(n: int) -> bool:
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    sqrt_n = int(n**0.5) + 1
    for i in range(3, sqrt_n, 2):
        if n % i == 0:
            return False
    return True

def check_perfect(n: int) -> bool:
    if n <= 1:
        return False
    sum_div = 1
    sqrt_n = int(n**0.5) + 1
    for i in range(2, sqrt_n):
        if n % i == 0:
            sum_div += i
            other_div = n // i
            if other_div != i:
                sum_div += other_div
    return sum_div == n

def check_armstrong(n: int) -> bool:
    if n < 0:
        return False
    s = str(n)
    length = len(s)
    total = 0
    for ch in s:
        digit = int(ch)
        total += digit ** length
    return total == n

def sum_digits(n: int) -> int:
    return sum(int(d) for d in str(abs(n)))

async def get_fun_fact(n: int) -> str:
    url = f"http://numbersapi.com/{n}/math?json"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get('text', 'No fun fact found.')
        else:
            return 'No fun fact available.'
    except (httpx.RequestError, ValueError):
        return 'No fun fact available.'

@app.get("/api/classify-number")
async def classify_number(number: str):
    try:
        num = int(number)
    except ValueError:
        return JSONResponse(
            status_code=400,
            content={"number": number, "error": True}
        )
    
    is_prime = check_prime(num)
    is_perfect = check_perfect(num)
    is_armstrong = check_armstrong(num)
    parity = "even" if num % 2 == 0 else "odd"
    digit_sum = sum_digits(num)
    fun_fact = await get_fun_fact(num)
    
    properties = []
    if is_armstrong:
        properties.append("armstrong")
    properties.append(parity)
    
    return {
        "number": num,
        "is_prime": is_prime,
        "is_perfect": is_perfect,
        "properties": properties,
        "digit_sum": digit_sum,
        "fun_fact": fun_fact
    }
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0")