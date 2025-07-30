---
date: 2021-01-29T10:00:00+05:30
draft: false
title: "TIL: Kubernetes Environment Variables, kubectl tree, Git CLI, SSH, and Typing Practice"
description: "Today I learned about Kubernetes environment variable injection, kubectl tree plugin for object hierarchy visualization, enhanced Git CLI tools, SSH host key management, and online typing practice."
tags:
  - kubernetes
  - kubectl
  - git
  - ssh
  - typing
  - cli-tools
  - productivity
---

## Kubernetes Configuration

### Environment Variables for Containers
- [Define Environment Variables for a Container | Kubernetes](https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/)
- Official Kubernetes documentation on injecting environment variables
- Multiple methods: direct values, ConfigMaps, Secrets, and field references
- Essential for application configuration in containerized environments

### Environment Variable Sources
- **Direct Values**: Hardcoded values in pod specifications
- **ConfigMaps**: External configuration data
- **Secrets**: Sensitive configuration data
- **Field References**: Pod and container metadata
- **Resource References**: CPU and memory limits/requests

## Kubernetes Tools

### kubectl tree Plugin
- [GitHub - ahmetb/kubectl-tree](https://github.com/ahmetb/kubectl-tree)
- kubectl plugin to browse Kubernetes object hierarchies as trees
- Visualize relationships between Kubernetes resources
- Helpful for understanding complex deployments and dependencies

### Tree Visualization Benefits
- **Resource Relationships**: See parent-child relationships clearly
- **Dependency Tracking**: Understand how resources connect
- **Debugging**: Identify missing or misconfigured resources
- **Learning**: Better understand Kubernetes object model

## Development Tools

### Gitsome - Enhanced Git CLI
- [GitHub - donnemartin/gitsome](https://github.com/donnemartin/gitsome)
- Supercharged Git/GitHub command line interface
- Official GitHub integration with enhanced functionality
- Autocomplete, syntax highlighting, and GitHub-specific commands

### Gitsome Features
- **GitHub Integration**: Direct GitHub API access from command line
- **Enhanced Commands**: Improved git commands with additional functionality
- **Autocomplete**: Intelligent command and argument completion
- **Syntax Highlighting**: Colorized output for better readability

## System Administration

### SSH Host Key Management
- [HowTo: Disable SSH Host Key Checking - ShellHacks](shellhacks.com/disable-ssh-host-key-checking/)
- Methods to disable SSH host key verification
- Useful for automation and dynamic environments
- Important security considerations when disabling checks

### SSH Configuration Options
- **StrictHostKeyChecking**: Control host key verification behavior
- **UserKnownHostsFile**: Specify known hosts file location
- **Global vs User**: System-wide vs user-specific configuration
- **Security Trade-offs**: Convenience vs security implications

## Productivity Tools

### Monkeytype - Typing Practice
- [Monkeytype](http://monkeytype.com/)
- Modern, customizable typing test and practice platform
- Various test modes, themes, and difficulty levels
- Track progress and improve typing speed and accuracy

### Typing Practice Benefits
- **Developer Productivity**: Faster typing improves coding efficiency
- **Customizable Tests**: Different languages, lengths, and difficulty
- **Progress Tracking**: Monitor improvement over time
- **Modern Interface**: Clean, distraction-free design

## Key Takeaways

- **Configuration Management**: Kubernetes provides flexible ways to inject configuration
- **Visualization Tools**: Tree views help understand complex resource relationships
- **CLI Enhancement**: Tools like gitsome can significantly improve command-line productivity
- **Automation vs Security**: Balance convenience with security in SSH configurations
- **Skill Development**: Improving typing skills has long-term productivity benefits

These tools and techniques span from infrastructure management to personal productivity, showing the breadth of skills needed in modern development workflows.