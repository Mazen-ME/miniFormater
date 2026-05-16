"""
Unit Tests for Arabic Novel Parser

Run with: python test_parser.py
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from parser import parse_chapters, ChapterParser
from formatter import format_chapters, get_stats


def test_parse_basic():
    """Test basic chapter parsing."""
    text = """**الفصل 1: الأول**
محتوى الفصل الأول

**الفصل 2: الثاني**
محتوى الفصل الثاني"""
    
    chapters = parse_chapters(text)
    
    assert len(chapters) == 2, f"Expected 2 chapters, got {len(chapters)}"
    assert chapters[0]["chapter_number"] == 1
    assert chapters[0]["title"] == "الأول"
    assert chapters[1]["chapter_number"] == 2
    assert chapters[1]["title"] == "الثاني"
    
    print("✅ test_parse_basic passed")


def test_parse_with_whitespace():
    """Test parsing with extra whitespace."""
    text = """  **الفصل 1: Title One**  
content line 1
content line 2

**الفصل 2: Title Two**  
content here"""
    
    chapters = parse_chapters(text)
    
    assert len(chapters) == 2
    assert chapters[0]["title"] == "Title One"
    assert "content line 1" in chapters[0]["content"]
    assert chapters[1]["title"] == "Title Two"
    
    print("✅ test_parse_with_whitespace passed")


def test_parse_empty_chapters():
    """Test parsing chapters with no content."""
    text = """**الفصل 1: First**

**الفصل 2: Second**
some content"""
    
    chapters = parse_chapters(text)
    
    assert len(chapters) == 2
    assert chapters[0]["content"].strip() == ""
    assert "some content" in chapters[1]["content"]
    
    print("✅ test_parse_empty_chapters passed")


def test_format_single_chapter():
    """Test formatting a single chapter."""
    chapters = [
        {
            "chapter_number": 1,
            "title": "Test Title",
            "content": "Test content here"
        }
    ]
    
    output = format_chapters(chapters)
    
    assert "chapter_number: 1" in output
    assert "title: Test Title" in output
    assert "is_published: true" in output
    assert "content:" in output
    assert "Test content here" in output
    
    print("✅ test_format_single_chapter passed")


def test_format_multiple_chapters():
    """Test formatting multiple chapters with separators."""
    chapters = [
        {
            "chapter_number": 1,
            "title": "First",
            "content": "Content 1"
        },
        {
            "chapter_number": 2,
            "title": "Second",
            "content": "Content 2"
        },
        {
            "chapter_number": 3,
            "title": "Third",
            "content": "Content 3"
        }
    ]
    
    output = format_chapters(chapters)
    
    # Check separators
    separator_count = output.count("\n---\n")
    assert separator_count == 2, f"Expected 2 separators, got {separator_count}"
    
    # Check no duplicate separators
    assert "---\n---" not in output
    
    # Check all chapters present
    assert "chapter_number: 1" in output
    assert "chapter_number: 2" in output
    assert "chapter_number: 3" in output
    
    print("✅ test_format_multiple_chapters passed")


def test_no_trailing_separator():
    """Test that output doesn't end with separator."""
    chapters = [
        {
            "chapter_number": 1,
            "title": "Test",
            "content": "Content"
        }
    ]
    
    output = format_chapters(chapters)
    
    assert not output.endswith("---"), "Output should not end with separator"
    assert not output.endswith("\n---"), "Output should not end with separator"
    
    print("✅ test_no_trailing_separator passed")


def test_stats():
    """Test statistics calculation."""
    chapters = [
        {
            "chapter_number": 1,
            "title": "First",
            "content": "word1 word2 word3"
        },
        {
            "chapter_number": 2,
            "title": "Second",
            "content": "word4 word5"
        }
    ]
    
    stats = get_stats(chapters)
    
    assert stats["chapter_count"] == 2
    assert stats["total_words"] == 5
    assert stats["avg_chapter_words"] == 2.5
    assert stats["total_characters"] == len("word1 word2 word3") + len("word4 word5")
    
    print("✅ test_stats passed")


def test_validate_chapters():
    """Test chapter validation."""
    valid_chapters = [
        {
            "chapter_number": 1,
            "title": "Valid",
            "content": "content"
        }
    ]
    
    # Should not raise
    ChapterParser.validate_chapters(valid_chapters)
    
    print("✅ test_validate_chapters passed")


def test_validate_invalid_chapters():
    """Test validation catches invalid chapters."""
    invalid_chapters = [
        {
            "chapter_number": "not_int",  # Should be int
            "title": "Invalid",
            "content": "content"
        }
    ]
    
    try:
        ChapterParser.validate_chapters(invalid_chapters)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    print("✅ test_validate_invalid_chapters passed")


def test_utf8_arabic():
    """Test UTF-8 Arabic text handling."""
    text = """**الفصل 1: الرحلة الطويلة**
كان الصباح بارداً جداً، والسماء رمادية اللون.

**الفصل 2: النهاية السعيدة**
عاد إلى الوطن بسعادة."""
    
    chapters = parse_chapters(text)
    
    assert len(chapters) == 2
    assert "الرحلة الطويلة" in chapters[0]["title"]
    assert "بارداً" in chapters[0]["content"]
    assert "النهاية السعيدة" in chapters[1]["title"]
    
    print("✅ test_utf8_arabic passed")


def test_special_characters():
    """Test handling special characters in content."""
    text = """**الفصل 1: Test!@#$%^&*()**
Content with special chars: !@#$%^&*()[]{}

**الفصل 2: Émojis?**
More content here with émojis 🎉"""
    
    chapters = parse_chapters(text)
    
    assert len(chapters) == 2
    assert "Test!@#$%^&*()" in chapters[0]["title"]
    
    print("✅ test_special_characters passed")


def test_large_content():
    """Test handling large content."""
    large_content = "\n".join(["word"] * 1000)  # 1000 word lines
    text = f"""**الفصل 1: Large**
{large_content}

**الفصل 2: Also Large**
{large_content}"""
    
    chapters = parse_chapters(text)
    
    assert len(chapters) == 2
    assert len(chapters[0]["content"].split()) >= 1000
    
    stats = get_stats(chapters)
    assert stats["total_words"] >= 2000
    
    print("✅ test_large_content passed")


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*50)
    print("Running Arabic Novel Parser Tests")
    print("="*50 + "\n")
    
    tests = [
        test_parse_basic,
        test_parse_with_whitespace,
        test_parse_empty_chapters,
        test_format_single_chapter,
        test_format_multiple_chapters,
        test_no_trailing_separator,
        test_stats,
        test_validate_chapters,
        test_validate_invalid_chapters,
        test_utf8_arabic,
        test_special_characters,
        test_large_content,
    ]
    
    failed = 0
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"❌ {test.__name__} failed: {e}")
            failed += 1
    
    print("\n" + "="*50)
    passed = len(tests) - failed
    print(f"Results: {passed}/{len(tests)} tests passed")
    
    if failed == 0:
        print("🎉 All tests passed!")
    else:
        print(f"⚠️  {failed} test(s) failed")
    
    print("="*50 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
