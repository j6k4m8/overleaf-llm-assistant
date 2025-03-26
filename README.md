# overleaf llm assistant hacky repo

this illustrates using the `overphloem` package to create a simple LLM assistant for Overleaf projects.

> [!CAUTION] > **This is super hacky right now and totally could erase all your text!** In general that's recoverable via Overleaf history, but obviously that sucks!

```bash
# git clone this repo, then:
uv run editor.py 1a2b3c4d5e6f7g890 # project ID
```

Get a project ID by opening an Overleaf project and looking at the URL. For example, if the URL is `https://www.overleaf.com/project/1234567890abcdef`, then the project ID is `1234567890abcdef`.

You'll also have to set up Overleaf git credentials on your system.
