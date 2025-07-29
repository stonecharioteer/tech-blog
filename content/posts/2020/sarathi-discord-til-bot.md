---
date: 2020-11-30T10:00:00+05:30
draft: false
title: "Sarathi - A Personal Discord Bot for TIL Management"
description: "Building a Discord bot to automate my Today I Learned (TIL) workflow - from manual WhatsApp notes to automated GitHub commits with search capabilities."
tags:
  - discord
  - python
  - til
  - automation
  - bot-development
  - github-integration
  - show-and-tell
  - productivity
  - jinja2
  - json
---

{{< warning title="Project Status - Deprecated" >}}
**Sarathi has been deprecated** since I migrated this blog to Hugo. My TIL workflow has evolved significantly - I now use GenAI-powered tools to create comprehensive TIL posts from my learning archive, generating detailed technical content that goes far beyond simple link collection. This post remains as documentation of an interesting automation project from my pre-Hugo days.
{{< /warning >}}

I've been maintaining [a TIL (Today I Learned) page](https://stonecharioteer.com/til.html) for a while now, and while the idea is great, I have had some issues updating the sheet daily. The manual workflow was becoming a bottleneck in my learning documentation process.

## The Problem with Manual TIL Management

My original flow looked like this:

1. **Discovery**: Whenever I find a link or factoid interesting, I save them in a WhatsApp group where I'm the only member for later record
2. **Manual Transfer**: Add these to the TIL page whenever I could find time
3. **Reality**: Lately, I've not been able to keep up with the manual updates

The problems with this approach were numerous:

{{< warning title="Manual Process Issues" >}}
- **Too Manual**: This is against everything I believe in - I automate everything I can
- **Poor Searchability**: Finding links is hard unless I'm using `ripgrep` on a non-mobile device  
- **Difficult Maintenance**: Categorizing things and updating the look of my TIL page is cumbersome
- **Mobile Unfriendly**: Hard to update when away from my development machine
{{< /warning >}}

