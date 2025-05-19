# Distributed Key-Value Store with Replication and Sharding

A scalable, fault-tolerant distributed key-value store implemented in Python. This project demonstrates a distributed system with sharding, replication, and routing to handle key-value operations across multiple nodes.
<br/>
<div align="center"><img src="https://github.com/user-attachments/assets/8f59ceae-6420-4726-899d-24d6d064a73c" width=720>

[Image Source](https://medium.com/@shivajiofficial5088/sharding-partitioning-and-replication-often-confused-concepts-of-system-design-%EF%B8%8F-e99c523791e8)
</div>

## Features

- **Sharding**: Distributes keys across multiple shards to optimize performance and scalability.
- **Replication**: Supports leader-follower replication for fault tolerance and high availability.
- **HTTP API**: Provides RESTful endpoints for `GET`, `PUT` and `DELETE` operations.
- **Routing**: A router service directs requests to the appropriate shard based on key hashing.
- **Load Testing**: Validation with Locust to check for high throughput.
- **Dockerized**: Containerized setup using Docker Compose for easy deployment.

## Architecture

The system consists of:

- **Router**: Receives client requests and routes them to the appropriate shard based on a consistent hashing mechanism.
- **Shards**: Each shard is a pair of nodes (leader and follower) handling a subset of the key space.
  - **Leader**: Processes read and write requests, replicates changes to the follower.
  - **Follower**: Maintains a replica of the leader’s data.
- **Locust**: A load-testing tool to simulate thousands of concurrent users and measure system performance.

The system uses three shards (`shard0`, `shard1`, `shard2`), each with a leader and follower, communicating over HTTP.

## Prerequisites

- **Docker** and **Docker Compose**: For running the services.
- **Python**: For local development or running tests.
- **Locust**: For load testing (installed in the Locust container).

## Setup

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/kmAyush/distributed-kv.git
   cd distributed-kv
   ```

2. **Directory Structure**:

   ```
   .
   ├── Dockerfile           # Dockerfile for shards and router
   ├── Dockerfile.locust    # Dockerfile for Locust
   ├── docker-compose.yml   # Docker Compose configuration
   ├── locustfile.py        # Locust script for load testing
   ├── shard.py             # Shard server implementation
   ├── router.py            # Router implementation
   ├── requirements.txt     # Python dependencies
   ```

3. **Build and Run**: Start all services (router, shards, and Locust) using Docker Compose:

   ```bash
   docker-compose up --build
   ```

   - This starts:
     - Router on `http://localhost:5000`
     - Shard leaders on ports `5001`, `5002`, `5003`
     - Shard followers on ports `6001`, `6002`, `6003`
     - Locust web interface on `http://localhost:8089`

## Usage

### Interacting with the Key-Value Store

The router exposes the following HTTP endpoints:

- **PUT /put**: Set a key-value pair.

  ```bash
  curl -X POST http://localhost:5000/put \
       -H "Content-Type: application/json" \
       -d '{"key": "sample_key", "value": "sample_value"}'
  ```
- **GET /get/**: Retrieve the value for a key.

  ```bash
  curl http://localhost:5000/get?key=sample_key
  ```
- **DELETE /delete/**: Delete the key-value pair.

  ```bash
  curl http://localhost:5000/delete?key=sample_key
  ```
### Load Testing with Locust

1. Open the Locust web interface at `http://localhost:8089`.
2. Configure the test:
   - **Number of users**: Start with 100.
   - **Spawn rate**: 10 users/second.
   - **Host**: `http://router:5000` (pre-configured).
3. Click **Run** to begin the test.
4. Monitor:
   - **Requests/second (RPS)**
   - **Response times**
   - **Failure rate**

Note : Wait time in locustfile is set to 1-3 seconds, reduce to optimize RPS.


## Acknowledgments
- To understand the basics of distributed database system. 
- Built with Python, Flask, and Docker.
- Load testing powered by Locust.
