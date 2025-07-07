# Claude Instructions for Tech Blog

## Project Overview
This is **Stonecharioteer's Tech Blog** - a sophisticated Hugo static site focused on software development, technology, and career insights. The site is deployed at `https://tech.stonecharioteer.com/` and represents a high-quality technical blog with advanced content authoring capabilities.

**Author**: Vinay Keerthi (`stonecharioteer`)  
**Focus**: Python development, microservices, career development, and technical tutorials  
**Theme**: PaperMod with extensive customizations

## Repository Structure
```
tech-blog/
├── content/
│   ├── posts/                    # Blog posts (year-organized)
│   │   ├── 2025/                # Current year posts
│   │   └── crews-not-teams.md   # Legacy posts
│   ├── unlisted/                # Published but not featured
│   ├── gear.md                  # Personal tech setup
│   ├── favourites.md            # Curated resources
│   ├── values.md                # Personal philosophy
│   ├── archive.md               # Post archive
│   └── search.md                # Search functionality
├── code/                        # External code examples
│   └── py-x-protobuf/          # Python protobuf examples
├── layouts/
│   ├── _default/
│   │   └── list.html           # Custom list with private post filtering
│   ├── partials/
│   │   ├── head.html           # Custom head with admonition CSS
│   │   └── post_meta.html      # Enhanced metadata display
│   └── shortcodes/             # Custom shortcodes
├── static/
│   ├── images/                 # Blog post images
│   └── logo/                   # Brand assets
├── themes/PaperMod/            # Git submodule theme
├── hugo.yml                    # Hugo configuration
└── README.md                   # Setup instructions
```

## Content Strategy & Organization

### Post Categories
1. **Technical Tutorials** - Python, microservices, performance analysis
2. **Career & Culture** - Team dynamics, professional development
3. **Meta/Housekeeping** - Blog maintenance, platform updates
4. **Personal Reflection** - Values, career transitions

### Content Patterns
- **TLDR sections** for longer posts
- **Performance benchmarks** with timing analysis
- **Practical code examples** with working implementations
- **Personal anecdotes** for context and engagement
- **Cross-references** to gear and favorites pages

### Frontmatter Standards
```yaml
---
date: 'YYYY-MM-DDTHH:MM:SS+05:30'  # IST timezone
draft: false
title: 'Post Title'
tags: ["tag1", "tag2"]
cover:                              # Optional
  image: "/images/filename.jpeg"
  alt: "Alt text"
private: true                       # Optional - hides from listings
url: "custom-path"                  # Optional - custom URL
---
```

### Tag Strategy
- **Technical**: `python`, `microservices`, `grpc`, `data-structures-and-algorithms`
- **Content**: `reflection`, `housekeeping`, `career`, `culture`
- **Consistency**: Mixed case (needs standardization)

## Build Process & Deployment

### Development Workflow
```bash
# Theme setup (one-time)
git submodule update --init --recursive

# Local development
hugo serve --buildDrafts

# New post creation
hugo new content content/posts/YYYY/title.md
```

### Dependencies
- **Hugo**: Install from GitHub releases (`.deb` package)
- **PaperMod Theme**: Git submodule at `themes/PaperMod/`
- **Python Code Examples**: `code/py-x-protobuf/` uses Python 3.13+ with uv/pip

### Configuration Highlights
- **Git Integration**: `enableGitInfo: true` for auto last-modified dates
- **Search**: JSON output format with Fuse.js integration
- **Syntax Highlighting**: Monokai theme with line numbers
- **Social Integration**: GitHub and LinkedIn profiles
- **Custom Menu**: Emoji navigation with external resume link

## Theme Customizations

### PaperMod Extensions
This blog extends the base PaperMod theme with several sophisticated customizations:

1. **Admonition System** - Complete documentation-style callouts
2. **External Code Integration** - Shortcode for including code files
3. **Private Post Filtering** - Content privacy without separate sections
4. **Enhanced Metadata** - Last-modified dates with Git integration
5. **SEO Enhancements** - Proper handling of private content

### Custom Features
- **Performance Focus**: Maintains PaperMod's speed while adding functionality
- **Dark Mode Support**: All customizations work in both light and dark themes
- **Responsive Design**: Mobile-first approach with proper spacing
- **Accessibility**: Proper contrast ratios and semantic HTML

