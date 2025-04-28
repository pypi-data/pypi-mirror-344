# llm-fragments-markitdown

[![PyPI](https://img.shields.io/pypi/v/llm-fragments-markitdown.svg)](https://pypi.org/project/llm-fragments-markitdown/)
[![Changelog](https://img.shields.io/github/v/release/wolfmanstout/llm-fragments-markitdown?include_prereleases&label=changelog)](https://github.com/wolfmanstout/llm-fragments-markitdown/releases)
[![Tests](https://github.com/wolfmanstout/llm-fragments-markitdown/actions/workflows/test.yml/badge.svg)](https://github.com/wolfmanstout/llm-fragments-markitdown/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/wolfmanstout/llm-fragments-markitdown/blob/master/LICENSE)

LLM fragment loader which converts various formats to Markdown.

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).

```bash
llm install llm-fragments-markitdown
```

## Usage

Use the fragment loader like this:

```bash
llm -f md:path/to/file.html
llm -f md:https://simonwillison.net/2025/Apr/7/long-context-llm/
```

This will use the [MarkItDown](https://github.com/microsoft/markitdown) library to convert the argument into Markdown.

While this supports various formats out-of-the-box, more can be added as optional dependencies, for example:

```bash
llm install markitdown[all]  # Installs all optional dependencies
llm install markitdown[pdf, youtube-transcription]  # Installs just the PDF and YouTube transcript readers.
```

## Development

To contribute to this tool, use uv. The following command will establish the
venv and run tests:

```bash
uv run pytest
```

To run llm-fragments-markitdown locally, use:

```bash
uv run llm-fragments-markitdown
```
