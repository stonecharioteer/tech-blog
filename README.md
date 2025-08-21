# Stonecharioteer's Tech Blog

A Hugo-powered technical blog focused on software development, Python, and career insights. Built with the PaperMod theme and enhanced with custom admonitions and features.

**Live Site**: https://tech.stonecharioteer.com/

## Setup

### Prerequisites
Install Hugo 0.146.7 extended using the `.deb` file:
```bash
# Download Hugo 0.146.7 extended
wget https://github.com/gohugoio/hugo/releases/download/v0.146.7/hugo_extended_0.146.7_linux-amd64.deb

# Install the package
sudo dpkg -i hugo_extended_0.146.7_linux-amd64.deb
```

### Development
```bash
# Clone and setup theme
git submodule update --init --recursive

# Local development server
hugo serve --buildDrafts

# Production build
hugo
```

### Testing GitHub Actions Locally
Test the build workflow locally using [act](https://github.com/nektos/act):
```bash
# Test the build job only (skips deployment)
gh act -j build

# Test with specific event (e.g., pull request)
gh act pull_request -j build
```

## Content Management

### Creating Posts
```bash
# Create new post with year organization
hugo new content content/posts/2025/my-post-title.md

# Legacy format (directly in posts/)
hugo new content content/posts/my-post-title.md
```

### Frontmatter Template
```yaml
---
date: '2025-01-15T10:30:00+05:30'  # IST timezone
draft: false
title: 'Your Post Title'
tags: ["python", "tutorial", "career"]
cover:                             # Optional
  image: "/images/cover.jpg"
  alt: "Cover image description"
private: true                      # Optional - hides from listings
url: "custom-url-path"            # Optional
---
```

### Content Types

**Regular Posts**: `content/posts/YYYY/title.md`
**Unlisted Content**: `content/unlisted/` (published but not featured)
**Static Pages**: 
- `gear.md` - Personal tech setup
- `favourites.md` - Curated resources
- `values.md` - Personal philosophy

## Custom Features

### Admonitions
Enhanced content blocks for technical documentation:

```markdown
{{< note title="Important" >}}
Your note content here
{{< /note >}}

{{< info >}}
Information with default title
{{< /info >}}

{{< warning title="Caution" >}}
Warning content
{{< /warning >}}

{{< tip title="Pro Tip" >}}
Helpful suggestion
{{< /tip >}}

{{< example title="Code Demo" >}}
Example or demonstration
{{< /example >}}
```

### Quotes (Special Features)
Perfect for poetry, literature, or attributed quotes:

```markdown
{{< quote title="Poetry" footer="Robert Frost" blockquote="true" >}}
Two roads diverged in a wood, and I—
I took the one less traveled by,
And that has made all the difference.
{{< /quote >}}

{{< quote footer="Maya Angelou" >}}
Prose quotes flow naturally without line preservation.
{{< /quote >}}
```

**Quote Parameters:**
- `title` - Custom title (default: "Quote")
- `footer` - Attribution text
- `blockquote` - Preserve line breaks for poetry (default: false)

### External Code Integration
```markdown
{{< code language="python" source="code/example/main.py" >}}
```
Includes and highlights code from files in the `/code/` directory.

## Content Guidelines

### Writing Style
- Technical precision with practical examples
- Personal voice and anecdotes
- Performance analysis using `timeit` when relevant
- Cross-references to gear and favorites pages

### Tag Strategy
- **Technical**: `python`, `microservices`, `grpc`, `data-structures-and-algorithms`
- **Content**: `reflection`, `housekeeping`, `career`, `culture`
- Use lowercase, hyphenated format for consistency

### Images
Place images in `static/images/` and reference as `/images/filename.jpg`

## Special Content

### Private Posts
Add `private: true` to frontmatter to hide from listings while keeping publicly accessible via direct URL.

### Code Examples
Maintain runnable examples in `/code/` directory that can be included in posts via the code shortcode.

## Theme & Styling

- **Base Theme**: PaperMod (git submodule)
- **Dark Mode**: Automatic theme switching supported
- **Custom Features**: Admonitions, external code integration, private posts
- **Typography**: Serif fonts for quotes, monospace for code

## Deployment

The site uses Git integration for automatic last-modified dates. Ensure commits are properly authored for accurate timestamps.
