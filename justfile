# Tech Blog - Justfile Commands
# https://github.com/casey/just

# Default recipe - show available commands
default:
    @just --list

# Initialize repository: check Hugo version, setup submodules
init:
    #!/usr/bin/env bash
    set -euo pipefail
    
    echo "🔧 Initializing tech blog repository..."
    
    # Check if Hugo is installed and get version
    if ! command -v hugo &> /dev/null; then
        echo "❌ Hugo is not installed. Please install Hugo v0.146.7 or later."
        echo "   Download from: https://github.com/gohugoio/hugo/releases"
        exit 1
    fi
    
    # Check Hugo version
    HUGO_VERSION=$(hugo version | grep -o 'v[0-9]\+\.[0-9]\+\.[0-9]\+' | head -1)
    REQUIRED_VERSION="v0.146.7"
    
    echo "📦 Found Hugo ${HUGO_VERSION}"
    
    # Simple version check (assumes semantic versioning)
    if ! printf '%s\n' "${REQUIRED_VERSION}" "${HUGO_VERSION}" | sort -V | head -1 | grep -q "${REQUIRED_VERSION}"; then
        echo "⚠️  Hugo version ${HUGO_VERSION} found, but ${REQUIRED_VERSION}+ recommended"
        echo "   Download latest from: https://github.com/gohugoio/hugo/releases"
    else
        echo "✅ Hugo version is compatible"
    fi
    
    # Initialize and update submodules
    echo "🔄 Initializing git submodules..."
    git submodule update --init --recursive
    
    echo "📡 Updating submodules to latest commits..."
    git submodule update --recursive --remote
    
    # Check if PaperMod theme is properly loaded
    if [[ ! -f "themes/PaperMod/layouts/_default/single.html" ]]; then
        echo "❌ PaperMod theme not properly loaded. Submodule issue detected."
        exit 1
    fi
    
    echo "✅ Repository initialized successfully!"
    echo "💡 Run 'just serve' to start development server"

# Build the Hugo site (passes through all arguments)
build *ARGS:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "🔨 Building Hugo site..."
    hugo {{ ARGS }}
    echo "✅ Build complete! Output in ./public/"

# Serve the Hugo site for development (passes through all arguments)
serve *ARGS:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "🚀 Starting Hugo development server..."
    echo "💡 Common flags: --buildDrafts --ignoreCache --disableFastRender"
    hugo serve {{ ARGS }}

# Clean build artifacts
clean:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "🧹 Cleaning build artifacts..."
    
    # Remove Hugo build outputs
    if [[ -d "public" ]]; then
        rm -rf public
        echo "   ✅ Removed public/ directory"
    fi
    
    # Remove Hugo cache
    if [[ -d "resources" ]]; then
        rm -rf resources
        echo "   ✅ Removed resources/ cache directory"
    fi
    
    # Remove any temp Hugo cache directories
    if [[ -n "${TMPDIR:-}" && -d "${TMPDIR}/hugo_cache" ]]; then
        rm -rf "${TMPDIR}/hugo_cache"
        echo "   ✅ Removed temporary Hugo cache"
    fi
    
    echo "✅ Clean complete!"

# Test GitHub Actions workflow locally using act
gh-act:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "🎭 Running GitHub Actions locally with act..."
    
    # Check if act is installed
    if ! command -v act &> /dev/null; then
        echo "❌ act is not installed. Install it with:"
        echo "   curl -s https://raw.githubusercontent.com/nektos/act/master/install.sh | bash"
        echo "   Or: brew install act"
        exit 1
    fi
    
    echo "📋 Available jobs in workflow:"
    act -l
    echo ""
    echo "🚀 Running 'build' job..."
    act -j build

# Create a new post (requires title as argument)
new-post TITLE:
    #!/usr/bin/env bash
    set -euo pipefail
    YEAR=$(date +%Y)
    SLUG=$(echo "{{ TITLE }}" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-\|-$//g')
    POST_PATH="content/posts/${YEAR}/${SLUG}.md"
    
    echo "✍️  Creating new post: {{ TITLE }}"
    echo "📁 Path: ${POST_PATH}"
    
    hugo new content "${POST_PATH}"
    
    echo "✅ Post created! Edit it at: ${POST_PATH}"
    echo "💡 Run 'just serve --buildDrafts' to preview drafts"

# Update theme submodule to latest version
update-theme:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "🔄 Updating PaperMod theme to latest version..."
    
    cd themes/PaperMod
    git fetch origin
    git checkout $(git describe --tags $(git rev-list --tags --max-count=1))
    cd ../..
    
    echo "✅ Theme updated to latest stable version"
    echo "💡 Test the site with 'just serve' before committing"

# Show repository status and useful info
status:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "📊 Tech Blog Repository Status"
    echo "=============================="
    echo ""
    
    # Hugo version
    echo "🏗️  Hugo Version:"
    hugo version
    echo ""
    
    # Git status
    echo "📋 Git Status:"
    git status --porcelain || echo "   No changes"
    echo ""
    
    # Submodule status
    echo "📦 Submodule Status:"
    git submodule status
    echo ""
    
    # Recent commits
    echo "📝 Recent Commits:"
    git log --oneline -5
    echo ""
    
    # Draft posts
    echo "✍️  Draft Posts:"
    find content -name "*.md" -exec grep -l "draft: true" {} \; 2>/dev/null | head -5 || echo "   No drafts found"

# Validate post tags against tags.txt (case-sensitive)
validate-tags:
    #!/usr/bin/env bash
    set -euo pipefail
    python3 scripts/validate_tags.py

# List all tags found in posts with counts
list-tags:
    #!/usr/bin/env bash
    set -euo pipefail
    python3 scripts/validate_tags.py --list

# Extract all current tags to tags.txt (overwrites existing)
extract-tags:
    #!/usr/bin/env bash
    set -euo pipefail
    python3 scripts/validate_tags.py --extract