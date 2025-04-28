import llm
from markitdown import MarkItDown


@llm.hookimpl
def register_fragment_loaders(register):
    """
    Register a fragment loader under the scheme "md".
    Usage:
        llm -f md:path/to/file.pdf …
        llm -f md:https://example.com/doc.docx …
    """
    register("md", markitdown_loader)


def markitdown_loader(argument: str) -> llm.Fragment:
    """
    Load a document via MarkItDown and return it as a single Markdown fragment.

    argument:
      - path to a local file
      - http[s]:// URL
    """
    md = MarkItDown(enable_plugins=False)
    result = md.convert(argument)
    return llm.Fragment(result.text_content, source=f"md:{argument}")
