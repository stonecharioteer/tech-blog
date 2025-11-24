---
date: 2020-07-30T10:00:00+05:30
draft: false
title:
  "TIL: Docker Networking Deep Dive, Julia Evans' Systems Knowledge, and
  Kubernetes from the Ground Up"
description:
  "Today I learned about Docker graph drivers and container networking, Julia
  Evans' excellent systems programming explanations, and comprehensive
  Kubernetes architecture through Kamal Marhubi's ground-up approach."
tags:
  - til
  - docker
  - networking
  - kubernetes
  - containers
  - systems-programming
  - linux
---

Today's learning focused on container technologies, systems programming
concepts, and distributed systems architecture.

## Docker Networking and Graph Drivers

[Brutally Honest Guide to Docker Graph Drivers](https://blog.jessfraz.com/post/the-brutally-honest-guide-to-docker-graphdrivers/)
and
[Container Networking](https://docs.docker.com/config/containers/container-networking/)
provide deep insights into Docker's internal mechanisms:

### Docker Graph Drivers:

#### **Storage Driver Comparison:**

```bash
# Check current storage driver
docker info | grep "Storage Driver"

# Available drivers and characteristics:
# overlay2 (recommended): Copy-on-write, good performance
# aufs: Legacy, being phased out
# devicemapper: Block-level storage, complex configuration
# btrfs: Advanced filesystem features, snapshot support
# zfs: Enterprise features, high memory usage
```

#### **Overlay2 Driver Deep Dive:**

```bash
# Inspect layer structure
docker pull ubuntu:20.04
docker history ubuntu:20.04

# Examine overlay2 directory structure
sudo ls -la /var/lib/docker/overlay2/

# Layer composition
# Lower layers: read-only base layers
# Upper layer: read-write container changes
# Merged layer: unified view presented to container

# Example layer structure:
# /var/lib/docker/overlay2/
# ├── abc123...def/
# │   ├── diff/          # Layer changes
# │   ├── link           # Short identifier
# │   ├── lower          # Parent layers
# │   └── work/          # Temporary work directory
# └── l/                 # Symbolic links to layers
```

#### **Performance Implications:**

```dockerfile
# Inefficient: creates many layers
FROM ubuntu:20.04
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y git
RUN apt-get clean

# Efficient: fewer layers, better caching
FROM ubuntu:20.04
RUN apt-get update && \
    apt-get install -y \
        python3 \
        python3-pip \
        git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

### Docker Container Networking:

#### **Network Types:**

```bash
# List networks
docker network ls

# Default networks:
# bridge: Default network for containers
# host: Container uses host networking directly
# none: No networking
# Custom networks: User-defined bridge networks

# Create custom network
docker network create --driver bridge my-network
docker network create --driver bridge --subnet=172.20.0.0/16 my-subnet

# Inspect network configuration
docker network inspect bridge
docker network inspect my-network
```

#### **Bridge Network Deep Dive:**

```bash
# Default bridge network (docker0)
ip addr show docker0
brctl show docker0

# Container networking internals
docker run -d --name web nginx
docker exec web ip addr show
docker exec web ip route show

# Network namespace inspection
docker inspect web | grep NetworkMode
sudo nsenter -t $(docker inspect -f '{{.State.Pid}}' web) -n ip addr
```

#### **Custom Networking:**

```yaml
# docker-compose.yml with custom networks
version: "3.8"
services:
  web:
    image: nginx
    networks:
      - frontend
      - backend
    ports:
      - "80:80"

  app:
    image: python:3.9
    networks:
      - backend
      - database
    depends_on:
      - db

  db:
    image: postgres:13
    networks:
      - database
    environment:
      POSTGRES_PASSWORD: secret

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
  database:
    driver: bridge
    internal: true # No external access
```

#### **Container Communication:**

```bash
# Service discovery within custom networks
docker network create app-network
docker run -d --name db --network app-network postgres:13
docker run -d --name app --network app-network my-app:latest

# Containers can reach each other by name
# app container can connect to: db:5432
# No need for --link (deprecated)

# Port publishing vs exposure
docker run -p 8080:80 nginx    # Publish to host
docker run --expose 80 nginx   # Only expose to other containers
```

## Julia Evans' Systems Programming Insights

Julia Evans provides exceptional explanations of complex systems concepts:

### Networking Fundamentals:

#### **[Computer Networking Basics](https://jvns.ca/blog/2018/03/05/things-ive-learned-networking/):**

- **TCP vs UDP**: Reliability vs speed trade-offs
- **DNS resolution**: How domain names become IP addresses
- **HTTP request flow**: Complete journey from browser to server
- **Load balancing**: Distributing traffic across multiple servers

#### **[HTTP Request Routing](https://jvns.ca/blog/2016/07/14/whats-sni/):**

```
Client Request Flow:
1. DNS lookup: domain.com → IP address
2. TCP connection: Three-way handshake
3. TLS handshake: Certificate validation, encryption setup
4. HTTP request: Headers, body, method
5. Server processing: Route matching, business logic
6. HTTP response: Status code, headers, body
7. Connection handling: Keep-alive or close

SNI (Server Name Indication):
- Allows multiple HTTPS sites on same IP
- Client sends domain name during TLS handshake
- Server selects appropriate certificate
- Critical for shared hosting and CDNs
```

### Kubernetes Architecture Understanding:

#### **[Kubernetes Learning Journey](https://jvns.ca/blog/2017/06/04/learning-about-kubernetes/):**

- **Pods**: Basic deployment units, shared networking/storage
- **Services**: Stable network endpoints for dynamic pods
- **Deployments**: Declarative pod management and rolling updates
- **ConfigMaps/Secrets**: Configuration and sensitive data management

## Kubernetes from the Ground Up

[Kamal Marhubi's series](http://kamalmarhubi.com) provides deep architectural
understanding:

### Core Kubernetes Components:

#### **[The API Server](http://kamalmarhubi.com/blog/2015/09/06/kubernetes-from-the-ground-up-the-api-server/):**

```yaml
# API Server responsibilities:
# 1. RESTful API for all Kubernetes resources
# 2. Authentication and authorization
# 3. Admission control and validation
# 4. etcd storage interface
# 5. Resource change notifications

# Example API interaction
apiVersion: v1
kind: Pod
metadata:
  name: example-pod
  namespace: default
spec:
  containers:
    - name: web
      image: nginx:1.20
      ports:
        - containerPort: 80
      resources:
        limits:
          memory: "128Mi"
          cpu: "500m"
```

#### **[The Kubelet](http://kamalmarhubi.com/blog/2015/08/27/what-even-is-a-kubelet/):**

```bash
# Kubelet responsibilities:
# 1. Watch API server for pod assignments
# 2. Manage container lifecycle (start, stop, restart)
# 3. Health checking and reporting
# 4. Resource monitoring and management
# 5. Volume mounting and networking setup

# Kubelet configuration
sudo systemctl status kubelet
sudo journalctl -u kubelet -f

# Pod lifecycle management
# kubelet receives pod spec from API server
# Downloads container images
# Creates container runtime (containerd/docker)
# Sets up networking (CNI plugins)
# Mounts volumes
# Starts containers
# Monitors health and reports status
```

#### **[The Scheduler](http://kamalmarhubi.com/blog/2015/11/17/kubernetes-from-the-ground-up-the-scheduler/):**

```go
// Simplified scheduler algorithm
func Schedule(pod *Pod, nodes []Node) *Node {
    // 1. Filter nodes (predicates)
    feasibleNodes := []Node{}
    for _, node := range nodes {
        if canSchedule(pod, node) {
            feasibleNodes = append(feasibleNodes, node)
        }
    }

    // 2. Score nodes (priorities)
    scoredNodes := make(map[Node]int)
    for _, node := range feasibleNodes {
        score := calculateScore(pod, node)
        scoredNodes[node] = score
    }

    // 3. Select highest scoring node
    bestNode := selectBestNode(scoredNodes)
    return bestNode
}

func canSchedule(pod *Pod, node *Node) bool {
    // Resource constraints
    if node.AvailableCPU < pod.RequestedCPU {
        return false
    }
    if node.AvailableMemory < pod.RequestedMemory {
        return false
    }

    // Node selectors
    if !nodeMatchesSelectors(node, pod.NodeSelector) {
        return false
    }

    // Taints and tolerations
    if !podToleratesNodeTaints(pod, node.Taints) {
        return false
    }

    return true
}
```

### Advanced Kubernetes Concepts:

#### **Networking Model:**

```yaml
# CNI (Container Network Interface) plugins
# Provide pod-to-pod networking across nodes

# Example: Calico network policy
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: web-netpol
spec:
  podSelector:
    matchLabels:
      app: web
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: frontend
      ports:
        - protocol: TCP
          port: 80
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: database
      ports:
        - protocol: TCP
          port: 5432
```

#### **Storage and Persistence:**

```yaml
# Persistent Volume and Claims
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-example
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  hostPath:
    path: /data/pv-example

---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-example
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
```

### Everything is a File Philosophy:

The Unix principle that
[everything is a file](https://www.tecmint.com/explanation-of-everything-is-a-file-and-types-of-files-in-linux/)
extends to container technologies:

```bash
# Container processes visible in host /proc
docker run -d --name test nginx
docker exec test ps aux

# Container networking through Linux primitives
ip netns list
docker exec test cat /proc/net/tcp

# Container storage as filesystem layers
ls -la /var/lib/docker/overlay2/
mount | grep overlay

# Socket communication
stat /var/run/docker.sock  # Docker daemon socket
file /var/run/docker.sock  # Shows socket type
```

These concepts form the foundation for understanding modern containerized and
orchestrated systems, from basic Docker networking to sophisticated Kubernetes
cluster management.
