# Math Microservice

This project is a mathematical computation microservice built using the Flask web framework and designed following modern software architecture principles such as microservice isolation, asynchronous task handling, and clean separation of concerns.

The microservice exposes a RESTful API and a minimal web interface for performing three essential types of computations:

Exponentiation (pow)

Fibonacci sequence number lookup

Factorial calculation

Each of these operations is executed in the background using a thread-based task queue, allowing the service to remain responsive and scalable while still returning real-time feedback to the user.

All requests are:

Validated using Pydantic to ensure clean and predictable data input

Persisted to an SQLite database using SQLAlchemy

Processed in a decoupled worker that runs in parallel using Python’s threading module and queue.Queue

Logged for visibility, diagnostics, and potential observability tooling in the future

This project can serve as a solid starting point for:

Learning how to build production-style Flask applications

Designing and scaling simple asynchronous workflows

Rapid prototyping of microservices that can later be containerized, extended with Celery or message brokers, or integrated into a larger system

The codebase is intentionally kept lightweight, readable, and extensible to suit both learning and real-world application needs.

## Features

- REST API built with Flask  
- HTML frontend (form-based interface)  
- Input validation using Pydantic  
- Task processing with Python threads  
- SQLite database persistence  
- Logging for visibility and debugging  

## How to Run

Make sure you have Python 3.9+ installed.

Then run the application:

```bash
python main.py
```

Once running, open your browser and navigate to:

```
http://localhost:5000
```

There you can:
- Select a math operation
- Enter the required inputs
- Click **Compute** and see the result appear on the page

## 📁 Project Structure

```
math_microservice/
├── app/
│   ├── api/v1/routes.py        # API endpoints
│   ├── core/services.py        # Math logic
│   ├── models/operation.py     # SQLAlchemy models
│   ├── schemas/operation.py    # Pydantic schemas
│   ├── utils/helpers.py        # Save/log requests
│   ├── extensions.py           # DB/cache
│   └── worker.py               # Threading + queue
├── templates/                  # HTML frontend
├── static/                     # CSS/JS (if any)
├── main.py                     # Entry point
├── requirements.txt
└── README.md
```

## Contributors

Dan Buzoianu - dan-teodor.buzoianu@endava.com
