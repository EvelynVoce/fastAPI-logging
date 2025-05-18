from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import uuid
import time
from log_config import info_logger, error_logger
import traceback
from pyinstrument import Profiler

app = FastAPI()


@app.middleware("http")
async def profile_request(request: Request, call_next):
    profiler = Profiler()
    profiler.start()

    response = await call_next(request)

    profiler.stop()
    print(profiler.output_text(unicode=True, color=True))

    return response


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Generate or retrieve correlation ID
        correlation_id = str(uuid.uuid4())
        request.state.correlation_id = correlation_id

        # Record start time for response time calculation
        start_time = time.time()
        request.state.start_time = start_time

        # Log the incoming request
        info_logger.info({
            "correlation_id": correlation_id,
            "request": {
                "method": request.method,
                "url": str(request.url)
            }
        })
        response = await call_next(request)

        # Calculate the response time
        response_time = time.time() - start_time

        # Log the outgoing response
        info_logger.info({
            "correlation_id": correlation_id,
            "response": {
                "status_code": response.status_code,
                "response_time": round(response_time, 4)  # Round to 4 decimal places
            }
        })

        return response


app.add_middleware(LoggingMiddleware)


# Custom exception handler for unhandled exceptions
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    stack_trace = traceback.format_exc()

    # Prepare error details
    error_details = {
        "correlation_id": request.state.correlation_id,
        "response_time": time.time() - request.state.start_time,
        "error": str(exc),  # The error message from the Exception
        "message": "Unhandled Exception",  # Custom message
        "stack_trace": stack_trace  # Include the stack trace in the logs
    }
    error_logger.error(error_details)  # Log using error_logger, not info_logger

    # Return a consistent error response
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again later."}
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: Exception):
    stack_trace = traceback.format_exc()

    # Prepare error details
    error_details = {
        "correlation_id": request.state.correlation_id,
        "response_time": time.time() - request.state.start_time,
        "error": str(exc),  # The error message from the Exception
        "message": "HTTPException Raised",  # Custom message
        "stack_trace": stack_trace  # Include the stack trace in the logs
    }
    error_logger.error(error_details)  # Log using error_logger, not info_logger

    # Return a consistent error response
    return JSONResponse(
        status_code=500,
        content={"detail": "An HTTP Exception was raised."}
    )


@app.get("/hello")
async def hello(request: Request):
    return {"message": "Hello World", "correlation_id": request.state.correlation_id}


@app.get("/error")
async def error(request: Request):
    _ = 1 / 0  # Force an error to test logging
    return {"message": "This won't be reached", "correlation_id": request.state.correlation_id}


@app.get("/bounding")
async def error(request: Request):
    example = [0, 1, 2, 3]
    for i in range(10):
        example[i]
    return example[i]


@app.get("/http-exception")
async def http(request: Request):
    raise HTTPException(status_code=404, detail="Item not found")


@app.get("/value")
async def http(request: Request):
    raise ValueError("Value is wrong")
