---
date: 2020-12-09T10:00:00+05:30
draft: false
title: "TIL: Bill Gates' 2020 Book Recommendations, Game Cartridge History, and OSO Authorization"
description: "Today I learned about Bill Gates' thoughtful book recommendations for 2020, the fascinating untold story of video game cartridge invention, and OSO's approach to application authorization."
tags:
  - til
  - books
  - reading
  - gaming-history
  - authorization
  - security
---

Today's learning combined thoughtful reading recommendations, gaming industry history, and modern security architecture.

## Bill Gates' 2020 Book Recommendations

[5 good books for a lousy year](https://www.gatesnotes.com/About-Bill-Gates/Holiday-Books-2020) presents Bill Gates' carefully curated reading list for 2020, focusing on books that provide perspective during challenging times.

### The Selection Criteria
Gates chose books that:
- **Offer hope and perspective** during difficult global circumstances
- **Span diverse topics** from science to biography to fiction
- **Provide intellectual escape** while maintaining relevance to current challenges
- **Come from trusted authors** with proven track records

### Why This Matters
These annual recommendations are valuable because:
- **Curated expertise**: Gates' broad reading and analytical approach
- **Global perspective**: Books chosen for universal appeal and insight
- **Timing sensitivity**: Selected specifically for their relevance to 2020's challenges
- **Proven impact**: Previous recommendations have consistently been worthwhile reads

The list demonstrates how thoughtful reading can provide both comfort and growth during uncertain times.

## The Untold Story of Game Cartridge Invention

[The Untold Story Of The Invention Of The Game Cartridge](https://www.fastcompany.com/3040889/the-untold-story-of-the-invention-of-the-game-cartridge) reveals the fascinating engineering and business decisions that led to one of gaming's most important innovations.

### Key Historical Points

#### **Technical Innovation:**
- **ROM-based storage**: Moving from arcade boards to removable cartridges
- **Licensing control**: Hardware design that prevented unauthorized games
- **Cost considerations**: Balancing manufacturing costs with functionality
- **Durability requirements**: Handling by consumers vs. arcade maintenance

#### **Business Strategy:**
- **Platform control**: Nintendo's masterful use of cartridge design for market dominance
- **Third-party relationships**: How cartridge specifications shaped developer relationships
- **Market differentiation**: Cartridges vs. floppy disks in early home computing

#### **Cultural Impact:**
- **Game collecting**: Cartridges as physical objects with intrinsic value
- **Software distribution**: Pre-internet content delivery challenges
- **User experience**: Instant loading vs. floppy disk inconvenience

### Lessons for Modern Tech
- **Hardware as platform strategy**: Physical design can enforce business models
- **User experience priorities**: Sometimes reliability trumps cost optimization
- **Ecosystem thinking**: Individual components must serve broader platform goals

## OSO Authorization Framework

[OSO Documentation](https://docs.osohq.com/index.html) introduces a modern approach to application authorization, moving beyond simple role-based access control.

### Core Concepts

#### **Policy-as-Code:**
- **Declarative permissions**: Express authorization logic in readable policy language
- **Version control**: Authorization rules managed like any other code
- **Testing capabilities**: Unit tests for permission logic
- **Audit trails**: Track changes to authorization policies

#### **Framework Integration:**
```python
# Example OSO policy definition
allow(actor: User, "read", resource: Document) if
    actor.role = "admin" or
    actor.id = resource.owner_id or
    resource.public = true;

allow(actor: User, "write", resource: Document) if
    actor.role = "admin" or
    actor.id = resource.owner_id;
```

### Advantages Over Traditional RBAC

#### **Flexibility:**
- **Context-aware permissions**: Consider resource attributes, time, location
- **Complex relationships**: Handle organizational hierarchies and delegation
- **Dynamic policies**: Rules that adapt based on application state

#### **Maintainability:**
- **Centralized logic**: Authorization rules in one place
- **Clear reasoning**: Understand why permissions were granted or denied
- **Incremental changes**: Modify policies without application rewrites

These discoveries highlight the value of curated learning resources, understanding the historical context of technological decisions, and adopting modern approaches to perennial software engineering challenges.