---
date: 2020-09-15T10:00:00+05:30
draft: false
title: "Building Single Page Applications in React using Dash and Python"
description: "How to build Single Page web applications without any Javascript using Dash, a Python library that generates React components."
tags:
  - python
  - react
  - dash
  - flask
  - plotly
  - tutorial
  - web-development
url: "dash-spa"
---

The `dash` library from Plotly allows you to build webpages that internally serve React components. Let's see how to use this to build a SPA with authentication, multiple pages and **zero** Javascript.

## Introduction

Dash is a Python library from Plotly that helps you take graphs that are generated using Plotly and then convert them into a web page.

In simple terms, Dash does just this. However, what Dash does internally is take your Python objects that define your views and convert them into React components. This is a powerful way of building React applications without having to write your own React code.

Dash also uses Flask internally, converting all your function calls into Flask API calls. This makes it easy to decouple the application and build a full stack application purely in Python.

Note that by saying we are writing Python for the UI, I don't mean that we are using WASM. This approach has nothing to do with Web Assembly. Instead, it is a simpler way to just take Python code and generate Javascript.

## Prerequisites

To understand this article, you should have an understanding of the following items.

1. **Python**: Learn how decorators work, how to write class definition and how methods are called.
2. **Flask**: Go through a good tutorial on flask. You will need to understand blueprints, the Application factory method approach, and MethodViews.
3. **Plotly**: Some minor understanding of the Plotly library is required.
4. **HTML and CSS**: While JS is not required to build your own Dash apps, I'd recommend getting to learn as much HTML and CSS as you can since that will help you polish your application.

Resources for all these can be found at the end of this article.

## Setup and Installation

Get the source code for this repository. Make sure you get all the tags.

```bash
git clone https://github.com/stonecharioteer/dash-spa
cd dash-spa
git fetch --all --tags --prune
```

Then, checkout the first version of this application.

```bash
git checkout v0.1
```

First, as you always should, make a virtual environment using a Python 3 (I use 3.8).

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Running the Application

This application uses `gunicorn` for deployment. I have provided a sample `wsgi.py` file for use with `gunicorn`. So go ahead and use it.

```bash
gunicorn -w 6 -b 0.0.0.0:10000 wsgi:app
```

Navigate to `http://localhost:10000` to see your application running.

## Structure of the Application

This application is broken into two portions. The first portion is the Flask application, while the other portion is the Dash application. Dash builds up an application *above* a Flask app by default. However, it can be explicitly attached to a Flask application.

I personally recommend the latter method as it provides better control over the application structure.

### Flask Structure

The Flask application follows the standard application factory pattern:

```python
# app/__init__.py
from flask import Flask
from dash import Dash

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    from .dash_app import create_dash_app
    create_dash_app(app)
    
    # Register blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app
```

The Flask app handles:
- Authentication and session management
- API endpoints for data processing
- Static file serving
- Configuration management

### Dash Structure

The Dash application is created as a separate module that gets attached to the Flask app:

```python
# app/dash_app.py
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

def create_dash_app(flask_app):
    dash_app = dash.Dash(
        __name__,
        server=flask_app,
        url_base_pathname='/dashboard/',
        external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css']
    )
    
    # Define the layout
    dash_app.layout = html.Div([
        html.H1("My Dashboard"),
        dcc.Graph(id='example-graph'),
        dcc.Dropdown(
            id='dropdown',
            options=[
                {'label': 'Option 1', 'value': 'opt1'},
                {'label': 'Option 2', 'value': 'opt2'}
            ],
            value='opt1'
        )
    ])
    
    # Define callbacks
    @dash_app.callback(
        Output('example-graph', 'figure'),
        Input('dropdown', 'value')
    )
    def update_graph(selected_value):
        # Your data processing logic here
        df = get_data_based_on_selection(selected_value)
        fig = px.bar(df, x='category', y='value')
        return fig
    
    return dash_app

def get_data_based_on_selection(selection):
    # Mock data function
    return pd.DataFrame({
        'category': ['A', 'B', 'C'],
        'value': [1, 2, 3] if selection == 'opt1' else [3, 2, 1]
    })
```

## Testing the Application

### Testing the Utilities

For utility functions, use standard unit tests:

