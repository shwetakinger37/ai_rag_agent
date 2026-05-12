from app.utils.chunking import split_text


def test_split_text_creates_chunks():
    text = "hello world " * 300
    chunks = split_text(text, chunk_size=100, overlap=10)
    assert len(chunks) > 1
    assert all(len(chunk) <= 100 for chunk in chunks)


def test_split_empty_text():
    assert split_text("") == []
