# Network Route Optimization API

This project implements a REST API for managing network nodes and computing optimal routes between them based on latency.

## Features

- Add nodes
- Add edges between nodes
- Compute shortest path using Dijkstra's algorithm
- Store and retrieve route query history

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite

## Running the project

Install dependencies:

pip install -r requirements.txt

Run the server:

uvicorn app:app --reload

Open API documentation:

http://127.0.0.1:8000/docs