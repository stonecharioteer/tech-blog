---
date: 2021-02-16T10:00:00+05:30
draft: false
title: "TIL: GitHubtop Real-time Activity Monitor and GoAccess Web Log Analyzer"
description:
  "Today I learned about ghtop for monitoring GitHub activity in real-time and
  GoAccess, a powerful visual web log analyzer for understanding website traffic
  patterns."
tags:
  - "til"
  - "github"
  - "monitoring"
  - "web-analytics"
  - "log-analysis"
  - "devops"
---

## ghtop - Real-time GitHub Activity Monitor

[GitHub - nat/ghtop: See what's happening on GitHub in real time](https://github.com/nat/ghtop)

Terminal-based tool for monitoring GitHub activity in real-time:

### What It Does:

- **Live Activity**: Real-time stream of GitHub events
- **API Consumption**: Helpful for using up GitHub API quota quickly
- **Terminal Interface**: htop-style display for GitHub events
- **Event Filtering**: Focus on specific types of GitHub activity

### Key Features:

#### **Event Types Monitored:**

- **Push Events**: Code commits to repositories
- **Pull Requests**: PR creation, updates, merges
- **Issues**: Issue creation, comments, closures
- **Releases**: New releases and tags
- **Forks**: Repository forks
- **Stars**: Repository stars and watches

#### **Display Information:**

```
User          Repository         Event Type    Time
alice         awesome-project    PushEvent     2s ago
bob           cool-tool         IssuesEvent    5s ago
charlie       web-framework     ForkEvent     8s ago
diana         data-viz          ReleaseEvent  12s ago
```

### Use Cases:

#### **API Quota Management:**

- **Testing**: Quickly consume API rate limits for testing
- **Development**: Understand API usage patterns
- **Monitoring**: Track when rate limits reset
- **Debugging**: Test API error handling

#### **Community Insights:**

- **Trending Activity**: See what's active on GitHub right now
- **Development Patterns**: Understand when developers are most active
- **Project Monitoring**: Watch for activity on specific projects
- **Language Trends**: Observe which languages are being used

#### **Educational Value:**

- **GitHub API**: Learn about GitHub's event API structure
- **Real-time Data**: Understand streaming data concepts
- **Rate Limiting**: Experience API rate limiting firsthand

### Installation and Usage:

```bash
# Installation
npm install -g ghtop

# Basic usage
ghtop

# With API token for higher rate limits
GITHUB_TOKEN=your_token ghtop

# Filter by event type
ghtop --filter=PushEvent
```

## GoAccess - Visual Web Log Analyzer

[GoAccess - Visual Web Log Analyzer](https://goaccess.io/)

Real-time web log analyzer and interactive viewer:

### Core Capabilities:

#### **Log Format Support:**

- **Apache**: Common and combined log formats
- **Nginx**: Standard and custom log formats
- **IIS**: Microsoft web server logs
- **Amazon S3**: S3 access logs
- **CloudFlare**: CDN access logs
- **Custom Formats**: Define your own log patterns

#### **Real-time Analysis:**

```bash
# Real-time monitoring
tail -f /var/log/nginx/access.log | goaccess -

# Generate HTML report
goaccess /var/log/nginx/access.log -o report.html

# Real-time HTML dashboard
goaccess /var/log/nginx/access.log -o report.html --real-time-html
```

### Rich Analytics Dashboard:

#### **Traffic Metrics:**

- **Unique Visitors**: Daily unique IP addresses
- **Requested Files**: Most popular pages and resources
- **Static Requests**: CSS, JS, images analytics
- **404 Errors**: Broken links and missing resources
- **Hosts**: Top visitor IP addresses and domains

#### **Detailed Reports:**

```
Top Requested Files
┌─────────────────────────────────────────────────────┐
│ /index.html              │ 1,234 │ 15.2% │ 2.1 MB  │
│ /api/users               │   987 │ 12.1% │ 890 KB  │
│ /static/app.js           │   756 │  9.3% │ 1.5 MB  │
│ /login                   │   654 │  8.0% │ 234 KB  │
└─────────────────────────────────────────────────────┘

Operating Systems
┌─────────────────────────────────────────────────────┐
│ Linux                    │ 2,345 │ 45.6% │         │
│ Windows                  │ 1,876 │ 36.5% │         │
│ macOS                    │   789 │ 15.3% │         │
│ Unknown                  │   134 │  2.6% │         │
└─────────────────────────────────────────────────────┘
```

### Advanced Features:

#### **GeoIP Integration:**

```bash
# Install GeoIP database
sudo apt-get install geoip-database

# Enable geographic reporting
goaccess --geoip-database=/usr/share/GeoIP/GeoIP.dat
```

**Geographic Analytics:**

- **Countries**: Visitor distribution by country
- **Cities**: Top cities accessing your site
- **Maps**: Visual geographic representation
- **Timezone Analysis**: Traffic patterns by timezone

#### **Custom Log Formats:**

```bash
# Define custom nginx format
goaccess --log-format='%h %^[%d:%t %^] "%r" %s %b "%R" "%u"' \
         --date-format='%d/%b/%Y' \
         --time-format='%T'

# Complex format with custom fields
goaccess --log-format='%h %^ %^ [%d:%t %^] "%r" %s %b "%R" "%u" %D %T' \
         --date-format='%d/%b/%Y' \
         --time-format='%T'
```

#### **Interactive HTML Dashboard:**

- **Real-time Updates**: Live data streaming
- **Responsive Design**: Mobile-friendly interface
- **Interactive Charts**: Clickable graphs and tables
- **Export Options**: PDF, CSV, JSON export capabilities

### Performance Optimization:

#### **Large Log Files:**

```bash
# Use --no-global-config for better performance
goaccess --no-global-config /var/log/nginx/*.log

# Process compressed logs
zcat /var/log/nginx/*.gz | goaccess -

# Multiple log files
goaccess /var/log/nginx/access.log.* --log-format=COMBINED
```

#### **Memory Management:**

- **Streaming Mode**: Process logs without loading entirely into memory
- **Incremental Updates**: Add new log entries to existing reports
- **Disk Storage**: Store data structures on disk for large datasets

### Integration and Automation:

#### **Automated Reporting:**

```bash
#!/bin/bash
# Daily report generation
goaccess /var/log/nginx/access.log \
    --log-format=COMBINED \
    --output-format=html \
    --output=/var/www/html/stats/daily-$(date +%Y%m%d).html

# Email reports
goaccess /var/log/nginx/access.log \
    --log-format=COMBINED \
    --output-format=csv | \
    mail -s "Daily Website Stats" admin@example.com
```

#### **CI/CD Integration:**

- **Performance Monitoring**: Track site performance over time
- **Traffic Analysis**: Understand user behavior patterns
- **Security Monitoring**: Detect unusual access patterns
- **Capacity Planning**: Analyze traffic growth trends

### Configuration Options:

#### **Color Schemes:**

```bash
# Dark theme
goaccess --color-scheme=2

# Custom colors
goaccess --html-custom-css=styles.css
```

#### **Filtering:**

```bash
# Exclude specific IPs
goaccess --exclude-ip=192.168.1.1

# Include only specific paths
goaccess --ignore-panel=KEYPHRASES,REFERERS

# Date range filtering
goaccess --date-spec=hr  # Hourly breakdown
```

Both tools provide valuable insights into different aspects of software
development and web operations - real-time GitHub activity monitoring and
comprehensive web traffic analysis.
