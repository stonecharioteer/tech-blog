---
date: 2020-11-01T10:00:00+05:30
draft: false
title: "TIL: tr Command for Stream Translation and Character Manipulation"
description: "Today I learned how the tr command can translate stdin from one format to another, providing powerful text transformation capabilities in Unix pipelines."
tags:
  - til
  - unix
  - text-processing
  - streams
  - command-line
---

Today I discovered the versatile `tr` command for translating and manipulating character streams in Unix pipelines.

## Basic tr Command Usage

The `tr` (translate) command transforms characters from stdin according to specified rules:

### Character Translation:
```bash
# Convert lowercase to uppercase
echo "hello world" | tr 'a-z' 'A-Z'
# Output: HELLO WORLD

# Convert uppercase to lowercase  
echo "HELLO WORLD" | tr 'A-Z' 'a-z'
# Output: hello world

# Replace specific characters
echo "hello-world" | tr '-' '_'
# Output: hello_world

# Multiple character replacement
echo "hello world" | tr 'hw' 'HW'
# Output: Hello World
```

### Character Deletion:
```bash
# Delete specific characters
echo "hello123world456" | tr -d '0-9'
# Output: helloworld

# Delete whitespace
echo "hello   world" | tr -d ' '
# Output: helloworld

# Delete newlines (join lines)
cat multiline.txt | tr -d '\n'
```

### Character Sets and Ranges:
```bash
# Using predefined character classes
echo "Hello World 123!" | tr '[:upper:]' '[:lower:]'
# Output: hello world 123!

echo "Hello World 123!" | tr -d '[:punct:]'
# Output: Hello World 123

echo "Hello World 123!" | tr -d '[:digit:]'
# Output: Hello World !

# Available character classes:
# [:alnum:]  - alphanumeric characters
# [:alpha:]  - alphabetic characters  
# [:digit:]  - numeric characters
# [:lower:]  - lowercase letters
# [:upper:]  - uppercase letters
# [:punct:]  - punctuation characters
# [:space:]  - whitespace characters
```

## Advanced tr Operations

### Squeeze Repeated Characters:
```bash
# Squeeze multiple spaces into single space
echo "hello    world" | tr -s ' '
# Output: hello world

# Squeeze any whitespace
echo -e "hello\t\t\nworld" | tr -s '[:space:]'
# Output: hello world

# Remove duplicate characters
echo "hellooo wooorld" | tr -s 'o'
# Output: helo world
```

### Complement Operations:
```bash
# Keep only specified characters (delete complement)
echo "abc123def456" | tr -cd '[:digit:]'
# Output: 123456

# Delete everything except letters and spaces
echo "Hello, World! 123" | tr -cd '[:alpha:][:space:]'
# Output: Hello World
```

## Practical Use Cases

### Data Cleaning:
```bash
# Clean CSV data - replace commas with tabs
cat data.csv | tr ',' '\t'

# Remove Windows line endings
cat windows_file.txt | tr -d '\r'

# Convert DOS to Unix line endings
tr -d '\r' < dos_file.txt > unix_file.txt

# Clean phone numbers
echo "(555) 123-4567" | tr -cd '[:digit:]'
# Output: 5551234567
```

### Text Processing:
```bash
# ROT13 cipher
echo "hello" | tr 'a-zA-Z' 'n-za-mN-ZA-M'
# Output: uryyb

# Create URL-safe strings
echo "Hello World!" | tr '[:upper:][:space:][:punct:]' '[:lower:]--'
# Output: hello-world-

# Extract words (replace non-letters with newlines)
echo "hello,world;testing" | tr -cs '[:alpha:]' '\n'
# Output:
# hello
# world  
# testing
```

### Log Analysis:
```bash
# Count unique IP addresses in log
cat access.log | tr -s ' ' | cut -d' ' -f1 | sort | uniq -c

# Extract only numeric data from mixed content
cat mixed_data.txt | tr -cd '[:digit:]\n'

# Convert log timestamps
cat log.txt | tr ':' '-'  # Replace colons with dashes
```

### System Administration:
```bash
# Generate random passwords (simple method)
tr -cd '[:alnum:]' < /dev/urandom | head -c 16
# Output: aB3xK9mP2qR8vN4L

# Convert file paths
echo "/path/to/file" | tr '/' '\\'
# Output: \path\to\file

# Clean environment variables
echo "$PATH" | tr ':' '\n'  # Show PATH entries one per line
```

## Advanced Patterns

### Character Mapping Tables:
```bash
# Create substitution cipher
plaintext="abcdefghijklmnopqrstuvwxyz"
ciphertext="zyxwvutsrqponmlkjihgfedcba"
echo "secret message" | tr "$plaintext" "$ciphertext"
# Output: hvxivg nvhhztv

# Leetspeak conversion
echo "elite hacker" | tr 'eElLoOaAsS' '33110044$$'
# Output: 3lit3 h4ck3r
```

### Combining with Other Commands:
```bash
# Word frequency analysis
cat text.txt | tr -cs '[:alpha:]' '\n' | tr '[:upper:]' '[:lower:]' | sort | uniq -c | sort -nr

# Extract email domains
grep -o '[a-zA-Z0-9._%+-]*@[a-zA-Z0-9.-]*\.[a-zA-Z]*' emails.txt | tr '[:upper:]' '[:lower:]' | cut -d'@' -f2 | sort | uniq

# Convert camelCase to snake_case
echo "camelCaseVariable" | tr '[:upper:]' '[:lower:]' | sed 's/\([a-z]\)\([A-Z]\)/\1_\2/g'
```

### Performance Considerations:
```bash
# tr is very fast for simple transformations
time cat large_file.txt | tr '[:lower:]' '[:upper:]' > /dev/null

# For complex patterns, tr + other tools often faster than sed/awk
time cat large_file.txt | tr -d '[:punct:]' | tr -s '[:space:]' > /dev/null
```

The `tr` command is particularly valuable because it's designed for character-level transformations and is extremely fast, making it ideal for preprocessing data in complex pipelines before more sophisticated tools like `sed`, `awk`, or `grep` operate on it.