I had been meaning to leverage a Telegram bot for this task for quite some time, but never got around to actually building it. This weekend, as I prepped myself to shift my body clock to attend [David Beazley's RAFT Course](http://dabeaz.com/raft.html), I decided to use the midnight oil to write my own bot.

## Why Discord Over Telegram?

I've been using Discord to talk to friends and communities lately, and I've found its integration with Linux to be amazing. Here's why I chose Discord:

### **Platform Benefits**
- **Cross-Platform**: Excellent web UI, desktop app that works well everywhere
- **Mobile Support**: Great mobile app for phones and tablets  
- **Linux Integration**: Seamless experience on my primary development platform
- **API Quality**: Robust Python library with comprehensive documentation

### **Developer Experience**
- **Rich API**: Discord's API is well-designed and feature-complete
- **Python Library**: [`discord.py`](https://discordpy.readthedocs.io/) provides excellent abstractions
- **Community**: Large developer community with good examples and support

## Development Resources

I relied on several key resources for building Sarathi:

1. **[Real Python Discord Bot Tutorial](https://realpython.com/how-to-make-a-discord-bot-python/)** - Excellent starting point
2. **[Discord Official Documentation](https://discord.com/developers/docs/intro)** - Comprehensive API reference  
3. **[`discord.py` Documentation](https://discordpy.readthedocs.io/)** - Library-specific guidance

{{< note title="Documentation Quality" >}}
One observation: The Discord API is robust, but the `discord.py` documentation leaves something to be desired. However, users of `click` will really understand how this library is architected - the patterns are very similar.
{{< /note >}}

## Bot Goals and Features

I wanted Sarathi to handle the complete TIL workflow automatically:

### **Core Functionality**
1. **Input Processing**: Parse arbitrary commands for URLs or factoids
2. **Content Extraction**: Extract titles from URLs automatically
3. **Data Management**: Maintain a time-based JSON file in my blog's GitHub repository
4. **Git Integration**: Automatically commit the JSON to GitHub
5. **Site Generation**: Regenerate the `til.md` file using Jinja2 templates
6. **Auto-Deploy**: Push code to GitHub for instant blog updates
7. **Search API**: Query the knowledge base with simple search functionality

### **Smart Features**
- **Duplicate Detection**: Prevent adding the same TIL on the same date
- **Repetition Tracking**: Track when I encounter previously recorded information
- **Category Management**: Organize TILs with space-separated category tags
- **Mobile-First**: Designed for easy use from Discord mobile app

## Bot in Action

Let me show you how Sarathi works in practice:

### **Help Command**
The bot uses `/` as a command prefix and provides comprehensive help:

```
/help - Show all available commands
/til add <url> <categories> - Add a URL to TIL with categories
/til add <factoid> <categories> - Add a text factoid to TIL  
/til find <search-string> - Search existing TIL entries
```

{{< example title="Adding a URL" >}}
**Command**: `/til add https://example.com/article python automation`

**Result**: Sarathi extracts the page title, adds it to the JSON database with today's date, commits to GitHub, regenerates the TIL page, and confirms the addition.
{{< /example >}}

### **Duplicate Prevention**
If you try adding the same TIL on the same date, Sarathi provides intelligent feedback:

{{< tip title="Smart Duplicate Handling" >}}
- **Same Day**: "You just learned this today!"
- **Different Day**: Adds to `repeated_added_on` field for learning pattern analysis
- **Future Analysis**: Could help identify gaps in my learning retention
{{< /tip >}}

### **Factoid Support**
Not all TILs are links - sometimes they're just interesting facts:

```
/til add "Python's GIL can be released using C extensions" python performance
```

Sarathi handles both URLs and plain text factoids seamlessly.

### **Search Functionality**
Query your accumulated knowledge instantly:

```
/til find python regex
```

The search matches against:
- **Categories**: Tagged topics and themes
- **Content**: URL titles and factoid text  
- **Context**: Any metadata associated with entries

## Technical Architecture

### **Core Technologies**
- **Python**: Primary development language
- **discord.py**: Discord API integration
- **Beautiful Soup**: Web scraping for URL title extraction
- **Jinja2**: Template engine for TIL page generation
- **Git/GitHub**: Version control and hosting
- **JSON**: Simple, readable data storage format

### **Workflow Automation**
1. **Discord Input** → Parse command and extract data
2. **Content Processing** → Fetch URL titles, validate input
3. **Database Update** → Add to JSON with timestamps and categories
4. **Git Operations** → Commit changes with descriptive messages
5. **Site Regeneration** → Use Jinja2 templates to rebuild TIL page
6. **Deployment** → Push to GitHub for instant site updates

### **Data Structure**
```json
{
  "2020-11-30": [
    {
      "type": "url",
      "url": "https://example.com/article",
      "title": "Extracted Page Title",
      "categories": ["python", "automation"],
      "added_at": "2020-11-30T10:30:00Z",
      "repeated_added_on": []
    }
  ]
}
```

## Learning and Development Experience

Building Sarathi taught me several important lessons:

### **Discord Bot Development**
- **Command Patterns**: How to structure bot commands effectively
- **Async Programming**: Working with Discord's async/await patterns
- **Error Handling**: Graceful failure and user feedback
- **State Management**: Handling persistent data across bot restarts

### **Workflow Automation**
- **Git Integration**: Programmatic commits and pushes
- **Template Systems**: Dynamic content generation with Jinja2
- **Web Scraping**: Reliable title extraction from diverse websites
- **Data Validation**: Ensuring data integrity in automated systems

## Future Improvements

Several enhancements are planned for Sarathi:

### **Immediate Roadmap**
1. **TODO Bot**: Manage my TODO list with VSCode-compliant TODO files
2. **Book Bot**: Interface with my bookshelf's API for reading tracking
3. **Reading Progress**: Track book reading progress and notes
4. **Anki Integration**: Generate Anki cards from TIL entries for spaced repetition

### **Advanced Features**
- **Regex Search**: More powerful search with regular expression support
- **Notes Integration**: Interface with my notes repository for learning packages
- **Analytics**: Learning pattern analysis and knowledge gap identification
- **Export Options**: Multiple output formats (PDF, Markdown, etc.)

## Impact and Results

Sarathi has dramatically improved my learning documentation workflow:

### **Quantitative Improvements**
- **Speed**: From manual updates taking 10-15 minutes to instant Discord commands
- **Consistency**: No more missed or forgotten TIL entries
- **Accessibility**: Can update from anywhere using Discord mobile app
- **Organization**: Automatic categorization and searchable knowledge base

### **Qualitative Benefits**
- **Reduced Friction**: Learning documentation is now effortless
- **Better Retention**: Searchable format helps reinforce past learning
- **Pattern Recognition**: Duplicate tracking reveals learning gaps
- **Motivation**: Seeing accumulated knowledge encourages continued learning

## Source Code and Learning

The complete source code for Sarathi is available on GitHub: [stonecharioteer/sarathi](https://github.com/stonecharioteer/sarathi)

While very specific to my personal workflow, the codebase demonstrates several useful patterns:

{{< example title="Learning Opportunities" >}}
- **Discord bot command structure** and async patterns
- **Git automation** with Python subprocess calls
- **Web scraping** with Beautiful Soup and requests
- **Template systems** with Jinja2 for content generation
- **JSON data management** for simple persistent storage
{{< /example >}}

## Reflection on Automation

This project reinforces a core principle I hold: **automate the boring stuff**. By removing the friction from learning documentation, I've made it more likely that I'll actually capture and retain new knowledge.

{{< quote title="Automation Philosophy" footer="Personal Learning" >}}
The best productivity systems are the ones you actually use. By making TIL documentation as easy as sending a Discord message, I've removed the biggest barrier to maintaining my learning journal.
{{< /quote >}}

Sarathi proves that sometimes the best solutions are the ones we build ourselves, tailored exactly to our personal workflows and preferences.

---

*Building Sarathi was a weekend project that turned into a daily productivity multiplier. It demonstrates how automation can transform tedious manual processes into effortless habits, ultimately supporting better learning and knowledge retention.*