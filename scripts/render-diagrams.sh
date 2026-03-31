#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DIAGRAMS_DIR="${REPO_ROOT}/diagrams"
IMAGES_DIR="${REPO_ROOT}/static/images/posts"

if ! command -v mmdc &>/dev/null; then
  echo "Error: mmdc (mermaid-cli) not found. Install with: brew install mermaid-cli"
  exit 1
fi

# mmdc's bundled puppeteer-core expects a specific Chrome version that may not
# be cached. Fall back to the system Chrome if PUPPETEER_EXECUTABLE_PATH is not
# already set.
if [ -z "${PUPPETEER_EXECUTABLE_PATH:-}" ]; then
  if [ -x "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ]; then
    export PUPPETEER_EXECUTABLE_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
  fi
fi

for f in "${DIAGRAMS_DIR}"/*.mmd; do
  [ -f "$f" ] || continue

  basename="$(basename "$f" .mmd)"

  # Map diagram name to output directory:
  #   merrilin-*  → merrilin/tech/
  #   homelab-*   → homelab/
  #   otherwise   → top-level images/posts/
  case "$basename" in
    merrilin-*)
      name="${basename#merrilin-}"
      out_dir="${IMAGES_DIR}/merrilin/tech"
      ;;
    homelab-*)
      name="${basename#homelab-}"
      out_dir="${IMAGES_DIR}/homelab"
      ;;
    tailscale-*)
      name="${basename#tailscale-}"
      out_dir="${IMAGES_DIR}/tailscale"
      ;;
    *)
      name="$basename"
      out_dir="${IMAGES_DIR}"
      ;;
  esac

  mkdir -p "$out_dir"
  out_path="${out_dir}/${name}.png"

  echo "Rendering ${f} → ${out_path}"
  mmdc -i "$f" -o "$out_path" -b white -s 3
done

echo "Done."
