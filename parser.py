"""
Arabic Novel Chapter Parser

Handles parsing of Arabic novel files with chapter detection and extraction.
Optimized for UTF-8 text and large file handling (100k+ words).
"""

import re
from typing import List, Dict, Optional


class ChapterParser:
    """Parse Arabic novels into structured chapter data."""
    
    # Pattern for matching: **الفصل X: Title**
    CHAPTER_PATTERN = re.compile(
        r"^\s*\*\*الفصل\s*(\d+)\s*:\s*(.+?)\*\*\s*$",
        re.MULTILINE | re.UNICODE
    )
    
    @staticmethod
    def parse_chapters(text: str) -> List[Dict]:
        """
        Parse Arabic novel text into structured chapters.
        
        Args:
            text: Raw text content with chapter headers
            
        Returns:
            List of dictionaries with keys: chapter_number, title, content
            
        Raises:
            ValueError: If text is empty or invalid encoding
        """
        if not text or not isinstance(text, str):
            raise ValueError("Input must be non-empty string")
        
        lines = text.splitlines()
        chapters = []
        current_chapter = None
        
        for line in lines:
            match = ChapterParser.CHAPTER_PATTERN.match(line)
            
            if match:
                # Save previous chapter if exists
                if current_chapter:
                    chapters.append(current_chapter)
                
                # Start new chapter
                try:
                    chapter_num = int(match.group(1))
                    title = match.group(2).strip()
                    
                    current_chapter = {
                        "chapter_number": chapter_num,
                        "title": title,
                        "content": []
                    }
                except (ValueError, IndexError) as e:
                    raise ValueError(f"Invalid chapter header format: {line}") from e
            else:
                # Accumulate content lines
                if current_chapter is not None:
                    current_chapter["content"].append(line)
        
        # Don't forget the last chapter
        if current_chapter:
            chapters.append(current_chapter)
        
        # Clean up content: join lines and strip whitespace
        for chapter in chapters:
            chapter["content"] = "\n".join(chapter["content"]).strip()
        
        return chapters
    
    @staticmethod
    def validate_chapters(chapters: List[Dict]) -> bool:
        """
        Validate chapter structure and content.
        
        Args:
            chapters: List of chapter dictionaries
            
        Returns:
            True if valid, raises ValueError otherwise
        """
        if not chapters:
            raise ValueError("No chapters parsed from input")
        
        for idx, ch in enumerate(chapters):
            required_keys = {"chapter_number", "title", "content"}
            if not required_keys.issubset(ch.keys()):
                raise ValueError(f"Chapter {idx} missing required fields: {required_keys}")
            
            if not isinstance(ch["chapter_number"], int):
                raise ValueError(f"Chapter {idx}: chapter_number must be integer")
            
            if not isinstance(ch["title"], str) or not ch["title"]:
                raise ValueError(f"Chapter {idx}: title must be non-empty string")
            
            if not isinstance(ch["content"], str):
                raise ValueError(f"Chapter {idx}: content must be string")
        
        return True


def parse_chapters(text: str) -> List[Dict]:
    """Convenience function for parsing chapters."""
    return ChapterParser.parse_chapters(text)