```python
# tests/test_utils.py
import unittest
from app.utils import process_data

class TestUtils(unittest.TestCase):
    def test_process_data(self):
        input_data = {'key': 'value'}
        result = process_data(input_data)
        self.assertEqual(result['processed'], True)
```

### Testing the Flask API

Test Flask routes using the Flask test client:

```python
# tests/test_flask_routes.py
import unittest
from app import create_app

class TestFlaskRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
    
    def tearDown(self):
        self.ctx.pop()
    
    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
```

### Testing the Dash UI with Selenium

For end-to-end testing of Dash components, use Selenium:

```python
# tests/test_dash_ui.py
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import time
from app import create_app

class TestDashUI(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.server_thread = threading.Thread(
            target=self.app.run,
            kwargs={'port': 8050, 'debug': False}
        )
        self.server_thread.daemon = True
        self.server_thread.start()
        time.sleep(2)  # Wait for server to start
        
        self.driver = webdriver.Chrome()  # or webdriver.Firefox()
    
    def tearDown(self):
        self.driver.quit()
    
    def test_dashboard_loads(self):
        self.driver.get('http://localhost:8050/dashboard/')
        
        # Wait for the page to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "example-graph"))
        )
        
        # Test dropdown interaction
        dropdown = self.driver.find_element(By.ID, "dropdown")
        dropdown.click()
        
        # Verify graph updates
        graph = self.driver.find_element(By.ID, "example-graph")
        self.assertTrue(graph.is_displayed())
```

#### Note on User Acceptance Tests

User Acceptance Tests (UATs) for Dash applications should focus on:
- Component interactions work as expected
- Data visualizations render correctly
- Responsive design works across devices
- Performance under various data loads

## Dash Callbacks

Callbacks are the heart of Dash interactivity. They define how components communicate:

```python
# Advanced callback example
@dash_app.callback(
    [Output('graph-1', 'figure'),
     Output('graph-2', 'figure'),
     Output('status-text', 'children')],
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date'),
     Input('filter-dropdown', 'value')],
    [State('user-input', 'value')]
)
def update_dashboard(start_date, end_date, filter_value, user_input):
    # Process inputs
    filtered_data = filter_data(start_date, end_date, filter_value)
    
    # Create visualizations
    fig1 = create_time_series(filtered_data)
    fig2 = create_distribution(filtered_data)
    
    # Update status
    status = f"Showing data from {start_date} to {end_date}"
    
    return fig1, fig2, status

def filter_data(start_date, end_date, filter_value):
    # Your data filtering logic
    pass

def create_time_series(data):
    # Create time series visualization
    pass

def create_distribution(data):
    # Create distribution visualization
    pass
```

{{< tip title="Callback Best Practices" >}}
- Keep callbacks focused on single responsibilities
- Use State for values that shouldn't trigger callbacks
- Implement error handling for data processing
- Consider performance implications for large datasets
{{< /tip >}}

## Deployment

### Using `systemctl` and `gunicorn`

Create a systemd service file:

```ini
# /etc/systemd/system/dash-spa.service
[Unit]
Description=Dash SPA Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/app
Environment=PATH=/path/to/your/app/env/bin
ExecStart=/path/to/your/app/env/bin/gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable dash-spa
sudo systemctl start dash-spa
```

### Using Docker

Create a Dockerfile:

```dockerfile
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "wsgi:app"]
```

Build and run:

```bash
docker build -t dash-spa .
docker run -p 8000:8000 dash-spa
```

#### Using `docker-compose`

Create a `docker-compose.yml`:

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - FLASK_ENV=production
    volumes:
      - ./data:/app/data
    depends_on:
      - redis
      - postgres

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: dashapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

### Using Kubernetes

Create Kubernetes manifests:

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dash-spa
spec:
  replicas: 3
  selector:
    matchLabels:
      app: dash-spa
  template:
    metadata:
      labels:
        app: dash-spa
    spec:
      containers:
      - name: dash-spa
        image: your-registry/dash-spa:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database-url

---
apiVersion: v1
kind: Service
metadata:
  name: dash-spa-service
spec:
  selector:
    app: dash-spa
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

Deploy to Kubernetes:

```bash
kubectl apply -f deployment.yaml
```

