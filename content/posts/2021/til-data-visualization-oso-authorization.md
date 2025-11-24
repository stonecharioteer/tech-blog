---
date: 2021-04-16T10:00:00+05:30
draft: false
title: "TIL: Data Visualization Guide and Oso Authorization Academy"
description:
  "Today I learned about Anton Zhiyanov's comprehensive data visualization guide
  and Oso's Authorization Academy for learning modern authorization patterns and
  best practices."
tags:
  - TIL
  - Data Visualization
  - Authorization
  - Security
  - Design
---

## Data Visualization Guide

[Data Visualization Guide | Anton Zhiyanov](https://antonz.org/dataviz-guide/)

Comprehensive guide to creating effective data visualizations:

### Core Principles:

#### **Clarity Over Complexity:**

- **Simple is Better**: Avoid unnecessary chart elements
- **Clear Labels**: Make axes and legends self-explanatory
- **Focused Message**: Each chart should communicate one main point
- **Appropriate Scale**: Choose scales that don't mislead

#### **Chart Type Selection:**

- **Bar Charts**: For comparing discrete categories
- **Line Charts**: For showing trends over time
- **Scatter Plots**: For showing relationships between variables
- **Heat Maps**: For showing patterns in matrix data

#### **Color and Design:**

- **Meaningful Colors**: Use color to encode information, not just decoration
- **Accessibility**: Consider colorblind-friendly palettes
- **Consistency**: Maintain consistent color schemes across related charts
- **Contrast**: Ensure sufficient contrast for readability

### Best Practices:

- **Know Your Audience**: Tailor complexity to viewer expertise
- **Tell a Story**: Guide viewers through the data narrative
- **Provide Context**: Include benchmarks and comparisons
- **Test Comprehension**: Verify that viewers understand the message

### Common Mistakes to Avoid:

- Misleading scales or truncated axes
- Too many colors or visual elements
- Charts that don't match the data type
- Missing context or explanatory text

## Oso Authorization Academy

[Oso - Authorization Academy](https://www.osohq.com/developers/authorization-academy)

Educational resource for learning modern authorization patterns:

### What is Authorization:

- **Different from Authentication**: Authentication verifies identity,
  authorization determines permissions
- **Fine-Grained Control**: Beyond simple role-based access control
- **Context-Aware**: Permissions based on relationships, attributes, and context
- **Scalable Patterns**: Authorization systems that grow with applications

### Key Concepts Covered:

#### **Authorization Models:**

- **Role-Based Access Control (RBAC)**: Users have roles, roles have permissions
- **Attribute-Based Access Control (ABAC)**: Decisions based on attributes
- **Relationship-Based Access Control (ReBAC)**: Permissions based on
  relationships
- **Policy-Based Access Control**: Centralized policy management

#### **Implementation Patterns:**

- **Policy Engines**: Centralized authorization decision points
- **Policy Languages**: Domain-specific languages for expressing policies
- **Enforcement Points**: Where authorization checks are performed
- **Information Points**: Sources of attributes for authorization decisions

### Modern Authorization Challenges:

- **Microservices**: Distributed authorization across services
- **Multi-Tenancy**: Isolation and sharing in SaaS applications
- **Dynamic Policies**: Policies that change based on context
- **Performance**: Fast authorization decisions at scale

### Why It Matters:

- **Security**: Proper authorization prevents unauthorized access
- **Compliance**: Meet regulatory requirements for access control
- **User Experience**: Smooth, context-aware permissions
- **Maintainability**: Clear, auditable authorization logic

Both resources provide essential knowledge for their respective domains -
effective data communication and secure application design.
