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
5. **TIL (Today I Learned)** - Daily learning entries and technical discoveries

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
- **Syntax Highlighting**: Theme-aware highlighting with custom light/dark mode support
- **Social Integration**: GitHub and LinkedIn profiles
- **Custom Menu**: Emoji navigation with external resume link

## Theme Customizations

### PaperMod Extensions
This blog extends the base PaperMod theme with several sophisticated customizations:

1. **Admonition System** - Complete documentation-style callouts
2. **Theme-Aware Syntax Highlighting** - Custom light/dark mode code block styling
3. **External Code Integration** - Shortcode for including code files
4. **Private Post Filtering** - Content privacy without separate sections
5. **Enhanced Metadata** - Last-modified dates with Git integration
6. **SEO Enhancements** - Proper handling of private content

### Custom Features
- **Performance Focus**: Maintains PaperMod's speed while adding functionality
- **Dark Mode Support**: All customizations work in both light and dark themes
- **Responsive Design**: Mobile-first approach with proper spacing
- **Accessibility**: Proper contrast ratios and semantic HTML

## Theme-Aware Syntax Highlighting

The blog features a comprehensive custom syntax highlighting system that automatically adapts to light and dark themes. This replaces Hugo's default fixed-theme approach with intelligent theme switching.

### Implementation Details

**Hugo Configuration** (`hugo.yml`):
```yaml
markup:
  highlight:
    lineNos: true
    lineNumbersInTable: true
    noClasses: false
    # NO fixed style - allows for theme-aware CSS
```

**Custom CSS** (in `layouts/partials/head.html`):
- **Light Mode**: Clean GitHub-style syntax highlighting with high contrast colors
- **Dark Mode**: Rich Monokai-style colors optimized for dark backgrounds  
- **Universal Coverage**: Works across all programming languages (Python, JavaScript, Rust, Go, etc.)

### Light Mode Colors:
- **Keywords** (`fn`, `let`, `if`): Bold red (`#d01040`)
- **Strings**: Dark blue (`#003d99`)
- **Functions**: Bold purple (`#6610f2`)
- **Comments**: Green italic (`#198754`)
- **Numbers**: Orange (`#fd7e14`)
- **Types**: Magenta (`#d63384`)
- **Background**: Light gray (`#f8f9fa`) with rounded corners

### Dark Mode Colors:
- **Keywords**: Light purple (`#c6a0f6`)
- **Strings**: Light green (`#a6da95`)
- **Functions**: Light blue (`#8aadf4`)
- **Comments**: Muted gray (`#6e738d`) italic
- **Numbers**: Orange (`#f5a97f`)
- **Background**: Dark (`#24273a`)

### Technical Approach:
1. **Removed fixed Hugo style** to enable CSS-based theming
2. **Comprehensive CSS selectors** target all Chroma highlighting elements
3. **Attribute selectors** (`[class*="chroma"]`) ensure universal coverage
4. **Multiple specificity layers** guarantee proper override of theme defaults
5. **Media query fallback** for systems using `prefers-color-scheme`

### Files Modified:
- `hugo.yml` - Removed fixed monokai style
- `layouts/partials/head.html` - Added comprehensive CSS overrides

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

{{< quote title="Einstein said" footer="Albert Einstein" >}}
This is a quote with a custom title and attribution
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

#### Quote with attribution (special case):
```
{{< quote title="Poetry" footer="Robert Frost, The Road Not Taken" blockquote="true" >}}
Two roads diverged in a wood, and I—
I took the one less traveled by,
And that has made all the difference.
{{< /quote >}}

{{< quote footer="Maya Angelou" >}}
There is no greater agony than bearing an untold story inside you.
{{< /quote >}}

{{< quote title="Prose Quote" footer="Marcus Aurelius, Meditations" blockquote="false" >}}
You have power over your mind—not outside events. Realize this, and you will find strength.
{{< /quote >}}
```

### Styling
The admonitions include:
- Responsive design
- Dark mode support
- Color-coded borders and backgrounds
- Icons for visual distinction
- Proper spacing and typography

**Quote Special Features:**
- Serif font (Georgia, Times New Roman) for elegant typography
- Italic styling for the quote content
- Optional footer parameter for attribution
- Right-aligned attribution with em dash prefix
- Optional `blockquote="true"` parameter for line-preserving quotes (default: false)
- Maintains readability in both light and dark modes

**Quote Parameters:**
- `title` - Custom title (default: "Quote")
- `footer` - Attribution text (optional)
- `blockquote` - Wrap content in blockquote for line preservation (default: "false")

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

### TIL Migration (COMPLETED ✅)
- **Migration Status**: 100% complete - all 990 TIL entries migrated
- **Source**: Archive Sphinx blog TIL page with 197 unique dates (2019-2021)
- **Target Format**: Hugo markdown posts with comprehensive frontmatter
- **Database Tracking**: SQLite database (`til.db`) for migration validation
- **Content Enhancement**: Each TIL expanded with context, explanations, and structured sections
- **Organization**: Year-based folders with descriptive filenames

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