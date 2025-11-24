---
date: 2020-07-20T18:00:00+05:30
draft: false
title: "TIL: Curated Development Resources and Learning Paths"
description:
  "Today I learned about comprehensive curated lists of development resources,
  learning curricula, and specialized tools covering everything from CSS protips
  to computer science fundamentals and documentation systems."
tags:
  - til
  - resources
  - learning
  - curated-lists
  - computer-science
  - documentation
  - design
  - security
---

Today I discovered an extensive collection of curated resources that provide
structured learning paths and comprehensive toolkits for various aspects of
software development and computer science education.

## Curated Learning Resources

### Computer Science and Programming Fundamentals

[ossu Computer Science Curriculum](https://github.com/ossu/computer-science)
provides a complete computer science education equivalent to a university
degree:

```markdown
# OSSU Computer Science Curriculum Structure

## Intro CS

- **Python for Everybody Specialization** (University of Michigan)
- **Introduction to Computer Science and Programming** (MIT)

## Core CS

### Core Programming

- **How to Code** (University of British Columbia)
- **Programming Languages** (University of Washington)

### Core Math

- **Calculus 1A** (MIT)
- **Mathematics for Computer Science** (MIT)

### Core Systems

- **Build a Modern Computer** (Hebrew University)
- **Introduction to Computer Systems** (Carnegie Mellon)

### Core Theory

- **Algorithms Specialization** (Stanford)
- **Divide and Conquer, Sorting, Randomized Algorithms** (Stanford)

### Core Security

- **Cybersecurity Fundamentals** (Rochester Institute of Technology)
- **Principles of Secure Coding** (University of California, Davis)

### Core Applications

- **Databases** (Stanford)
- **Machine Learning** (Stanford)
- **Computer Graphics** (University of California, San Diego)

## Advanced CS

### Advanced Programming

- **Parallel Programming** (University of Illinois)
- **Compilers** (Stanford)

### Advanced Systems

- **Reliable Distributed Systems** (MIT)
- **Introduction to Operating Systems** (Georgia Tech)

### Advanced Theory

- **Introduction to Formal Logic** (Stanford)
- **Game Theory** (Stanford)

### Advanced Applications

- **Cryptography I** (Stanford)
- **Big Data Analytics** (Georgia Tech)
```

### Implementation of Self-Directed Learning

```python
# learning_tracker.py - Track progress through OSSU curriculum
import json
import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from enum import Enum

class CourseStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    AUDITED = "audited"  # Watched but didn't complete assignments

@dataclass
class Course:
    name: str
    provider: str
    url: str
    estimated_hours: int
    prerequisites: List[str]
    status: CourseStatus = CourseStatus.NOT_STARTED
    start_date: Optional[datetime.date] = None
    completion_date: Optional[datetime.date] = None
    notes: str = ""

@dataclass
class Subject:
    name: str
    courses: List[Course]

    def completion_percentage(self) -> float:
        if not self.courses:
            return 0.0
        completed = sum(1 for course in self.courses
                       if course.status == CourseStatus.COMPLETED)
        return (completed / len(self.courses)) * 100

class OSLearningTracker:
    """Track progress through self-directed learning curriculum"""

    def __init__(self, data_file: str = "learning_progress.json"):
        self.data_file = data_file
        self.subjects = self.load_curriculum()

    def load_curriculum(self) -> Dict[str, Subject]:
        """Load or create curriculum structure"""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                return self.deserialize_subjects(data)
        except FileNotFoundError:
            return self.create_default_curriculum()

    def create_default_curriculum(self) -> Dict[str, Subject]:
        """Create the default OSSU curriculum structure"""
        curriculum = {
            "intro_cs": Subject("Introduction to CS", [
                Course("Python for Everybody", "University of Michigan",
                      "https://www.coursera.org/specializations/python",
                      120, []),
                Course("Introduction to CS", "MIT",
                      "https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-0001-introduction-to-computer-science-and-programming-in-python-fall-2016/",
                      150, ["Python for Everybody"])
            ]),

            "core_programming": Subject("Core Programming", [
                Course("How to Code: Simple Data", "UBC",
                      "https://www.edx.org/course/how-to-code-simple-data",
                      60, ["Introduction to CS"]),
                Course("How to Code: Complex Data", "UBC",
                      "https://www.edx.org/course/how-to-code-complex-data",
                      60, ["How to Code: Simple Data"]),
                Course("Programming Languages A", "University of Washington",
                      "https://www.coursera.org/learn/programming-languages",
                      60, ["How to Code: Complex Data"])
            ]),

            "core_math": Subject("Core Mathematics", [
                Course("Calculus 1A", "MIT",
                      "https://www.edx.org/course/calculus-1a-differentiation",
                      80, []),
                Course("Mathematics for Computer Science", "MIT",
                      "https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-042j-mathematics-for-computer-science-spring-2015/",
                      120, ["Calculus 1A"])
            ]),

            "core_systems": Subject("Core Systems", [
                Course("Build a Modern Computer", "Hebrew University",
                      "https://www.coursera.org/learn/build-a-computer",
                      60, ["Core Programming"]),
                Course("Computer Systems", "Carnegie Mellon",
                      "https://www.coursera.org/learn/introduction-computer-systems",
                      80, ["Build a Modern Computer"])
            ]),

            "core_theory": Subject("Core Theory", [
                Course("Algorithms Specialization", "Stanford",
                      "https://www.coursera.org/specializations/algorithms",
                      160, ["Mathematics for Computer Science"]),
                Course("Data Structures", "UC San Diego",
                      "https://www.coursera.org/specializations/data-structures-algorithms",
                      120, ["Algorithms Specialization"])
            ])
        }

        return curriculum

    def start_course(self, subject_name: str, course_name: str):
        """Mark a course as started"""
        subject = self.subjects.get(subject_name)
        if not subject:
            print(f"Subject '{subject_name}' not found")
            return

        course = next((c for c in subject.courses if c.name == course_name), None)
        if not course:
            print(f"Course '{course_name}' not found in {subject_name}")
            return

        # Check prerequisites
        if not self.check_prerequisites(course):
            print(f"Prerequisites not met for '{course_name}'")
            return

        course.status = CourseStatus.IN_PROGRESS
        course.start_date = datetime.date.today()

        print(f"Started '{course_name}' in {subject_name}")
        self.save_progress()

    def complete_course(self, subject_name: str, course_name: str, notes: str = ""):
        """Mark a course as completed"""
        subject = self.subjects.get(subject_name)
        if not subject:
            return

        course = next((c for c in subject.courses if c.name == course_name), None)
        if not course:
            return

        course.status = CourseStatus.COMPLETED
        course.completion_date = datetime.date.today()
        course.notes = notes

        print(f"Completed '{course_name}' in {subject_name}!")
        self.save_progress()

        # Check for newly available courses
        self.suggest_next_courses()

    def check_prerequisites(self, course: Course) -> bool:
        """Check if all prerequisites are completed"""
        for prereq_name in course.prerequisites:
            prereq_completed = False
            for subject in self.subjects.values():
                for c in subject.courses:
                    if c.name == prereq_name and c.status == CourseStatus.COMPLETED:
                        prereq_completed = True
                        break
                if prereq_completed:
                    break

            if not prereq_completed:
                return False

        return True

    def suggest_next_courses(self):
        """Suggest courses that can be started now"""
        available_courses = []

        for subject_name, subject in self.subjects.items():
            for course in subject.courses:
                if (course.status == CourseStatus.NOT_STARTED and
                    self.check_prerequisites(course)):
                    available_courses.append((subject_name, course))

        if available_courses:
            print("\nAvailable courses you can start:")
            for subject_name, course in available_courses:
                print(f"  • {course.name} ({subject_name}) - {course.estimated_hours}h")

    def progress_report(self):
        """Generate comprehensive progress report"""
        print("=== Learning Progress Report ===\n")

        total_courses = 0
        completed_courses = 0
        in_progress_courses = 0
        total_hours = 0
        completed_hours = 0

        for subject_name, subject in self.subjects.items():
            subject_completed = sum(1 for c in subject.courses
                                  if c.status == CourseStatus.COMPLETED)
            subject_in_progress = sum(1 for c in subject.courses
                                    if c.status == CourseStatus.IN_PROGRESS)
            subject_total = len(subject.courses)

            print(f"📚 {subject.name}")
            print(f"   Progress: {subject_completed}/{subject_total} courses")
            print(f"   Percentage: {subject.completion_percentage():.1f}%")

            if subject_in_progress > 0:
                print(f"   In Progress: {subject_in_progress} courses")

            # Show individual course status
            for course in subject.courses:
                status_icon = {
                    CourseStatus.NOT_STARTED: "⭕",
                    CourseStatus.IN_PROGRESS: "🔄",
                    CourseStatus.COMPLETED: "✅",
                    CourseStatus.AUDITED: "👁️"
                }[course.status]

                print(f"     {status_icon} {course.name} ({course.estimated_hours}h)")
                if course.completion_date:
                    print(f"        Completed: {course.completion_date}")
                if course.notes:
                    print(f"        Notes: {course.notes}")

            print()

            # Update totals
            total_courses += subject_total
            completed_courses += subject_completed
            in_progress_courses += subject_in_progress

            for course in subject.courses:
                total_hours += course.estimated_hours
                if course.status == CourseStatus.COMPLETED:
                    completed_hours += course.estimated_hours

        # Overall statistics
        overall_percentage = (completed_courses / total_courses) * 100 if total_courses > 0 else 0

        print("📊 Overall Statistics:")
        print(f"   Courses: {completed_courses}/{total_courses} ({overall_percentage:.1f}%)")
        print(f"   Hours: {completed_hours}/{total_hours} ({(completed_hours/total_hours)*100:.1f}%)")
        print(f"   In Progress: {in_progress_courses} courses")

        # Time projections
        if in_progress_courses > 0:
            remaining_hours = total_hours - completed_hours
            print(f"   Estimated Remaining: {remaining_hours} hours")

            # Estimate completion time based on study rate
            hours_per_week = 10  # Configurable
            weeks_remaining = remaining_hours / hours_per_week
            completion_date = datetime.date.today() + datetime.timedelta(weeks=weeks_remaining)
            print(f"   Projected Completion: {completion_date} (at {hours_per_week}h/week)")

    def save_progress(self):
        """Save progress to JSON file"""
        data = {}
        for name, subject in self.subjects.items():
            data[name] = {
                'name': subject.name,
                'courses': [self.serialize_course(course) for course in subject.courses]
            }

        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)

    def serialize_course(self, course: Course) -> dict:
        """Convert course to serializable dictionary"""
        return {
            'name': course.name,
            'provider': course.provider,
            'url': course.url,
            'estimated_hours': course.estimated_hours,
            'prerequisites': course.prerequisites,
            'status': course.status.value,
            'start_date': course.start_date.isoformat() if course.start_date else None,
            'completion_date': course.completion_date.isoformat() if course.completion_date else None,
            'notes': course.notes
        }

    def deserialize_subjects(self, data: dict) -> Dict[str, Subject]:
        """Convert dictionary data back to Subject objects"""
        subjects = {}
        for key, subject_data in data.items():
            courses = []
            for course_data in subject_data['courses']:
                course = Course(
                    name=course_data['name'],
                    provider=course_data['provider'],
                    url=course_data['url'],
                    estimated_hours=course_data['estimated_hours'],
                    prerequisites=course_data['prerequisites'],
                    status=CourseStatus(course_data['status']),
                    start_date=datetime.date.fromisoformat(course_data['start_date']) if course_data['start_date'] else None,
                    completion_date=datetime.date.fromisoformat(course_data['completion_date']) if course_data['completion_date'] else None,
                    notes=course_data['notes']
                )
                courses.append(course)

            subjects[key] = Subject(subject_data['name'], courses)

        return subjects

# Command-line interface
def main():
    import argparse

    parser = argparse.ArgumentParser(description="Track learning progress through OSSU curriculum")
    parser.add_argument("--start", nargs=2, metavar=("SUBJECT", "COURSE"),
                       help="Start a course")
    parser.add_argument("--complete", nargs=2, metavar=("SUBJECT", "COURSE"),
                       help="Complete a course")
    parser.add_argument("--notes", help="Add notes when completing a course")
    parser.add_argument("--report", action="store_true", help="Show progress report")
    parser.add_argument("--suggest", action="store_true", help="Suggest next courses")

    args = parser.parse_args()

    tracker = OSLearningTracker()

    if args.start:
        tracker.start_course(args.start[0], args.start[1])
    elif args.complete:
        notes = args.notes or ""
        tracker.complete_course(args.complete[0], args.complete[1], notes)
    elif args.suggest:
        tracker.suggest_next_courses()
    else:
        tracker.progress_report()

if __name__ == "__main__":
    main()
```

## Specialized Development Resources

### CSS and Design Resources

[Awesome CSS Protips](https://github.com/AllThingsSmitty/css-protips) and
[Awesome Design Resources](https://github.com/gztchan/awesome-design) provide
curated design and styling knowledge:

```css
/* CSS Protips Implementation Examples */

/* 1. Use CSS Reset for consistent styling across browsers */
*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

/* 2. Inherit box-sizing for easier component styling */
html {
  box-sizing: border-box;
}

*,
*::before,
*::after {
  box-sizing: inherit;
}

/* 3. Use unset instead of undoing properties */
.button {
  all: unset;
  /* Then add only what you need */
  background: #007bff;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  cursor: pointer;
}

/* 4. Use :not() to apply/unapply borders on navigation */
.nav li:not(:last-child) {
  border-right: 1px solid #666;
}

/* 5. Add line-height to body for better text readability */
body {
  line-height: 1.6;
}

/* 6. Vertically center anything with flexbox */
.center-flex {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}

/* 7. Use comma-separated lists for font stacks */
body {
  font-family:
    "SF Pro Display",
    -apple-system,
    BlinkMacSystemFont,
    "Segoe UI",
    Roboto,
    Oxygen,
    Ubuntu,
    Cantarell,
    sans-serif;
}

/* 8. Use :empty to hide empty elements */
.empty-state:empty {
  display: none;
}

/* 9. Create smooth scrolling with scroll-behavior */
html {
  scroll-behavior: smooth;
}

/* 10. Use CSS custom properties for consistent theming */
:root {
  --primary-color: #007bff;
  --secondary-color: #6c757d;
  --success-color: #28a745;
  --danger-color: #dc3545;
  --warning-color: #ffc107;
  --info-color: #17a2b8;

  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.25rem;
  --font-size-xl: 1.5rem;

  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 3rem;

  --border-radius: 0.375rem;
  --box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24);
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  :root {
    --bg-color: #121212;
    --text-color: #ffffff;
    --border-color: #333333;
  }
}

/* 11. Use aspect-ratio for responsive images */
.aspect-ratio-16-9 {
  aspect-ratio: 16 / 9;
  object-fit: cover;
  width: 100%;
}

/* 12. Use CSS Grid for complex layouts */
.grid-layout {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--spacing-md);
  padding: var(--spacing-md);
}

/* 13. Use clamp() for responsive typography */
h1 {
  font-size: clamp(1.5rem, 4vw, 3rem);
}

/* 14. Use focus-visible for better accessibility */
.button:focus-visible {
  outline: 2px solid var(--primary-color);
  outline-offset: 2px;
}

/* 15. Use CSS logical properties for internationalization */
.content {
  margin-inline-start: var(--spacing-md);
  padding-block: var(--spacing-sm) var(--spacing-md);
  border-inline-start: 3px solid var(--primary-color);
}

/* 16. Use container queries for component-based responsive design */
@container (min-width: 400px) {
  .card {
    display: flex;
    align-items: center;
  }

  .card-image {
    width: 150px;
    flex-shrink: 0;
  }
}

/* 17. Advanced selectors for form validation */
input:user-invalid {
  border-color: var(--danger-color);
}

input:user-valid {
  border-color: var(--success-color);
}

/* 18. Use :has() for parent selection */
.form-group:has(input:user-invalid) label {
  color: var(--danger-color);
}

/* 19. Modern CSS reset */
*,
*::before,
*::after {
  box-sizing: border-box;
}

body {
  margin: 0;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

img,
picture,
video,
canvas,
svg {
  display: block;
  max-width: 100%;
}

input,
button,
textarea,
select {
  font: inherit;
}

p,
h1,
h2,
h3,
h4,
h5,
h6 {
  overflow-wrap: break-word;
}

/* 20. Utility classes following atomic CSS principles */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

.flow > * + * {
  margin-top: var(--flow-space, 1rem);
}

.cluster {
  display: flex;
  flex-wrap: wrap;
  gap: var(--cluster-space, 1rem);
  justify-content: flex-start;
  align-items: center;
}

.sidebar {
  display: flex;
  flex-wrap: wrap;
  gap: var(--sidebar-space, 1rem);
}

.sidebar > :first-child {
  flex-basis: var(--sidebar-width, 250px);
  flex-grow: 1;
}

.sidebar > :last-child {
  flex-basis: 0;
  flex-grow: 999;
  min-width: 50%;
}
```

### Security and Penetration Testing

[Awesome Penetration Test](https://github.com/enaqx/awesome-pentest) provides
comprehensive security testing resources:

```python
# security_checklist.py - Implementation of security best practices
import hashlib
import secrets
import hmac
import re
from typing import Dict, List, Optional
import logging
from datetime import datetime, timedelta
import bcrypt

class SecurityValidator:
    """Implement common security validation patterns"""

    def __init__(self):
        self.failed_attempts: Dict[str, List[datetime]] = {}
        self.rate_limit_window = timedelta(minutes=15)
        self.max_attempts = 5

    def validate_password_strength(self, password: str) -> Dict[str, bool]:
        """Validate password against security requirements"""
        checks = {
            'min_length': len(password) >= 12,
            'has_uppercase': re.search(r'[A-Z]', password) is not None,
            'has_lowercase': re.search(r'[a-z]', password) is not None,
            'has_digit': re.search(r'\d', password) is not None,
            'has_special': re.search(r'[!@#$%^&*(),.?":{}|<>]', password) is not None,
            'no_common_patterns': not self.has_common_patterns(password),
            'no_personal_info': True  # Would check against user data in real implementation
        }

        checks['is_strong'] = all(checks.values())
        return checks

    def has_common_patterns(self, password: str) -> bool:
        """Check for common weak password patterns"""
        common_patterns = [
            r'123456',
            r'password',
            r'qwerty',
            r'abc123',
            r'admin',
            r'(.)\1{3,}',  # Repeated characters
            r'(012|123|234|345|456|567|678|789)',  # Sequential numbers
        ]

        lower_password = password.lower()
        return any(re.search(pattern, lower_password) for pattern in common_patterns)

    def hash_password(self, password: str) -> str:
        """Securely hash password using bcrypt"""
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    def generate_secure_token(self, length: int = 32) -> str:
        """Generate cryptographically secure random token"""
        return secrets.token_urlsafe(length)

    def generate_csrf_token(self, user_id: str, secret_key: str) -> str:
        """Generate CSRF token tied to user session"""
        timestamp = str(int(datetime.now().timestamp()))
        message = f"{user_id}:{timestamp}"
        signature = hmac.new(
            secret_key.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        return f"{message}:{signature}"

    def verify_csrf_token(self, token: str, user_id: str, secret_key: str,
                         max_age: int = 3600) -> bool:
        """Verify CSRF token"""
        try:
            parts = token.split(':')
            if len(parts) != 3:
                return False

            token_user_id, timestamp, signature = parts

            # Check user ID matches
            if token_user_id != user_id:
                return False

            # Check token age
            token_time = datetime.fromtimestamp(int(timestamp))
            if datetime.now() - token_time > timedelta(seconds=max_age):
                return False

            # Verify signature
            message = f"{token_user_id}:{timestamp}"
            expected_signature = hmac.new(
                secret_key.encode(),
                message.encode(),
                hashlib.sha256
            ).hexdigest()

            return hmac.compare_digest(signature, expected_signature)

        except (ValueError, TypeError):
            return False

    def check_rate_limit(self, identifier: str) -> bool:
        """Check if identifier is rate limited"""
        now = datetime.now()

        # Clean old attempts
        if identifier in self.failed_attempts:
            self.failed_attempts[identifier] = [
                attempt for attempt in self.failed_attempts[identifier]
                if now - attempt < self.rate_limit_window
            ]

        # Check current attempt count
        attempt_count = len(self.failed_attempts.get(identifier, []))
        return attempt_count < self.max_attempts

    def record_failed_attempt(self, identifier: str):
        """Record a failed authentication attempt"""
        if identifier not in self.failed_attempts:
            self.failed_attempts[identifier] = []

        self.failed_attempts[identifier].append(datetime.now())

        logging.warning(f"Failed authentication attempt for {identifier}")

    def sanitize_input(self, input_string: str) -> str:
        """Basic input sanitization"""
        # Remove null bytes
        sanitized = input_string.replace('\x00', '')

        # Remove control characters except newline and tab
        sanitized = ''.join(char for char in sanitized
                          if char.isprintable() or char in '\n\t')

        # Limit length
        return sanitized[:1000]

    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def check_sql_injection_patterns(self, input_string: str) -> bool:
        """Check for common SQL injection patterns"""
        dangerous_patterns = [
            r"(?i)(union|select|insert|update|delete|drop|create|alter|exec|execute)",
            r"[';\"]\s*(--)?\s*(union|select|insert|update|delete)",
            r"(?i)(script|javascript|vbscript|onload|onerror)",
            r"(?i)(\<|\>|&lt|&gt)",  # Basic XSS patterns
        ]

        return any(re.search(pattern, input_string) for pattern in dangerous_patterns)

# Security headers implementation
class SecurityHeaders:
    """Generate security headers for web applications"""

    @staticmethod
    def get_security_headers() -> Dict[str, str]:
        """Get comprehensive security headers"""
        return {
            # Prevent MIME type sniffing
            'X-Content-Type-Options': 'nosniff',

            # Enable XSS protection
            'X-XSS-Protection': '1; mode=block',

            # Prevent clickjacking
            'X-Frame-Options': 'DENY',

            # HSTS for HTTPS enforcement
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains; preload',

            # Content Security Policy
            'Content-Security-Policy':
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "connect-src 'self'; "
                "font-src 'self'; "
                "object-src 'none'; "
                "media-src 'self'; "
                "frame-src 'none';",

            # Referrer policy
            'Referrer-Policy': 'strict-origin-when-cross-origin',

            # Feature policy
            'Permissions-Policy':
                "geolocation=(), "
                "microphone=(), "
                "camera=(), "
                "payment=(), "
                "usb=(), "
                "magnetometer=(), "
                "gyroscope=(), "
                "speaker=()",
        }

    @staticmethod
    def get_api_security_headers() -> Dict[str, str]:
        """Get security headers specific to APIs"""
        headers = SecurityHeaders.get_security_headers()

        # API-specific modifications
        headers.update({
            'X-API-Version': '1.0',
            'Cache-Control': 'no-store, no-cache, must-revalidate, private',
            'Pragma': 'no-cache',
            'Expires': '0',
        })

        return headers

# Example usage and testing
def demonstrate_security_practices():
    """Demonstrate security validation implementation"""
    validator = SecurityValidator()

    # Password strength testing
    test_passwords = [
        "password123",           # Weak
        "MySecureP@ssw0rd!2024", # Strong
        "12345678",              # Very weak
        "Th1s1sMyStr0ngP@ssw0rd!", # Strong
    ]

    print("=== Password Strength Analysis ===")
    for password in test_passwords:
        strength = validator.validate_password_strength(password)
        print(f"\nPassword: {password}")
        print(f"Strong: {'✅' if strength['is_strong'] else '❌'}")
        for check, passed in strength.items():
            if check != 'is_strong':
                print(f"  {check}: {'✅' if passed else '❌'}")

    # Token generation
    print(f"\n=== Secure Tokens ===")
    print(f"Random token: {validator.generate_secure_token()}")
    print(f"CSRF token: {validator.generate_csrf_token('user123', 'secret_key')}")

    # Security headers
    print(f"\n=== Security Headers ===")
    headers = SecurityHeaders.get_security_headers()
    for header, value in headers.items():
        print(f"{header}: {value}")

if __name__ == "__main__":
    demonstrate_security_practices()
```

## Documentation and Knowledge Management

### Documentation System Philosophy

[Divio's Documentation System](https://www.divio.com/blog/documentation/) and
[What Nobody Tells You about Documentation](https://www.youtube.com/watch?v=t4vKPhjcMZg)
provide the definitive framework for documentation:

```markdown
# The Four Types of Documentation

## 1. Tutorials (Learning-Oriented)

**Purpose**: Enable newcomers to get started **Characteristics**:

- Step-by-step instructions
- Focus on immediate success
- No explanations of why
- Reproducible results

**Example Structure**:
```

# Getting Started with Our API

## Prerequisites

- Python 3.8+
- API key from our dashboard

## Step 1: Install the SDK

```bash
pip install our-api-sdk
```

## Step 2: Make Your First Request

```python
from our_api import Client

client = Client(api_key="your_key_here")
response = client.users.list()
print(response.data)
```

## Step 3: Verify the Response

You should see output similar to:

```json
{
  "users": [
    { "id": 1, "name": "Alice" },
    { "id": 2, "name": "Bob" }
  ]
}
```

Next Steps:

- Read our How-To Guides for common tasks
- Check the API Reference for full details

```

## 2. How-To Guides (Problem-Oriented)
**Purpose**: Show how to solve specific problems
**Characteristics**:
- Goal-oriented
- Assume some knowledge
- Focus on practical steps
- Real-world scenarios

**Example Structure**:
```

# How to Implement User Authentication

## Problem

You need to add secure user authentication to your application.

## Solution Overview

We'll use JWT tokens with refresh token rotation for security.

## Step-by-Step Implementation

### 1. Set up authentication endpoints

```python
@app.route('/auth/login', methods=['POST'])
def login():
    credentials = request.get_json()
    user = authenticate_user(credentials)
    if user:
        tokens = generate_tokens(user.id)
        return jsonify(tokens)
    return jsonify({'error': 'Invalid credentials'}), 401
```

### 2. Implement token validation middleware

[Detailed implementation...]

### 3. Handle token refresh

[Refresh logic...]

## Testing Your Implementation

[Test cases and validation steps...]

## Security Considerations

- Always use HTTPS in production
- Set appropriate token expiration times
- Implement rate limiting

```

## 3. Reference (Information-Oriented)
**Purpose**: Provide comprehensive information
**Characteristics**:
- Complete and accurate
- Structured and organized
- Factual descriptions
- Easy to search

**Example Structure**:
```

# API Reference

## Authentication

All API requests require authentication via Bearer token.

### Headers

| Header        | Required | Description      |
| ------------- | -------- | ---------------- |
| Authorization | Yes      | Bearer {token}   |
| Content-Type  | Yes      | application/json |

## Endpoints

### GET /users

Retrieve a list of users.

**Parameters**: | Parameter | Type | Required | Description |
|-----------|------|----------|-------------| | page | integer | No | Page
number (default: 1) | | limit | integer | No | Items per page (default: 20,
max: 100) | | search | string | No | Search term for filtering |

**Response**:

```json
{
  "users": [
    {
      "id": 1,
      "name": "Alice Smith",
      "email": "alice@example.com",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "pages": 5
  }
}
```

**Error Responses**: | Status | Description | |--------|-------------| | 401 |
Unauthorized | | 403 | Forbidden | | 422 | Validation Error |

```

## 4. Explanation (Understanding-Oriented)
**Purpose**: Explain the why and how
**Characteristics**:
- Provide context and background
- Discuss alternatives and trade-offs
- Explain design decisions
- Connect concepts

**Example Structure**:
```

# Understanding Our Authentication Architecture

## Why JWT Tokens?

Traditional session-based authentication stores session data on the server,
which creates several challenges in distributed systems:

1. **Scalability**: Session storage becomes a bottleneck
2. **Statelessness**: Violates REST principles
3. **Mobile Support**: Cookies don't work well with mobile apps

JWT (JSON Web Tokens) solve these problems by:

- Encoding user information in the token itself
- Eliminating server-side session storage
- Working seamlessly across platforms

## Token Structure

A JWT consists of three parts separated by dots:

```
header.payload.signature
```

### Header

Contains metadata about the token:

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

### Payload

Contains the claims (user data):

```json
{
  "sub": "1234567890",
  "name": "John Doe",
  "exp": 1516239022
}
```

### Signature

Ensures token integrity:

```
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  secret
)
```

## Security Considerations

### Token Expiration

We use short-lived access tokens (15 minutes) paired with longer-lived refresh
tokens (7 days) to balance security and user experience.

### Refresh Token Rotation

Each time a refresh token is used, we issue a new refresh token and invalidate
the old one. This limits the impact of token compromise.

## Alternative Approaches

### OAuth 2.0

For applications requiring third-party authentication, OAuth 2.0 provides a
standard framework. However, it adds complexity that may not be necessary for
first-party applications.

### Session-based Authentication

Still appropriate for traditional web applications where all requests come from
the same origin and session storage isn't a bottleneck.

```

```

This documentation framework ensures comprehensive coverage while serving
different user needs and contexts.
