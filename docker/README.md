# Homework Project: Docker and Kubernetes Deployment (Advanced)

This project extends a basic Flask application into a more capable service with multiple routes, containerized with Docker and deployed to a local Kubernetes cluster via Rancher Desktop.

## Project Structure

```
homework_complex/
├─ app.py
├─ requirements.txt
├─ Dockerfile
└─ k8s/
   ├─ deployment.yaml
   └─ service.yaml
```

## Prerequisites

- Rancher Desktop with either dockerd (Moby) or containerd runtime
- Docker or nerdctl (matching your runtime)
- kubectl configured to use the Rancher Desktop Kubernetes cluster
- Python 3.11+ (optional for local testing)

## Application Overview

The service exposes several routes for demonstration and testing:

- `GET /` – simple text response
- `GET /health` – health probe with current UTC time
- `GET /time` – returns the server UTC time
- `GET /greet/<name>` – personalized greeting
- `GET /echo?msg=...` – echoes a query parameter
- `POST /compute/sum` – accepts JSON `{"numbers":[...]}` and returns their sum
- `POST /items` – create an item in an in-memory store. JSON body must include `id` and `name`
- `GET /items/<id>` – read an item by id
- `DELETE /items/<id>` – delete an item
- `GET /metrics` – minimal metrics: total requests and item count

### Example Requests

```bash
curl -s http://localhost:8000/
curl -s http://localhost:8000/health
curl -s http://localhost:8000/time
curl -s http://localhost:8000/greet/Ada
curl -s "http://localhost:8000/echo?msg=hello"
curl -s -X POST http://localhost:8000/compute/sum -H "Content-Type: application/json" -d '{"numbers":[1,2,3,4.5]}'
curl -s -X POST http://localhost:8000/items -H "Content-Type: application/json" -d '{"id":"42","name":"demo"}'
curl -s http://localhost:8000/items/42
curl -i -X DELETE http://localhost:8000/items/42
curl -s http://localhost:8000/metrics
```

## Build and Run with Docker (or nerdctl)

```bash
# Build an updated image tag
docker build -t hello-flask:2.0 .

# Run the container
docker run -d --name hello-flask -p 8000:8000 hello-flask:2.0

# Verify locally
curl -s http://localhost:8000/health
```

If your Rancher Desktop uses containerd, use `nerdctl` instead of `docker` in the commands above.

## Kubernetes Deployment

The manifests in `k8s/` deploy the service and expose it via a ClusterIP Service.

```bash
kubectl create namespace hw || true
kubectl -n hw apply -f k8s/deployment.yaml
kubectl -n hw apply -f k8s/service.yaml
kubectl -n hw rollout status deploy/hello-flask
kubectl -n hw get pods,svc
```

### Access via Port-Forward (per assignment requirement)

```bash
kubectl -n hw port-forward service/hello-flask 8000:80
# New terminal:
curl -s http://localhost:8000/health
```

## Image Availability Notes

- With dockerd (Moby), Kubernetes can usually see images built locally with Docker when imagePullPolicy is `IfNotPresent`.
- With containerd, either build the image using `nerdctl`, or push the image to a registry (e.g., Docker Hub) and update the `image:` in `deployment.yaml`.

## Success Criteria

- Local container responds to the sample requests above.
- Kubernetes Deployment becomes Ready and the Service responds via port-forwarding.

## Contributor
dan-teodor.buzoianu@endava.com