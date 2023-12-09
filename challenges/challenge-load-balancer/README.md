# The Challenge - Building a Load Balancer

**A load balancer performs the following functions:**
- Distributes client requests/network load efficiently across multiple servers
- Ensures high availability and reliability by sending requests only to servers that are online
- Provides the flexibility to add or subtract servers as demand dictates
- Therefore our goals for this project are to:

**Build a load balancer that can send traffic to two or more servers.**
- Health check the servers.
- Handle a server going offline (failing a health check).
- Handle a server coming back online (passing a health check).

## Requirements
- [Docker Desktop](https://docs.docker.com/desktop/)/[Docker Engine](https://docs.docker.com/engine/)
- [Docker Compose](https://docs.docker.com/compose/)

## Setup
- Install Docker Desktop/Docker Engine and Docker Compose.
- Start Load Balancer and Servers.

  ```sh
  docker compose up
  ```

## Examples

```sh
$ curl http://localhost:8000
Hello there! I am Server 1

$ curl http://localhost:8000
Hello there! I am Server 2
```

## Docker Compose Logs

```sh
[SERVER-2] Server started ...
[SERVER-2] Listening on port 8000
[SERVER-1] Server started ...
[SERVER-1] Listening on port 8000
[LB] Load balancer started ...
172.28.0.4 - - [09/Dec/2023 16:45:29] "GET http://server-2:8000/ HTTP/1.1" 200 - 
172.28.0.1 - - [09/Dec/2023 16:45:29] "GET / HTTP/1.1" 200 -
[LB] Received request
[LB] Routing request to server 1
172.28.0.4 - - [09/Dec/2023 16:45:31] "GET http://server-1:8000/ HTTP/1.1" 200 - 
[SERVER-1] Received request
172.28.0.1 - - [09/Dec/2023 16:45:31] "GET / HTTP/1.1" 200 -
[LB] Received request
[LB] Routing request to server 2
172.28.0.1 - - [09/Dec/2023 16:47:18] "GET / HTTP/1.1" 200 -
[SERVER-2] Received request
172.28.0.4 - - [09/Dec/2023 16:47:18] "GET http://server-2:8000/ HTTP/1.1" 200 -
```
