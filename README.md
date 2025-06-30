# tech-blog

Install `hugo` using the `.deb` file from https://github.com/gohugoio/hugo/releases/latest. Use `sudo dpkg -i $FILE_PATH` to install the package.

```bash
git submodule update --init --recursive # gets the papermod theme as a submodule
hugo serve --buildDrafts # serve the blog locally
```

To add a new post

`hugo new content content/posts/$TITLE.md`
