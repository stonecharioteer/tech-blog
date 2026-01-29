#!/usr/bin/env python3
"""
Validate Hugo blog post tags against an allowed tags list.

Usage:
    python scripts/validate_tags.py                    # Validate tags
    python scripts/validate_tags.py --extract         # Extract all tags to tags.txt
    python scripts/validate_tags.py --list            # List all tags found in posts
"""

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path


def parse_frontmatter(content: str) -> dict:
    """Parse YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return {}

    # Find the closing ---
    end_match = re.search(r"\n---\s*\n", content[3:])
    if not end_match:
        return {}

    frontmatter_text = content[3:end_match.start() + 3]

    # Simple YAML parsing for tags
    result = {}

    # Match tags in either format:
    # tags: ["tag1", "tag2"] or tags:\n  - tag1\n  - tag2

    # First try inline array format: tags: ["tag1", "tag2"]
    inline_match = re.search(r'^tags:\s*\[([^\]]*)\]', frontmatter_text, re.MULTILINE)
    if inline_match:
        tags_str = inline_match.group(1)
        # Parse items, handling both quoted and unquoted
        tags = []
        for item in tags_str.split(','):
            item = item.strip().strip('"').strip("'")
            if item:
                tags.append(item)
        result['tags'] = tags
        return result

    # Try multiline format: tags:\n  - tag1\n  - tag2
    multiline_match = re.search(r'^tags:\s*\n((?:\s+-\s+[^\n]+\n?)+)', frontmatter_text, re.MULTILINE)
    if multiline_match:
        tags_block = multiline_match.group(1)
        tags = []
        for line in tags_block.split('\n'):
            line = line.strip()
            if line.startswith('-'):
                tag = line[1:].strip().strip('"').strip("'")
                if tag:
                    tags.append(tag)
        result['tags'] = tags
        return result

    return result


def find_posts(content_dir: Path) -> list[Path]:
    """Find all markdown posts in content directory."""
    posts = []
    posts_dir = content_dir / "posts"
    if posts_dir.exists():
        posts.extend(posts_dir.rglob("*.md"))
    return sorted(posts)


def extract_all_tags(posts: list[Path]) -> dict[str, list[Path]]:
    """Extract all tags from posts, returning a dict of tag -> list of posts."""
    tags_to_posts = defaultdict(list)

    for post in posts:
        content = post.read_text(encoding='utf-8')
        frontmatter = parse_frontmatter(content)
        tags = frontmatter.get('tags', [])

        for tag in tags:
            tags_to_posts[tag].append(post)

    return dict(tags_to_posts)


def load_allowed_tags(tags_file: Path) -> set[str]:
    """Load allowed tags from tags.txt file."""
    if not tags_file.exists():
        print(f"Error: {tags_file} not found.", file=sys.stderr)
        print("Run with --extract to create it from existing tags.", file=sys.stderr)
        sys.exit(1)

    tags = set()
    for line in tags_file.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if line and not line.startswith('#'):
            tags.add(line)
    return tags


def validate_tags(content_dir: Path, tags_file: Path) -> int:
    """Validate all post tags against allowed tags. Returns exit code."""
    allowed_tags = load_allowed_tags(tags_file)
    posts = find_posts(content_dir)

    # Find all unrecognized tags
    unrecognized = defaultdict(list)  # tag -> list of posts

    for post in posts:
        content = post.read_text(encoding='utf-8')
        frontmatter = parse_frontmatter(content)
        tags = frontmatter.get('tags', [])

        for tag in tags:
            if tag not in allowed_tags:
                rel_path = post.relative_to(content_dir.parent)
                unrecognized[tag].append(str(rel_path))

    if not unrecognized:
        print(f"All tags are valid. ({len(allowed_tags)} allowed tags)")
        return 0

    # Output unrecognized tags
    print(f"Found {len(unrecognized)} unrecognized tag(s):\n")

    for tag in sorted(unrecognized.keys()):
        posts_with_tag = unrecognized[tag]
        print(f"  \"{tag}\" ({len(posts_with_tag)} post(s)):")
        for post_path in sorted(posts_with_tag):
            print(f"    - {post_path}")
        print()

    # Summary
    total_occurrences = sum(len(posts) for posts in unrecognized.values())
    print(f"Total: {len(unrecognized)} unrecognized tags in {total_occurrences} location(s)")

    return 1


def extract_tags(content_dir: Path, tags_file: Path) -> None:
    """Extract all tags from posts and write to tags.txt."""
    posts = find_posts(content_dir)
    all_tags = extract_all_tags(posts)

    # Sort tags alphabetically (case-insensitive for sorting, but preserve case)
    sorted_tags = sorted(all_tags.keys(), key=str.lower)

    # Write to file
    with tags_file.open('w', encoding='utf-8') as f:
        f.write("# Allowed tags for Hugo blog posts\n")
        f.write("# One tag per line, case-sensitive\n")
        f.write("# Lines starting with # are comments\n")
        f.write("\n")
        for tag in sorted_tags:
            f.write(f"{tag}\n")

    print(f"Extracted {len(sorted_tags)} unique tags to {tags_file}")


def list_tags(content_dir: Path) -> None:
    """List all tags found in posts with counts."""
    posts = find_posts(content_dir)
    all_tags = extract_all_tags(posts)

    # Sort by count (descending), then alphabetically
    sorted_tags = sorted(all_tags.items(), key=lambda x: (-len(x[1]), x[0].lower()))

    print(f"Found {len(sorted_tags)} unique tags:\n")
    for tag, posts_list in sorted_tags:
        print(f"  {tag}: {len(posts_list)} post(s)")


def main():
    parser = argparse.ArgumentParser(
        description="Validate Hugo blog post tags against tags.txt"
    )
    parser.add_argument(
        "--extract",
        action="store_true",
        help="Extract all tags from posts and write to tags.txt"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all tags found in posts with counts"
    )
    parser.add_argument(
        "--content-dir",
        type=Path,
        default=Path("content"),
        help="Path to content directory (default: content)"
    )
    parser.add_argument(
        "--tags-file",
        type=Path,
        default=Path("tags.txt"),
        help="Path to tags file (default: tags.txt)"
    )

    args = parser.parse_args()

    # Resolve paths relative to script location if not absolute
    script_dir = Path(__file__).parent.parent

    content_dir = args.content_dir
    if not content_dir.is_absolute():
        content_dir = script_dir / content_dir

    tags_file = args.tags_file
    if not tags_file.is_absolute():
        tags_file = script_dir / tags_file

    if args.extract:
        extract_tags(content_dir, tags_file)
    elif args.list:
        list_tags(content_dir)
    else:
        sys.exit(validate_tags(content_dir, tags_file))


if __name__ == "__main__":
    main()
