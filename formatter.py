"""
Chapter Formatter

Formats parsed chapters into structured output with proper separators and spacing.
Ensures no duplicate separators or trailing whitespace issues.
"""

from typing import List, Dict, Optional


class ChapterFormatter:
    """Format chapters into structured text output."""
    
    SEPARATOR = "---"
    CHAPTER_FIELDS = ["chapter_number", "title", "is_published", "content"]
    
    @staticmethod
    def format_single_chapter(chapter: Dict, include_metadata: bool = True) -> str:
        """
        Format a single chapter into structured text.
        
        Args:
            chapter: Dictionary with chapter_number, title, content
            include_metadata: Whether to include is_published field
            
        Returns:
            Formatted chapter string
        """
        lines = []
        
        # Add chapter metadata
        lines.append(f"chapter_number: {chapter['chapter_number']}")
        lines.append(f"title: {chapter['title']}")
        
        if include_metadata:
            lines.append("is_published: true")
        
        # Add content with "content:" label
        lines.append("content:")
        lines.append(chapter["content"])
        
        return "\n".join(lines)
    
    @staticmethod
    def format_chapters(chapters: List[Dict]) -> str:
        """
        Format multiple chapters with proper separators.
        
        Ensures:
        - Exactly one separator between chapters
        - No duplicate separators
        - No leading/trailing separators
        - Consistent spacing
        
        Args:
            chapters: List of chapter dictionaries
            
        Returns:
            Formatted text with all chapters
            
        Raises:
            ValueError: If chapters list is empty or invalid
        """
        if not chapters:
            raise ValueError("Cannot format empty chapter list")
        
        if not isinstance(chapters, list):
            raise ValueError("Chapters must be a list")
        
        # Format each chapter
        formatted_blocks = []
        for chapter in chapters:
            block = ChapterFormatter.format_single_chapter(chapter)
            formatted_blocks.append(block)
        
        # Join with single separator (no extra newlines)
        output = f"\n{ChapterFormatter.SEPARATOR}\n".join(formatted_blocks)
        
        return output
    
    @staticmethod
    def format_chapters_with_metadata(chapters: List[Dict]) -> str:
        """
        Format chapters with additional metadata (chapter count, etc).
        
        Args:
            chapters: List of chapter dictionaries
            
        Returns:
            Formatted text with metadata header
        """
        metadata = f"# Total Chapters: {len(chapters)}\n\n"
        content = ChapterFormatter.format_chapters(chapters)
        return metadata + content
    
    @staticmethod
    def get_stats(chapters: List[Dict]) -> Dict:
        """
        Get statistics about the chapters.
        
        Args:
            chapters: List of chapter dictionaries
            
        Returns:
            Dictionary with stats: chapter_count, total_words, etc.
        """
        if not chapters:
            return {
                "chapter_count": 0,
                "total_words": 0,
                "avg_chapter_words": 0
            }
        
        chapter_count = len(chapters)
        total_words = sum(
            len(ch["content"].split()) for ch in chapters
        )
        avg_words = total_words / chapter_count if chapter_count > 0 else 0
        
        return {
            "chapter_count": chapter_count,
            "total_words": total_words,
            "avg_chapter_words": round(avg_words, 1),
            "total_characters": sum(len(ch["content"]) for ch in chapters)
        }


def format_chapters(chapters: List[Dict]) -> str:
    """Convenience function for formatting chapters."""
    return ChapterFormatter.format_chapters(chapters)


def get_stats(chapters: List[Dict]) -> Dict:
    """Convenience function for getting statistics."""
    return ChapterFormatter.get_stats(chapters)
