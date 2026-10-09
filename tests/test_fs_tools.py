"""Tests for fs_tools (Part A)."""

from pathlib import Path

import fs_tools

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESUMES_DIR = PROJECT_ROOT / "resumes"


def test_list_files_returns_metadata() -> None:
    files = fs_tools.list_files(str(RESUMES_DIR))
    print(f"    Outcome: listed {len(files)} file(s) in resumes/")
    assert len(files) >= 2
    names = {item["name"] for item in files}
    assert "resume_john_doe.txt" in names
    for item in files:
        assert "name" in item and "size" in item and "modified" in item
        assert item["size"] > 0


def test_list_files_extension_filter() -> None:
    pdfs = fs_tools.list_files(str(RESUMES_DIR), extension=".pdf")
    print(f"    Outcome: {len(pdfs)} PDF(s) — {[p['name'] for p in pdfs]}")
    assert pdfs
    assert all(name["name"].endswith(".pdf") for name in pdfs)


def test_read_file_txt() -> None:
    path = RESUMES_DIR / "resume_john_doe.txt"
    result = fs_tools.read_file(str(path))
    print(
        f"    Outcome: read TXT ok={result['error'] is None}, "
        f"size={result['size']}, content_len={len(result['content'] or '')}"
    )
    assert result["error"] is None
    assert result["content"] is not None
    assert "John Doe" in result["content"]
    assert result["filename"] == "resume_john_doe.txt"
    assert result["size"] > 0


def test_read_file_pdf() -> None:
    path = RESUMES_DIR / "resume_john_doe.pdf"
    assert path.is_file(), "resume_john_doe.pdf must exist in resumes/"
    result = fs_tools.read_file(str(path))
    print(
        f"    Outcome: read PDF ok={result['error'] is None}, "
        f"has_python={'Python' in (result['content'] or '')}"
    )
    assert result["error"] is None
    assert result["content"] is not None
    assert "Python" in result["content"]


def test_read_file_docx() -> None:
    path = RESUMES_DIR / "resume_john_doe.docx"
    assert path.is_file(), "resume_john_doe.docx must exist in resumes/"
    result = fs_tools.read_file(str(path))
    print(
        f"    Outcome: read DOCX ok={result['error'] is None}, "
        f"has_john_doe={'John Doe' in (result['content'] or '')}"
    )
    assert result["error"] is None
    assert result["content"] is not None
    assert "John Doe" in result["content"]


def test_search_in_file_case_insensitive() -> None:
    path = RESUMES_DIR / "resume_john_doe.txt"
    result = fs_tools.search_in_file(str(path), "python")
    print(f"    Outcome: search TXT matches={len(result['matches'])} for keyword 'python'")
    assert result["error"] is None
    assert len(result["matches"]) >= 1
    assert result["matches"][0]["line_number"] >= 1
    assert "context_before" in result["matches"][0]
    assert "context_after" in result["matches"][0]


def test_search_in_file_pdf() -> None:
    path = RESUMES_DIR / "resume_john_doe.pdf"
    result = fs_tools.search_in_file(str(path), "Python")
    print(f"    Outcome: search PDF matches={len(result['matches'])} for keyword 'Python'")
    assert result["error"] is None
    assert len(result["matches"]) >= 1


def test_write_file_creates_directories(tmp_path: Path) -> None:
    target = tmp_path / "nested" / "summary.txt"
    outcome = fs_tools.write_file(str(target), "hello")
    print(f"    Outcome: write success={outcome['success']}, path={outcome['path']}")
    assert outcome["success"] is True
    assert outcome["error"] is None
    assert target.read_text(encoding="utf-8") == "hello"


def test_read_file_missing_returns_error() -> None:
    result = fs_tools.read_file(str(RESUMES_DIR / "does_not_exist.txt"))
    print(f"    Outcome: missing file error={result['error']!r}")
    assert result["content"] is None
    assert result["error"] is not None
