# Vendored theme

This directory is a **vendored copy** of [hugo-PaperMod](https://github.com/adityatelange/hugo-PaperMod),
not a git submodule. The files are committed directly into this repository.

- Upstream: https://github.com/adityatelange/hugo-PaperMod.git
- Vendored at: `v8.0-32-g5a46517` (commit `5a4651783fa9159123d947bd3511b355146d4797`)

## Updating

To pull a newer upstream version, re-sync the files (this overwrites local
changes to the theme — keep project-specific overrides in the repo-root
`layouts/` instead, which Hugo loads in preference to the theme):

```bash
tmp=$(mktemp -d)
git clone --depth 1 --branch <tag-or-branch> https://github.com/adityatelange/hugo-PaperMod.git "$tmp"
rm -rf themes/PaperMod
rsync -a --exclude='.git' "$tmp"/ themes/PaperMod/
# restore this note, then update the version line above
git -C "$tmp" describe --tags
rm -rf "$tmp"
```
