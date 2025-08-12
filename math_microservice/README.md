# Math Microservice

This project is a mathematical computation microservice built using the Flask web framework and designed following modern software architecture principles such as microservice isolation, asynchronous task handling, and clean separation of concerns.

The microservice exposes a RESTful API and a minimal web interface for performing three essential types of computations:

- Exponentiation (pow)
- Fibonacci sequence number lookup
- Factorial calculation

Each of these operations is executed in the background using a thread-based task queue, allowing the service to remain responsive and scalable while still returning real-time feedback to the user.

All requests are:
- Validated using Pydantic to ensure clean and predictable data input
- Persisted to an SQLite database using SQLAlchemy
- Logged to a Kafka topic for stream processing
- Processed in a decoupled worker that runs in parallel using Python’s threading module and queue.Queue
- Displayed in a simple form-based web UI

This project is ideal for learning production-style Flask applications, asynchronous task handling, Kafka-based messaging, and microservice design patterns.

## Features

- REST API with Flask
- HTML frontend interface
- Thread-based background task queue
- SQLite persistence layer
- Kafka producer for request streaming
- Pydantic for request validation
- Modular codebase with MVC structure

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Start Kafka and Zookeeper (Docker Compose)

```bash
docker-compose up -d
```

Kafka will be available on localhost:9092.

### 3. Run the microservice

```bash
python main.py
```

Then open your browser at:

```
http://localhost:5000
```

Use the UI to compute power, Fibonacci, or factorial operations. The result will be shown in the browser, logged to the database, and also streamed to Kafka.

### 4. Run the Kafka consumer (optional)

To see live-streamed logs of the operations:

```bash
python kafka_consumer.py
```

This will consume and print messages from the math_operations topic.

## Project Structure

```
math_microservice/
├── app/
│   ├── api/v1/routes.py            # REST API endpoints
│   ├── core/services.py            # Math logic
│   ├── models/operation.py         # SQLAlchemy models
│   ├── schemas/operation.py        # Pydantic schemas
│   ├── utils/request_logger.py     # DB + Kafka logging
│   ├── messaging/kafka_producer.py # Kafka producer
│   ├── extensions.py               # DB and caching
│   └── worker.py                   # Threaded task queue
├── templates/                      # HTML templates
├── kafka_consumer.py               # Kafka consumer script
├── main.py                         # App entry point
├── requirements.txt
└── docker-compose.yml
```

## Contributors

Dan Buzoianu - dan-teodor.buzoianu@endava.com
