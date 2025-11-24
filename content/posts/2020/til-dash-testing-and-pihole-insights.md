---
date: 2020-07-24T18:00:00+05:30
draft: false
title: "TIL: Dash Application Testing and Pi-hole DNS Architecture"
description:
  "Today I learned about testing Dash applications with pytest and selenium,
  implementing Flask-Dash integration patterns, and understanding Pi-hole's FTL
  engine based on dnsmasq."
tags:
  - til
  - dash
  - plotly
  - testing
  - pytest
  - selenium
  - pihole
  - dns
  - dnsmasq
  - argparse
---

Today I explored advanced testing strategies for Dash applications and gained
deeper insights into Pi-hole's DNS blocking architecture, along with discovering
useful Python argparse features.

## Dash Application Testing

### Testing with Pytest and Selenium

[Testing Dash Applications using Pytest and Selenium](https://dash.plotly.com/testing)
provides comprehensive testing strategies for interactive web applications:

```python
# test_dash_app.py - Complete Dash testing example
import pytest
import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Sample Dash application for testing
def create_test_app():
    """Create a simple Dash app for testing"""
    df = px.data.iris()

    app = dash.Dash(__name__)

    app.layout = html.Div([
        html.H1("Iris Dataset Dashboard", id="title"),

        dcc.Dropdown(
            id="species-dropdown",
            options=[{'label': species, 'value': species}
                    for species in df['species'].unique()],
            value=df['species'].unique()[0],
            clearable=False
        ),

        dcc.Graph(id="scatter-plot"),

        html.Div(id="stats-display"),

        dcc.Interval(
            id="interval-component",
            interval=1000,  # Update every second
            n_intervals=0,
            disabled=True
        )
    ])

    @callback(
        [Output("scatter-plot", "figure"),
         Output("stats-display", "children")],
        [Input("species-dropdown", "value")]
    )
    def update_plots(selected_species):
        filtered_df = df[df['species'] == selected_species]

        fig = px.scatter(
            filtered_df,
            x="sepal_width",
            y="sepal_length",
            color="petal_length",
            title=f"Scatter plot for {selected_species}"
        )

        stats = html.Div([
            html.P(f"Selected species: {selected_species}"),
            html.P(f"Number of samples: {len(filtered_df)}"),
            html.P(f"Average sepal length: {filtered_df['sepal_length'].mean():.2f}")
        ])

        return fig, stats

    return app

# Pytest fixtures for Dash testing
@pytest.fixture
def dash_app():
    """Create Dash app for testing"""
    return create_test_app()

@pytest.fixture
def dash_duo(dash_app):
    """Create DashDuo test fixture"""
    from dash.testing.application_runners import import_app
    from dash.testing.composite import DashComposite

    # Note: In real tests, you'd use dash.testing.composite.DashComposite
    # This is a simplified version for demonstration
    class MockDashDuo:
        def __init__(self, app):
            self.app = app
            self.driver = None

        def start_server(self, app):
            # In real implementation, this starts the server
            pass

        def wait_for_element(self, selector, timeout=10):
            # Mock implementation
            pass

    return MockDashDuo(dash_app)

# Basic functionality tests
def test_app_creation(dash_app):
    """Test that the app is created properly"""
    assert dash_app is not None
    assert dash_app.layout is not None

def test_callback_registration(dash_app):
    """Test that callbacks are registered"""
    assert len(dash_app.callback_map) > 0

# Integration tests with Selenium
class TestDashInteraction:
    """Integration tests for Dash application"""

    @pytest.fixture(autouse=True)
    def setup_driver(self):
        """Setup Chrome driver for testing"""
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Run in headless mode
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)

        yield

        self.driver.quit()

    def test_dropdown_interaction(self, dash_app):
        """Test dropdown interaction updates the plot"""
        # Start the Dash server (simplified)
        # In real tests, you'd use dash.testing framework

        # Navigate to the application
        self.driver.get("http://localhost:8050")

        # Wait for the page to load
        title = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "title"))
        )
        assert "Iris Dataset Dashboard" in title.text

        # Find and interact with dropdown
        dropdown = self.driver.find_element(By.CSS_SELECTOR,
                                          "#species-dropdown .Select-value")
        dropdown.click()

        # Select a different species
        option = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                "//div[text()='versicolor']"))
        )
        option.click()

        # Wait for the plot to update
        time.sleep(2)

        # Verify the stats display updated
        stats = self.driver.find_element(By.ID, "stats-display")
        assert "versicolor" in stats.text

    def test_plot_rendering(self, dash_app):
        """Test that plots render correctly"""
        self.driver.get("http://localhost:8050")

        # Wait for plot to load
        plot = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                          ".plotly-graph-div"))
        )

        # Check that plot has data
        assert plot.is_displayed()

        # Check for plot traces (data points)
        traces = self.driver.find_elements(By.CSS_SELECTOR,
                                         ".scatterlayer .trace")
        assert len(traces) > 0

# Performance tests
def test_callback_performance(dash_app):
    """Test callback execution performance"""
    import time

    # Get the callback function
    callback_id = list(dash_app.callback_map.keys())[0]
    callback_func = dash_app.callback_map[callback_id]['callback']

    # Measure execution time
    start_time = time.time()
    result = callback_func.func('setosa')  # Test with sample input
    execution_time = time.time() - start_time

    # Assert reasonable performance (< 100ms)
    assert execution_time < 0.1
    assert result is not None

# Mock external dependencies for testing
@pytest.fixture
def mock_data():
    """Mock data for testing without external dependencies"""
    return pd.DataFrame({
        'species': ['setosa', 'versicolor', 'virginica'] * 10,
        'sepal_length': [5.1, 4.9, 4.7] * 10,
        'sepal_width': [3.5, 3.0, 3.2] * 10,
        'petal_length': [1.4, 1.4, 1.3] * 10,
        'petal_width': [0.2, 0.2, 0.2] * 10
    })
```

### Flask-Dash Integration Testing

```python
# Flask-Dash integration patterns and testing
from flask import Flask
import dash
from dash import dcc, html
from werkzeug.middleware.dispatcher import DispatcherMiddleware

def create_flask_dash_app():
    """Create integrated Flask-Dash application"""
    # Main Flask application
    flask_app = Flask(__name__)
    flask_app.config['SECRET_KEY'] = 'your-secret-key'

    @flask_app.route('/')
    def index():
        return '<h1>Flask App</h1><p><a href="/dash/">Go to Dashboard</a></p>'

    @flask_app.route('/api/data')
    def api_data():
        return {'message': 'Hello from Flask API'}

    # Dash application
    dash_app = dash.Dash(__name__, server=flask_app, url_base_pathname='/dash/')

    dash_app.layout = html.Div([
        html.H1('Dash App within Flask'),
        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': [1, 2, 3, 4], 'y': [4, 5, 2, 3], 'type': 'bar', 'name': 'SF'},
                    {'x': [1, 2, 3, 4], 'y': [2, 4, 5, 6], 'type': 'bar', 'name': 'NYC'},
                ],
                'layout': {'title': 'Dash Data Visualization'}
            }
        )
    ])

    return flask_app

# Testing Flask-Dash integration
import pytest
from flask.testing import FlaskClient

def test_flask_dash_integration():
    """Test Flask-Dash integration"""
    app = create_flask_dash_app()

    with app.test_client() as client:
        # Test Flask route
        response = client.get('/')
        assert response.status_code == 200
        assert b'Flask App' in response.data

        # Test Flask API
        response = client.get('/api/data')
        assert response.status_code == 200
        assert response.json['message'] == 'Hello from Flask API'

        # Test Dash route
        response = client.get('/dash/')
        assert response.status_code == 200
        assert b'Dash App within Flask' in response.data

# Configuration-aware Dash testing
class TestDashConfiguration:
    """Test Dash application with different configurations"""

    def test_development_config(self):
        """Test Dash app in development mode"""
        app = create_test_app()
        app.config.update({
            'suppress_callback_exceptions': False,
            'dev_tools_hot_reload': True,
            'dev_tools_serve_dev_bundles': True
        })

        # Test that debug features are enabled
        assert app.config['dev_tools_hot_reload'] is True

    def test_production_config(self):
        """Test Dash app in production mode"""
        app = create_test_app()
        app.config.update({
            'suppress_callback_exceptions': True,
            'dev_tools_hot_reload': False,
            'dev_tools_serve_dev_bundles': False
        })

        # Test that production settings are applied
        assert app.config['dev_tools_hot_reload'] is False

# Mocking external data sources
@pytest.fixture
def mock_database():
    """Mock database for testing"""
    import sqlite3
    import tempfile

    # Create in-memory database
    db = sqlite3.connect(':memory:')
    cursor = db.cursor()

    # Create test table
    cursor.execute('''
        CREATE TABLE sales (
            id INTEGER PRIMARY KEY,
            product TEXT,
            amount REAL,
            date TEXT
        )
    ''')

    # Insert test data
    test_data = [
        ('Product A', 100.0, '2020-07-01'),
        ('Product B', 150.0, '2020-07-02'),
        ('Product C', 200.0, '2020-07-03')
    ]

    cursor.executemany('INSERT INTO sales (product, amount, date) VALUES (?, ?, ?)',
                      test_data)
    db.commit()

    yield db
    db.close()

def test_dash_with_database(mock_database):
    """Test Dash app that uses database"""
    cursor = mock_database.cursor()
    cursor.execute('SELECT * FROM sales')
    data = cursor.fetchall()

    assert len(data) == 3
    assert data[0][1] == 'Product A'  # product name
```

{{< note title="Dash Testing Best Practices" >}} **Key Testing Strategies:**

- **Use dash.testing framework** for official Dash testing support
- **Mock external dependencies** to ensure isolated tests
- **Test callbacks separately** from UI interactions
- **Use headless browsers** for CI/CD environments
- **Implement page object patterns** for complex UI interactions
- **Test responsiveness** across different screen sizes {{< /note >}}

### Caching Dash Responses

[Memoizing dash callback responses with flask-caching](http://dash.plotly.com/testing)
improves application performance:

```python
# Implementing caching in Dash applications
from flask_caching import Cache
import dash
from dash import dcc, html, Input, Output, callback
import time
import hashlib

def create_cached_dash_app():
    """Create Dash app with caching enabled"""
    app = dash.Dash(__name__)

    # Configure caching
    cache = Cache(app.server, config={
        'CACHE_TYPE': 'simple',  # Use 'redis' for production
        'CACHE_DEFAULT_TIMEOUT': 300  # 5 minutes
    })

    app.layout = html.Div([
        html.H1("Cached Dashboard"),

        dcc.Dropdown(
            id="data-selector",
            options=[
                {'label': 'Dataset A', 'value': 'dataset_a'},
                {'label': 'Dataset B', 'value': 'dataset_b'},
                {'label': 'Dataset C', 'value': 'dataset_c'}
            ],
            value='dataset_a'
        ),

        dcc.Graph(id="cached-graph"),
        html.Div(id="computation-time"),
        html.Button("Clear Cache", id="clear-cache-btn"),
        html.Div(id="cache-status")
    ])

    # Expensive computation function (simulated)
    @cache.memoize(timeout=300)
    def expensive_computation(dataset_name):
        """Simulate expensive data processing"""
        print(f"Computing expensive operation for {dataset_name}")

        # Simulate processing time
        time.sleep(2)

        # Generate mock data based on dataset
        import numpy as np
        np.random.seed(hash(dataset_name) % 2**32)  # Deterministic randomness

        x = np.linspace(0, 10, 100)
        y = np.sin(x) + np.random.normal(0, 0.1, 100)

        return {
            'x': x.tolist(),
            'y': y.tolist(),
            'computation_time': time.time()
        }

    @callback(
        [Output("cached-graph", "figure"),
         Output("computation-time", "children")],
        [Input("data-selector", "value")]
    )
    def update_graph(dataset_name):
        start_time = time.time()

        # This will be cached after first call
        data = expensive_computation(dataset_name)

        end_time = time.time()

        figure = {
            'data': [{
                'x': data['x'],
                'y': data['y'],
                'type': 'scatter',
                'mode': 'lines+markers',
                'name': dataset_name
            }],
            'layout': {
                'title': f'Cached Data for {dataset_name}',
                'xaxis': {'title': 'X Values'},
                'yaxis': {'title': 'Y Values'}
            }
        }

        time_info = html.Div([
            html.P(f"Callback execution time: {end_time - start_time:.3f} seconds"),
            html.P(f"Data computed at: {time.ctime(data['computation_time'])}")
        ])

        return figure, time_info

    @callback(
        Output("cache-status", "children"),
        [Input("clear-cache-btn", "n_clicks")]
    )
    def clear_cache(n_clicks):
        if n_clicks:
            cache.clear()
            return html.P("Cache cleared!", style={'color': 'green'})
        return html.P("Cache active", style={'color': 'blue'})

    return app, cache

# Advanced caching strategies
class DashCacheManager:
    """Advanced cache management for Dash applications"""

    def __init__(self, cache):
        self.cache = cache

    def cache_key_generator(self, *args, **kwargs):
        """Generate cache key from function arguments"""
        key_string = str(args) + str(sorted(kwargs.items()))
        return hashlib.md5(key_string.encode()).hexdigest()

    def conditional_cache(self, condition_func, timeout=300):
        """Cache decorator that only caches based on condition"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                if condition_func(*args, **kwargs):
                    cache_key = f"{func.__name__}_{self.cache_key_generator(*args, **kwargs)}"
                    cached_result = self.cache.get(cache_key)

                    if cached_result is not None:
                        return cached_result

                    result = func(*args, **kwargs)
                    self.cache.set(cache_key, result, timeout=timeout)
                    return result
                else:
                    return func(*args, **kwargs)
            return wrapper
        return decorator

    def cache_with_invalidation(self, invalidation_keys, timeout=300):
        """Cache with dependency-based invalidation"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                cache_key = f"{func.__name__}_{self.cache_key_generator(*args, **kwargs)}"

                # Check if any invalidation keys have changed
                for inv_key in invalidation_keys:
                    if self.cache.get(f"invalidation_{inv_key}") is None:
                        # Key doesn't exist, set it
                        self.cache.set(f"invalidation_{inv_key}", time.time())

                cached_result = self.cache.get(cache_key)
                if cached_result is not None:
                    return cached_result

                result = func(*args, **kwargs)
                self.cache.set(cache_key, result, timeout=timeout)
                return result
            return wrapper
        return decorator

    def invalidate_cache_group(self, group_key):
        """Invalidate all cache entries in a group"""
        self.cache.delete(f"invalidation_{group_key}")

# Usage example
def test_advanced_caching():
    """Test advanced caching features"""
    app, cache = create_cached_dash_app()
    cache_manager = DashCacheManager(cache)

    @cache_manager.conditional_cache(
        condition_func=lambda dataset: len(dataset) > 100,
        timeout=600
    )
    def process_large_dataset(dataset):
        # Only cache if dataset is large
        return sum(dataset)

    @cache_manager.cache_with_invalidation(
        invalidation_keys=['user_data', 'settings'],
        timeout=300
    )
    def user_specific_computation(user_id, settings):
        # Cache invalidated when user_data or settings change
        return f"Result for user {user_id} with {settings}"

    # Test the functions
    small_data = [1, 2, 3]  # Won't be cached
    large_data = list(range(200))  # Will be cached

    result1 = process_large_dataset(small_data)
    result2 = process_large_dataset(large_data)

    # Invalidate user-specific cache
    cache_manager.invalidate_cache_group('user_data')
```

## Pi-hole DNS Architecture

### Understanding FTL Engine

Pi-hole's "Faster than Light" (FTL) engine is based on a fork of dnsmasq,
providing advanced DNS filtering capabilities:

```bash
# Pi-hole architecture and configuration

# Check Pi-hole FTL status
sudo systemctl status pihole-FTL

# View FTL configuration
cat /etc/pihole/pihole-FTL.conf

# Monitor DNS queries in real-time
tail -f /var/log/pihole.log

# Query Pi-hole API for statistics
curl "http://pi.hole/admin/api.php"

# Get query types over time
curl "http://pi.hole/admin/api.php?overTimeDataForGraph"

# Get top blocked domains
curl "http://pi.hole/admin/api.php?topBlocked"

# Get DNS query sources
curl "http://pi.hole/admin/api.php?topClients"
```

### DNS Resolution Flow in Pi-hole

```python
# Simulate Pi-hole DNS resolution logic
import socket
import time
from typing import Dict, Set, Optional
import re

class PiHoleDNSSimulator:
    """Simulate Pi-hole DNS resolution process"""

    def __init__(self):
        self.blocklists: Set[str] = set()
        self.whitelist: Set[str] = set()
        self.local_dns: Dict[str, str] = {}
        self.upstream_dns = ['8.8.8.8', '1.1.1.1']
        self.query_log = []
        self.cache = {}
        self.cache_ttl = {}

    def load_blocklist(self, blocklist_url: str):
        """Load blocklist from URL (simulated)"""
        # In real Pi-hole, this downloads and parses blocklists
        sample_blocked = [
            'ads.example.com',
            'tracker.evil.com',
            'malware.bad.com',
            'popup.annoying.com'
        ]
        self.blocklists.update(sample_blocked)
        print(f"Loaded {len(sample_blocked)} domains from blocklist")

    def add_to_whitelist(self, domain: str):
        """Add domain to whitelist"""
        self.whitelist.add(domain)
        print(f"Whitelisted: {domain}")

    def add_local_dns(self, domain: str, ip: str):
        """Add local DNS entry"""
        self.local_dns[domain] = ip
        print(f"Local DNS: {domain} -> {ip}")

    def is_blocked(self, domain: str) -> bool:
        """Check if domain should be blocked"""
        # Check whitelist first
        if domain in self.whitelist:
            return False

        # Check exact match
        if domain in self.blocklists:
            return True

        # Check wildcard/subdomain blocking
        for blocked in self.blocklists:
            if blocked.startswith('*.') and domain.endswith(blocked[2:]):
                return True
            if domain.endswith('.' + blocked):
                return True

        return False

    def resolve_dns(self, domain: str, query_type: str = 'A') -> Optional[str]:
        """Simulate DNS resolution process"""
        query_start = time.time()
        client_ip = "192.168.1.100"  # Simulated client

        # Log the query
        self.query_log.append({
            'timestamp': query_start,
            'client': client_ip,
            'domain': domain,
            'type': query_type,
            'status': 'processing'
        })

        # Step 1: Check if domain is blocked
        if self.is_blocked(domain):
            self.query_log[-1]['status'] = 'blocked'
            self.query_log[-1]['response'] = '0.0.0.0'  # Pi-hole returns null route
            print(f"BLOCKED: {domain} -> 0.0.0.0")
            return '0.0.0.0'

        # Step 2: Check local DNS entries
        if domain in self.local_dns:
            result = self.local_dns[domain]
            self.query_log[-1]['status'] = 'local'
            self.query_log[-1]['response'] = result
            print(f"LOCAL: {domain} -> {result}")
            return result

        # Step 3: Check cache
        cache_key = f"{domain}_{query_type}"
        if cache_key in self.cache and time.time() < self.cache_ttl[cache_key]:
            result = self.cache[cache_key]
            self.query_log[-1]['status'] = 'cached'
            self.query_log[-1]['response'] = result
            print(f"CACHED: {domain} -> {result}")
            return result

        # Step 4: Forward to upstream DNS
        result = self.forward_to_upstream(domain, query_type)

        if result:
            # Cache the result
            self.cache[cache_key] = result
            self.cache_ttl[cache_key] = time.time() + 300  # 5 minute TTL

            self.query_log[-1]['status'] = 'forwarded'
            self.query_log[-1]['response'] = result
            print(f"FORWARDED: {domain} -> {result}")
            return result
        else:
            self.query_log[-1]['status'] = 'failed'
            print(f"FAILED: Could not resolve {domain}")
            return None

    def forward_to_upstream(self, domain: str, query_type: str) -> Optional[str]:
        """Simulate forwarding to upstream DNS servers"""
        # In real implementation, this would make actual DNS queries
        # For simulation, return mock IPs based on domain
        import hashlib

        if query_type == 'A':
            # Generate deterministic IP based on domain
            hash_int = int(hashlib.md5(domain.encode()).hexdigest()[:8], 16)
            ip = f"{(hash_int >> 24) % 256}.{(hash_int >> 16) % 256}.{(hash_int >> 8) % 256}.{hash_int % 256}"
            return ip
        elif query_type == 'AAAA':
            return "2001:db8::1"  # Mock IPv6
        else:
            return None

    def get_statistics(self) -> Dict:
        """Get Pi-hole style statistics"""
        total_queries = len(self.query_log)
        blocked_queries = len([q for q in self.query_log if q['status'] == 'blocked'])

        return {
            'dns_queries_today': total_queries,
            'ads_blocked_today': blocked_queries,
            'ads_percentage_today': (blocked_queries / total_queries * 100) if total_queries > 0 else 0,
            'domains_being_blocked': len(self.blocklists),
            'queries_cached': len([q for q in self.query_log if q['status'] == 'cached']),
            'queries_forwarded': len([q for q in self.query_log if q['status'] == 'forwarded']),
            'unique_domains': len(set(q['domain'] for q in self.query_log)),
            'unique_clients': len(set(q['client'] for q in self.query_log))
        }

    def get_top_blocked(self, limit: int = 10) -> list:
        """Get most blocked domains"""
        blocked_domains = [q['domain'] for q in self.query_log if q['status'] == 'blocked']
        from collections import Counter
        return Counter(blocked_domains).most_common(limit)

    def get_query_timeline(self) -> Dict:
        """Get queries over time"""
        timeline = {}
        for query in self.query_log:
            hour = int(query['timestamp'] // 3600)
            if hour not in timeline:
                timeline[hour] = {'total': 0, 'blocked': 0}
            timeline[hour]['total'] += 1
            if query['status'] == 'blocked':
                timeline[hour]['blocked'] += 1

        return timeline

# Usage example and testing
def test_pihole_simulation():
    """Test Pi-hole DNS simulation"""
    pihole = PiHoleDNSSimulator()

    # Configure Pi-hole
    pihole.load_blocklist("https://someonewhocares.org/hosts/zero/hosts")
    pihole.add_to_whitelist("ads.example.com")  # Whitelist an ad domain
    pihole.add_local_dns("router.local", "192.168.1.1")
    pihole.add_local_dns("printer.local", "192.168.1.10")

    # Simulate various DNS queries
    test_domains = [
        "google.com",           # Should be allowed and forwarded
        "ads.example.com",      # Should be allowed (whitelisted)
        "tracker.evil.com",     # Should be blocked
        "router.local",         # Should resolve locally
        "facebook.com",         # Should be allowed and cached on repeat
        "malware.bad.com",      # Should be blocked
        "github.com"            # Should be allowed
    ]

    print("=== Pi-hole DNS Resolution Simulation ===\n")

    # First round of queries
    for domain in test_domains:
        pihole.resolve_dns(domain)

    print("\n=== Repeat queries (should show caching) ===\n")

    # Repeat some queries to test caching
    for domain in ["google.com", "facebook.com", "github.com"]:
        pihole.resolve_dns(domain)

    # Show statistics
    stats = pihole.get_statistics()
    print(f"\n=== Pi-hole Statistics ===")
    print(f"Total DNS queries: {stats['dns_queries_today']}")
    print(f"Ads blocked: {stats['ads_blocked_today']}")
    print(f"Percentage blocked: {stats['ads_percentage_today']:.1f}%")
    print(f"Domains being blocked: {stats['domains_being_blocked']}")
    print(f"Queries cached: {stats['queries_cached']}")
    print(f"Queries forwarded: {stats['queries_forwarded']}")

    # Show top blocked domains
    top_blocked = pihole.get_top_blocked(5)
    print(f"\n=== Top Blocked Domains ===")
    for domain, count in top_blocked:
        print(f"{domain}: {count} queries blocked")

# Run the simulation
test_pihole_simulation()
```

{{< example title="Pi-hole DNS Resolution Process" >}} **DNS Query Flow in
Pi-hole:**

1. **Client Query** - Device sends DNS request to Pi-hole
2. **Blocklist Check** - Pi-hole checks if domain is in blocklists
3. **Whitelist Override** - Whitelisted domains bypass blocking
4. **Local DNS** - Check for local network entries (router.local, etc.)
5. **Cache Lookup** - Check if response is already cached
6. **Upstream Forward** - Forward to configured DNS servers (Google, Cloudflare)
7. **Response & Cache** - Return response and cache for future queries
8. **Logging** - Record query details for statistics and monitoring
   {{< /example >}}

## Python argparse Subcommands

Python's `argparse` module supports subcommands for building complex CLI
applications:

```python
# Advanced argparse patterns with subcommands
import argparse
import sys
from typing import Optional

class PiHoleCLI:
    """Pi-hole command-line interface simulator"""

    def __init__(self):
        self.parser = self.create_parser()

    def create_parser(self) -> argparse.ArgumentParser:
        """Create argument parser with subcommands"""
        parser = argparse.ArgumentParser(
            description="Pi-hole DNS management tool",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  pihole status                    # Show Pi-hole status
  pihole enable                    # Enable DNS blocking
  pihole disable 300              # Disable blocking for 5 minutes
  pihole query google.com         # Query domain status
  pihole blacklist add ads.com    # Add domain to blacklist
  pihole whitelist remove safe.com # Remove from whitelist
  pihole log tail -n 100          # Show last 100 log entries
            """
        )

        parser.add_argument(
            '--config',
            default='/etc/pihole/pihole-FTL.conf',
            help='Path to Pi-hole configuration file'
        )

        parser.add_argument(
            '-v', '--verbose',
            action='store_true',
            help='Enable verbose output'
        )

        # Create subparsers
        subparsers = parser.add_subparsers(
            dest='command',
            help='Available commands',
            metavar='COMMAND'
        )

        # Status command
        status_parser = subparsers.add_parser(
            'status',
            help='Show Pi-hole status'
        )

        # Enable command
        enable_parser = subparsers.add_parser(
            'enable',
            help='Enable DNS blocking'
        )

        # Disable command
        disable_parser = subparsers.add_parser(
            'disable',
            help='Disable DNS blocking'
        )
        disable_parser.add_argument(
            'duration',
            type=int,
            nargs='?',
            default=0,
            help='Disable duration in seconds (0 = permanently)'
        )

        # Query command
        query_parser = subparsers.add_parser(
            'query',
            help='Query domain status'
        )
        query_parser.add_argument(
            'domain',
            help='Domain to query'
        )
        query_parser.add_argument(
            '--type',
            choices=['A', 'AAAA', 'MX', 'TXT'],
            default='A',
            help='DNS query type'
        )

        # Blacklist management
        blacklist_parser = subparsers.add_parser(
            'blacklist',
            help='Manage blacklist'
        )
        blacklist_subparsers = blacklist_parser.add_subparsers(
            dest='blacklist_action',
            help='Blacklist actions'
        )

        # Blacklist add
        blacklist_add = blacklist_subparsers.add_parser(
            'add',
            help='Add domains to blacklist'
        )
        blacklist_add.add_argument(
            'domains',
            nargs='+',
            help='Domains to add'
        )
        blacklist_add.add_argument(
            '--comment',
            help='Comment for the entry'
        )

        # Blacklist remove
        blacklist_remove = blacklist_subparsers.add_parser(
            'remove',
            help='Remove domains from blacklist'
        )
        blacklist_remove.add_argument(
            'domains',
            nargs='+',
            help='Domains to remove'
        )

        # Blacklist list
        blacklist_list = blacklist_subparsers.add_parser(
            'list',
            help='List blacklisted domains'
        )
        blacklist_list.add_argument(
            '--grep',
            help='Filter domains with grep pattern'
        )

        # Whitelist management (similar structure)
        whitelist_parser = subparsers.add_parser(
            'whitelist',
            help='Manage whitelist'
        )
        whitelist_subparsers = whitelist_parser.add_subparsers(
            dest='whitelist_action',
            help='Whitelist actions'
        )

        whitelist_add = whitelist_subparsers.add_parser('add', help='Add domains to whitelist')
        whitelist_add.add_argument('domains', nargs='+', help='Domains to add')

        whitelist_remove = whitelist_subparsers.add_parser('remove', help='Remove domains from whitelist')
        whitelist_remove.add_argument('domains', nargs='+', help='Domains to remove')

        whitelist_list = whitelist_subparsers.add_parser('list', help='List whitelisted domains')

        # Log management
        log_parser = subparsers.add_parser(
            'log',
            help='Manage Pi-hole logs'
        )
        log_subparsers = log_parser.add_subparsers(
            dest='log_action',
            help='Log actions'
        )

        log_tail = log_subparsers.add_parser('tail', help='Tail log file')
        log_tail.add_argument('-n', '--lines', type=int, default=10, help='Number of lines to show')
        log_tail.add_argument('-f', '--follow', action='store_true', help='Follow log file')

        log_grep = log_subparsers.add_parser('grep', help='Search log file')
        log_grep.add_argument('pattern', help='Search pattern')
        log_grep.add_argument('-i', '--ignore-case', action='store_true', help='Ignore case')

        # Statistics
        stats_parser = subparsers.add_parser(
            'stats',
            help='Show Pi-hole statistics'
        )
        stats_parser.add_argument(
            '--format',
            choices=['json', 'table', 'csv'],
            default='table',
            help='Output format'
        )

        return parser

    def handle_command(self, args):
        """Handle parsed command arguments"""
        if args.verbose:
            print(f"Verbose mode enabled. Config: {args.config}")

        if not args.command:
            self.parser.print_help()
            return

        # Route to appropriate handler
        handler_name = f"handle_{args.command}"
        if hasattr(self, handler_name):
            handler = getattr(self, handler_name)
            handler(args)
        else:
            print(f"Command '{args.command}' not implemented yet")

    def handle_status(self, args):
        """Handle status command"""
        print("Pi-hole Status:")
        print("  DNS Service: Active")
        print("  Blocking: Enabled")
        print("  Blocklists: 1,234,567 domains")
        print("  Queries today: 12,345")
        print("  Blocked today: 1,234 (10.0%)")

    def handle_enable(self, args):
        """Handle enable command"""
        print("Enabling Pi-hole DNS blocking...")
        print("DNS blocking is now ENABLED")

    def handle_disable(self, args):
        """Handle disable command"""
        if args.duration > 0:
            print(f"Disabling Pi-hole DNS blocking for {args.duration} seconds...")
        else:
            print("Disabling Pi-hole DNS blocking permanently...")
        print("DNS blocking is now DISABLED")

    def handle_query(self, args):
        """Handle query command"""
        print(f"Querying {args.domain} ({args.type} record)...")
        print(f"Domain: {args.domain}")
        print(f"Status: Not blocked")
        print(f"Response: 192.168.1.1")

    def handle_blacklist(self, args):
        """Handle blacklist command"""
        if args.blacklist_action == 'add':
            print(f"Adding {len(args.domains)} domain(s) to blacklist:")
            for domain in args.domains:
                print(f"  + {domain}")
                if args.comment:
                    print(f"    Comment: {args.comment}")
        elif args.blacklist_action == 'remove':
            print(f"Removing {len(args.domains)} domain(s) from blacklist:")
            for domain in args.domains:
                print(f"  - {domain}")
        elif args.blacklist_action == 'list':
            print("Blacklisted domains:")
            sample_domains = ['ads.example.com', 'tracker.evil.com', 'malware.bad.com']
            for domain in sample_domains:
                if not args.grep or args.grep in domain:
                    print(f"  {domain}")

    def handle_whitelist(self, args):
        """Handle whitelist command"""
        action = args.whitelist_action
        if action == 'add':
            print(f"Adding {len(args.domains)} domain(s) to whitelist:")
            for domain in args.domains:
                print(f"  + {domain}")
        elif action == 'remove':
            print(f"Removing {len(args.domains)} domain(s) from whitelist:")
            for domain in args.domains:
                print(f"  - {domain}")
        elif action == 'list':
            print("Whitelisted domains:")
            print("  google.com")
            print("  github.com")

    def handle_log(self, args):
        """Handle log command"""
        if args.log_action == 'tail':
            print(f"Showing last {args.lines} lines from Pi-hole log:")
            if args.follow:
                print("Following log file (Ctrl+C to stop)...")
            # In real implementation, would tail actual log file
            for i in range(args.lines):
                print(f"2020-07-24 12:34:{i:02d} Query: example.com from 192.168.1.100")
        elif args.log_action == 'grep':
            print(f"Searching log for pattern: {args.pattern}")
            if args.ignore_case:
                print("Case-insensitive search enabled")
            print("192.168.1.100 2020-07-24 12:34:56 example.com")

    def handle_stats(self, args):
        """Handle stats command"""
        stats = {
            'dns_queries_today': 12345,
            'ads_blocked_today': 1234,
            'ads_percentage_today': 10.0,
            'domains_being_blocked': 1234567,
            'unique_domains': 5678,
            'unique_clients': 15
        }

        if args.format == 'json':
            import json
            print(json.dumps(stats, indent=2))
        elif args.format == 'csv':
            print("metric,value")
            for key, value in stats.items():
                print(f"{key},{value}")
        else:  # table format
            print("Pi-hole Statistics:")
            print(f"  DNS queries today: {stats['dns_queries_today']:,}")
            print(f"  Ads blocked today: {stats['ads_blocked_today']:,}")
            print(f"  Percentage blocked: {stats['ads_percentage_today']:.1f}%")
            print(f"  Domains being blocked: {stats['domains_being_blocked']:,}")
            print(f"  Unique domains: {stats['unique_domains']:,}")
            print(f"  Unique clients: {stats['unique_clients']}")

    def run(self, args=None):
        """Run the CLI application"""
        if args is None:
            args = sys.argv[1:]

        parsed_args = self.parser.parse_args(args)
        self.handle_command(parsed_args)

# Usage examples
if __name__ == "__main__":
    cli = PiHoleCLI()

    # Test various commands
    test_commands = [
        ['status'],
        ['query', 'google.com', '--type', 'A'],
        ['blacklist', 'add', 'ads.com', 'tracker.com', '--comment', 'Ad domains'],
        ['whitelist', 'list'],
        ['log', 'tail', '-n', '5'],
        ['stats', '--format', 'json'],
        ['disable', '300']
    ]

    for cmd in test_commands:
        print(f"\n> pihole {' '.join(cmd)}")
        print("-" * 50)
        cli.run(cmd)
```

{{< tip title="argparse Subcommand Benefits" >}} **Advantages of Subcommands:**

- **Organized functionality** - Group related operations logically
- **Context-specific help** - Each subcommand has its own help text
- **Nested commands** - Support for sub-subcommands (like git)
- **Clean interfaces** - Users see only relevant options for each command
- **Extensible design** - Easy to add new commands without cluttering main
  parser {{< /tip >}}

## Key Learning Insights

### Testing Interactive Applications

Today's exploration of Dash testing highlighted the complexity of testing
interactive web applications:

- **Multi-layer testing** - Unit tests for callbacks, integration tests for UI
  interactions
- **Caching strategies** - Performance optimization through intelligent response
  caching
- **Mock external dependencies** - Isolate application logic from external
  services
- **Configuration awareness** - Test different deployment scenarios

### DNS Infrastructure Understanding

The Pi-hole deep dive revealed the sophisticated nature of modern DNS filtering:

- **Query pipeline** - Multiple decision points in DNS resolution flow
- **Performance optimization** - Caching and local resolution reduce latency
- **Monitoring and analytics** - Comprehensive logging enables insights and
  troubleshooting
- **Flexibility** - Whitelist overrides and local DNS provide fine-grained
  control

### CLI Design Patterns

The argparse exploration demonstrated best practices for command-line tool
design:

- **Hierarchical commands** - Subcommands create intuitive organization
- **Context-sensitive help** - Users get relevant information at each level
- **Consistent interfaces** - Similar patterns across different command groups
- **Extensible architecture** - Easy to add functionality without breaking
  existing usage

---

_This exploration reinforced that complex systems benefit from layered
architectures, comprehensive testing strategies, and intuitive user interfaces
that scale from simple to advanced use cases._