#### Pushing Updates to Settings

For configuration updates without downtime:

```bash
kubectl create configmap app-config --from-file=config.py
kubectl rollout restart deployment/dash-spa
```

## Using the Cookiecutter Template

To streamline future projects, create a cookiecutter template:

```bash
cookiecutter https://github.com/stonecharioteer/cookiecutter-dash-spa
```

This will generate a new project with:
- Proper Flask application factory structure
- Dash integration setup
- Testing framework configured
- Docker configuration
- CI/CD pipeline templates

## Advanced Features

### Authentication Integration

```python
from flask_login import LoginManager, login_required

def create_dash_app(flask_app):
    # Protect Dash routes with authentication
    for view_func in flask_app.server.view_functions:
        if view_func.startswith('/dashboard/'):
            flask_app.server.view_functions[view_func] = login_required(
                flask_app.server.view_functions[view_func]
            )
```

### Real-time Updates

```python
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from collections import deque
import random

# For real-time data updates
@dash_app.callback(
    Output('live-graph', 'figure'),
    Input('graph-update', 'n_intervals')
)
def update_graph_live(n):
    # Simulate real-time data
    global data_queue
    data_queue.append(random.randint(1, 100))
    
    if len(data_queue) > 50:
        data_queue.popleft()
    
    trace = go.Scatter(
        y=list(data_queue),
        mode='lines+markers'
    )
    
    return {'data': [trace], 'layout': go.Layout(xaxis=dict(range=[0, 50]))}
```

## Performance Optimization

### Caching

```python
from flask_caching import Cache

cache = Cache()

@cache.memoize(timeout=300)  # Cache for 5 minutes
def expensive_computation(params):
    # Your expensive computation here
    pass
```

### Asynchronous Processing

```python
from celery import Celery

celery = Celery('dash-spa')

@celery.task
def process_large_dataset(data_id):
    # Process data in background
    pass

# In your callback
@dash_app.callback(...)
def trigger_processing(n_clicks):
    if n_clicks:
        process_large_dataset.delay(data_id)
        return "Processing started..."
```

## End Note

Building SPAs with Dash and Python offers a unique approach to web development that leverages Python's data science ecosystem while providing modern web interfaces. This approach is particularly powerful for:

- Data-heavy applications
- Scientific computing interfaces  
- Business intelligence dashboards
- Rapid prototyping of analytical tools

The combination of Flask's flexibility and Dash's component-based architecture creates a robust foundation for scalable web applications without requiring deep JavaScript expertise.

{{< warning title="Consider Your Use Case" >}}
While Dash is powerful, consider traditional web frameworks for applications that require heavy DOM manipulation, complex user interactions, or when you need maximum performance for client-side operations.
{{< /warning >}}

## References

1. [Python 101: Classes](https://python101.pythonlibrary.org/chapter11_classes.html)
2. [Python 101: Decorators](https://python101.pythonlibrary.org/chapter25_decorators.html?highlight=decorator)
3. [Real Python Article on Decorators](https://realpython.com/primer-on-python-decorators/)
4. [Real Python article on Virtual Environments](https://realpython.com/python-virtual-environments-a-primer/)
5. [Miguel Grinberg's Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
6. [Explore Flask](https://exploreflask.com/en/latest/)
7. [Flask `create_app` example](https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/)
8. [Plotly Documentation](https://plotly.com/python/)
9. [Dash documentation](https://dash.plotly.com/)
10. [Pytest Documentation](https://docs.pytest.org/en/latest/contents.html)
11. [Gunicorn Documentation](https://gunicorn.org/)
12. [How to write a `systemctl` file](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-centos-7)
13. [Docker tutorial](https://docs.docker.com/)
14. [Docker Flask tutorial](https://github.com/docker/labs/tree/master/beginner/flask-app)
15. [Docker Compose tutorial](https://docs.docker.com/compose/)
16. [k3s documentation](https://k3s.io/)
17. [Flask on k8s](https://testdriven.io/blog/running-flask-on-kubernetes/)
18. [Dash Enterprise](https://plotly.com/dash/) - For production deployments
19. [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/) - For better styling
20. [Plotly Community Forum](https://community.plotly.com/) - For community support