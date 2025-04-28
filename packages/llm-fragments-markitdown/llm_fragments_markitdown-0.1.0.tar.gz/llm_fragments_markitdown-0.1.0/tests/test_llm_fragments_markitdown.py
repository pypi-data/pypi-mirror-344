import llm

from llm_fragments_markitdown import markitdown_loader


def test_markitdown_loader_with_local_file(tmp_path) -> None:
    # Create a simple HTML file
    sample_file = tmp_path / "sample.html"
    html_content = "<html><body><h1>Test</h1><p>Hello world</p></body></html>"
    sample_file.write_text(html_content)

    # Call the function with the file
    fragment = markitdown_loader(str(sample_file))

    # Basic checks to verify the loader works
    assert isinstance(fragment, llm.Fragment)
    assert fragment.source == f"md:{sample_file}"

    # Simple content check - we don't need to test MarkItDown's conversion
    content = str(fragment)
    assert "Test" in content
    assert "Hello world" in content
