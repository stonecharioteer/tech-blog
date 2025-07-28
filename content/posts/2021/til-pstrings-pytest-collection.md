---
date: 2021-01-30T10:00:00+05:30
draft: false
title: "TIL: Gary Bernhardt's 'It's Fine' Talk, pstrings for Process Memory, and pytest Collection Techniques"
description: "Today I learned about Gary Bernhardt's humorous take on software development culture, the pstrings tool for examining process memory strings, and pytest's powerful test collection and filtering capabilities."
tags:
  - TIL
  - Software Culture
  - System Programming
  - Testing
  - pytest
  - Memory Analysis
  - Linux Tools
---

## Gary Bernhardt: "It's Fine" - Software Development Culture

[Gary Bernhardt: It's Fine | DHTMLConf 2000 | JSFest Oakland 2014 - YouTube](https://youtu.be/8QlZbg5B1vk)

Brilliant satirical talk about software development culture and technical debt:

### The Premise:
- **Satirical Commentary**: Humorous take on "this is fine" mentality in software
- **Technical Debt**: How developers normalize increasingly broken systems
- **Cultural Critique**: Examination of acceptance culture in tech industry
- **Historical Perspective**: How we got to "everything is broken but fine"

### Key Themes:

#### **Normalization of Dysfunction:**
```javascript
// "It's fine" examples
setTimeout(() => {
  // This will probably work most of the time
  document.getElementById('maybe-exists').click();
}, 100); // Magic number that "works"

// CSS that's definitely fine
.container { position: relative; }
.content { position: absolute; top: -1px; left: -1px; }
.fix { margin-top: 2px; } /* Fixes Safari bug from 2008 */
```

#### **Accumulated Workarounds:**
- **Layer Upon Layer**: Fixes built on top of previous fixes
- **Historical Context**: Solutions that made sense years ago
- **Knowledge Loss**: Original reasons for workarounds forgotten
- **Fear of Change**: "Don't touch it, it works somehow"

### Cultural Observations:

#### **Developer Mindset:**
- **Pragmatic Acceptance**: "Ship it now, fix it later"
- **Stockholm Syndrome**: Growing fond of broken systems
- **Learned Helplessness**: Accepting that things are just broken
- **Tribal Knowledge**: Undocumented fixes passed down through teams

#### **System Evolution:**
```bash
# The evolution of a "simple" deployment
./run.sh                     # 2010: It's fine!
./run.sh | tee deploy.log    # 2012: Need logs
./run.sh 2>&1 | tee deploy.log # 2013: Capture errors too
nohup ./run.sh 2>&1 | tee deploy.log & # 2014: Run in background
screen -S deploy ./run.sh 2>&1 | tee deploy.log # 2015: Reattachable
docker run --rm -v $(pwd):/app deploy-image # 2018: Containerized
kubectl apply -f deploy.yaml  # 2020: "Simple" Kubernetes
```

### The Deeper Message:
- **Systemic Issues**: Individual "it's fine" decisions compound
- **Technical Debt**: Accumulation leads to unmaintainable systems
- **Culture Change**: Need for higher standards and better practices
- **Awareness**: Recognizing when "fine" isn't actually fine

## pstrings - Process Memory String Analysis

[GitHub - andikleen/pstrings: strings for a Linux process' address space](https://github.com/andikleen/pstrings)

Advanced tool for examining strings in running process memory:

### What It Does:
- **Live Process Analysis**: Extract strings from running processes
- **Memory Mapping**: Analyze different memory regions (heap, stack, libs)
- **Dynamic Analysis**: Monitor string changes over time
- **Security Research**: Find sensitive data in memory

### Key Features:

#### **Memory Region Targeting:**
```bash
# Analyze specific memory regions
pstrings -h <pid>    # Heap only
pstrings -s <pid>    # Stack only
pstrings -l <pid>    # Shared libraries only
pstrings -a <pid>    # All regions (default)

# Filter by string length
pstrings -n 10 <pid>   # Minimum 10 characters
pstrings -m 100 <pid>  # Maximum 100 characters
```

#### **Output Formatting:**
```bash
# Show memory addresses
pstrings -t x <pid>    # Hexadecimal addresses
pstrings -t d <pid>    # Decimal addresses
pstrings -t o <pid>    # Octal addresses

# Include region information
pstrings -r <pid>      # Show which memory region
```

### Use Cases:

#### **Security Analysis:**
```bash
# Look for sensitive data in memory
pstrings $(pgrep myapp) | grep -i password
pstrings $(pgrep browser) | grep -E '[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{4}'

# Monitor for credential leaks
while true; do
  pstrings $(pgrep webapp) | grep -i "api.*key" >> credential_monitor.log
  sleep 60
done
```

#### **Debugging:**
```bash
# Find configuration strings
pstrings $(pgrep myservice) | grep -E '(config|setting|option)'

# Locate error messages
pstrings $(pgrep failing_app) | grep -i error

# Find file paths being used
pstrings $(pgrep myapp) | grep -E '^/'
```

#### **Performance Analysis:**
- **Memory Leaks**: Find repeated strings indicating leaks
- **Cache Analysis**: Examine cached data in memory
- **Resource Usage**: Identify large string allocations

### Advanced Usage:

#### **Comparative Analysis:**
```bash
# Before operation
pstrings $(pgrep myapp) > before.txt

# Perform operation
curl http://localhost:8080/api/process-data

# After operation
pstrings $(pgrep myapp) > after.txt

# Find new strings
comm -13 before.txt after.txt
```

#### **Security Monitoring:**
```bash
#!/bin/bash
# Monitor for credential patterns
PATTERNS="password|secret|token|key|credential"
pstrings -a $(pgrep -f "web|server|app") | \
  grep -iE "$PATTERNS" | \
  while read line; do
    echo "$(date): POTENTIAL CREDENTIAL: $line" >> security.log
  done
```

## pytest Collection and Filtering

**Pytest Tip**: `pytest --collect-only -q` will collect all test names, with parameters, and just print out the names in a way that you can use with `pytest <name>`

Powerful pytest feature for test discovery and selective execution:

### Test Collection:

#### **Basic Collection:**
```bash
# List all tests without running them
pytest --collect-only

# Quiet mode - just test names
pytest --collect-only -q

# Very quiet - minimal output
pytest --collect-only -qq
```

#### **Output Format:**
```bash
$ pytest --collect-only -q
test_user.py::TestUserAuth::test_login
test_user.py::TestUserAuth::test_logout
test_user.py::TestUserProfile::test_update_profile
test_api.py::test_get_users
test_api.py::test_create_user[admin-user]
test_api.py::test_create_user[regular-user]
```

### Selective Test Execution:

#### **Run Specific Tests:**
```bash
# Run single test
pytest test_user.py::TestUserAuth::test_login

# Run parameterized test instance
pytest "test_api.py::test_create_user[admin-user]"

# Run test class
pytest test_user.py::TestUserAuth

# Run tests matching pattern
pytest -k "login or logout"
```

#### **Advanced Filtering:**
```bash
# Run tests with specific markers
pytest -m "slow"
pytest -m "not slow"
pytest -m "integration and not slow"

# Combine node ID with markers
pytest test_api.py -m "smoke"

# Run last failed tests
pytest --lf

# Run tests that failed, then continue with rest
pytest --ff
```

### Practical Applications:

#### **CI/CD Integration:**
```yaml
# GitHub Actions example
- name: List all tests
  run: pytest --collect-only -q > test_list.txt

- name: Run smoke tests
  run: pytest -m smoke

- name: Run specific test suite
  run: |
    for test in $(pytest --collect-only -q | grep "test_critical"); do
      pytest "$test" --tb=short
    done
```

#### **Development Workflow:**
```bash
# Find tests related to feature
pytest --collect-only -q | grep -i "user.*auth"

# Run subset during development
pytest --collect-only -q | grep "test_api" | head -5 | xargs pytest

# Test specific functionality
pytest --collect-only -q | grep -E "(login|logout|auth)" | xargs pytest -v
```

#### **Test Analysis:**
```python
# conftest.py - Collect test metadata
def pytest_collection_modifyitems(config, items):
    for item in items:
        # Add markers based on test names
        if "slow" in item.name:
            item.add_marker(pytest.mark.slow)
        if "integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        
        # Log test discovery
        print(f"Discovered: {item.nodeid}")
```

### Benefits:
- **Faster Feedback**: Run only relevant tests during development
- **CI Optimization**: Parallel test execution based on collection
- **Debugging**: Isolate and focus on specific failing tests
- **Documentation**: Test names serve as executable documentation

These tools and techniques represent different aspects of software development - cultural awareness, system-level debugging, and efficient testing practices.