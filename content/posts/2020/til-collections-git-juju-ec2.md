---
date: "2020-08-01T23:59:59+05:30"
draft: false
title: "TIL: Python Collections, Git Commands, Juju, and EC2"
tags:
  [
    "til",
    "python",
    "collections",
    "git",
    "juju",
    "aws",
    "ec2",
    "cloud",
    "devops",
  ]
---

## Python Programming

### Collections Module - defaultdict

- `collections.defaultdict` takes a _type_ not a value
- It will initialize based on the default value for that type
- Common mistake: passing a value instead of a callable type
- Example: `defaultdict(list)` not `defaultdict([])`
- Cleaner than manually checking if keys exist before accessing

## Version Control

### Git Commands and Tricks

- `git log --format="%H" -n 1 | cat` outputs the last commit ID
- Useful for scripting and automation
- The `cat` ensures the output is properly formatted
- `%H` format specifier gives the full commit hash
- `-n 1` limits to the most recent commit

## Cloud Infrastructure and DevOps

### AWS EC2 Free Tier

- EC2 has a Free tier! I can request a bunch of machines here
- Great for learning and experimenting with cloud infrastructure
- Limited resources but sufficient for development and testing
- Good entry point for understanding cloud computing concepts

### Juju - Multi-Cloud Orchestration

- Juju is a tool that helps manage server providers, whether they are GCP, AWS,
  your own servers or Azure, among others
- Gives you one way to start, setup and run your servers across different cloud
  providers
- Abstracts away cloud provider differences
- Enables consistent deployment across hybrid and multi-cloud environments

#### Juju Configuration System

- Juju's configurations are called charms
- These are written in Python
- Charms define how services should be deployed and configured
- Reusable deployment patterns for common software stacks
- Community-maintained charm store with pre-built configurations