## Admonition Shortcodes
The most significant customization is a complete admonition system that brings documentation-quality content formatting to the blog:

### Available Types
- `note` - Blue themed with 📝 icon
- `info` - Cyan themed with ℹ️ icon  
- `warning` - Yellow themed with ⚠️ icon
- `tip` - Green themed with 💡 icon
- `quote` - Gray themed with 💬 icon
- `example` - Purple themed with 📋 icon

### Usage Examples

#### Basic usage with default titles:
```
{{< note >}}
This is a note with default title "Note"
{{< /note >}}

{{< info >}}
This is an info box with default title "Info"
{{< /info >}}

{{< warning >}}
This is a warning with default title "Warning"
{{< /warning >}}

{{< tip >}}
This is a tip with default title "Tip"
{{< /tip >}}

{{< quote >}}
This is a quote with default title "Quote"
{{< /quote >}}

{{< example >}}
This is an example with default title "Example"
{{< /example >}}
```

#### Custom titles:
```
{{< note title="Important Point" >}}
This is a note with a custom title
{{< /note >}}

{{< info title="Pro Tip" >}}
This is an info box with a custom title
{{< /info >}}

{{< warning title="Caution" >}}
This is a warning with a custom title
{{< /warning >}}

{{< tip title="Pro Tip" >}}
This is a tip with a custom title
{{< /tip >}}

{{< quote title="Einstein said" >}}
This is a quote with a custom title
{{< /quote >}}

{{< example title="Code Sample" >}}
This is an example with a custom title
{{< /example >}}
```

#### With Markdown content:
```
{{< note title="Code Example" >}}
You can use **markdown** inside admonitions:

- Lists work
- `Code snippets` work
- [Links](https://example.com) work

```python
def hello():
    print("Hello from inside an admonition!")
```
{{< /note >}}
```

### Styling
The admonitions include:
- Responsive design
- Dark mode support
- Color-coded borders and backgrounds
- Icons for visual distinction
- Proper spacing and typography

### Files Created
- `layouts/shortcodes/note.html`
- `layouts/shortcodes/info.html`
- `layouts/shortcodes/warning.html`
- `layouts/shortcodes/tip.html`
- `layouts/shortcodes/quote.html`
- `layouts/shortcodes/example.html`
- Added CSS styles to `layouts/partials/head.html`

## Additional Shortcodes

### External Code Integration
```
{{< code language="python" source="code/py-x-protobuf/example.py" >}}
```
- Reads external code files at build time
- Supports syntax highlighting with configurable options
- Allows maintaining runnable examples in `/code/` directory

## Content Guidelines

### Writing Style
- **Technical precision** with detailed explanations
- **Personal voice** - conversational and reflective
- **Practical focus** - real-world applications
- **Educational intent** - teaching through experience

### Performance Analysis
- Use `timeit` for benchmarking code examples
- Include comparative analysis when relevant
- Document performance characteristics of solutions

### Cross-References
- Link to gear page for technical setup context
- Reference favorites page for recommended resources
- Use internal links to build content coherence

## SEO & Social

### Meta Information
- **OpenGraph**: Proper social media sharing
- **Twitter Cards**: Enhanced tweet previews
- **Schema.org**: Structured data for search engines
- **Git Integration**: Automatic last-modified dates

### Content Discovery
- **Search**: Fast client-side search with Fuse.js
- **Archives**: Chronological post listing
- **Tags**: Semantic categorization
- **RSS**: Full content feeds

## Maintenance Notes

### Theme Updates
- PaperMod is a git submodule - update with care
- Test admonition styling after theme updates
- Verify custom shortcodes remain functional

### Content Management
- Use IST timezone for consistency
- Maintain year-based organization for posts
- Review tag consistency regularly
- Update gear/favorites pages periodically

### Code Examples
- Keep `/code/` directory examples runnable
- Update Python versions and dependencies as needed
- Test external code inclusion after changes

## Technical Specifications

### Hugo Version
- **Minimum**: 0.125.7 (required by PaperMod)
- **Features Used**: GitInfo, JSON output, advanced templating

### Performance Characteristics
- **Build Time**: Fast due to minimal theme overhead
- **Runtime**: Static site with client-side search
- **SEO**: Optimized for search engines and social sharing
- **Accessibility**: WCAG compliant with proper contrast ratios