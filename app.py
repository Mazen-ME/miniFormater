"""
Arabic Novel Parser - Streamlit Web Application

A production-ready web app for parsing Arabic novels into structured chapters.
Supports file upload, processing, preview, and download.
"""

import streamlit as st
import io
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from parser import parse_chapters, ChapterParser
from formatter import format_chapters, get_stats


def setup_page():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="Arabic Novel Parser",
        page_icon="📖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
        <style>
            .main {
                max-width: 1200px;
            }
            .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
                font-size: 1rem;
            }
            .info-box {
                background-color: #f0f2f6;
                padding: 1rem;
                border-radius: 0.5rem;
                margin: 1rem 0;
            }
            .success-box {
                background-color: #d1e7dd;
                padding: 1rem;
                border-radius: 0.5rem;
                margin: 1rem 0;
                color: #0f5132;
            }
            .error-box {
                background-color: #f8d7da;
                padding: 1rem;
                border-radius: 0.5rem;
                margin: 1rem 0;
                color: #842029;
            }
        </style>
    """, unsafe_allow_html=True)


def main():
    """Main application function."""
    setup_page()
    
    # Header
    st.title("📖 Arabic Novel Parser")
    st.markdown("Transform your Arabic novels into structured, organized chapters")
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Information")
        st.markdown("""
        ### How it works:
        1. Upload a TXT file with chapters
        2. Click Process
        3. Preview results
        4. Download formatted output
        
        ### Expected Format:
        ```
        **الفصل 1: Title Here**
        Content of chapter 1...
        
        **الفصل 2: Another Title**
        Content of chapter 2...
        ```
        
        ### Features:
        - ✅ Automatic chapter detection
        - ✅ UTF-8 Arabic text support
        - ✅ Large file handling (100k+ words)
        - ✅ Instant download
        """)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📤 Upload & Process")
        uploaded_file = st.file_uploader(
            "Choose a TXT file",
            type=["txt"],
            help="Select your Arabic novel file"
        )
    
    # Process button
    if uploaded_file is not None:
        with col2:
            st.write("")  # Vertical spacing
            process_clicked = st.button(
                "🔄 Process File",
                use_container_width=True,
                key="process_btn"
            )
        
        if process_clicked:
            with st.spinner("Processing your file..."):
                try:
                    # Read and decode file
                    content = uploaded_file.read().decode('utf-8')
                    
                    if not content.strip():
                        st.error("❌ File is empty. Please upload a file with content.")
                        return
                    
                    # Parse chapters
                    chapters = parse_chapters(content)
                    
                    # Validate
                    ChapterParser.validate_chapters(chapters)
                    
                    # Store in session state
                    st.session_state.chapters = chapters
                    st.session_state.raw_content = content
                    st.session_state.processed = True
                    
                    st.success(f"✅ Successfully processed {len(chapters)} chapters!")
                    
                except UnicodeDecodeError:
                    st.error(
                        "❌ File encoding error. Please ensure the file is UTF-8 encoded."
                    )
                except ValueError as e:
                    st.error(f"❌ Parsing error: {str(e)}")
                except Exception as e:
                    st.error(f"❌ Unexpected error: {str(e)}")
    
    # Display results if processing completed
    if st.session_state.get("processed", False):
        st.divider()
        
        chapters = st.session_state.chapters
        
        # Statistics
        stats = get_stats(chapters)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📊 Chapters Found", stats["chapter_count"])
        with col2:
            st.metric("📝 Total Words", f"{stats['total_words']:,}")
        with col3:
            st.metric("📄 Characters", f"{stats['total_characters']:,}")
        with col4:
            st.metric("📈 Avg/Chapter", f"{stats['avg_chapter_words']:.0f} words")
        
        st.divider()
        
        # Tabs for different views
        tab1, tab2, tab3 = st.tabs(["📋 Preview", "📄 Chapter List", "⚙️ Details"])
        
        with tab1:
            st.subheader("Output Preview")
            
            # Format chapters
            formatted_output = format_chapters(chapters)
            
            # Display with scrollable text area
            st.text_area(
                "Formatted Output (Read-only)",
                value=formatted_output,
                height=400,
                disabled=True,
                key="preview"
            )
        
        with tab2:
            st.subheader("Chapters Overview")
            
            # Create chapter list
            chapter_data = []
            for ch in chapters:
                word_count = len(ch["content"].split())
                chapter_data.append({
                    "Chapter": f"الفصل {ch['chapter_number']}",
                    "Title": ch["title"],
                    "Words": word_count,
                    "Status": "Published"
                })
            
            st.dataframe(
                chapter_data,
                use_container_width=True,
                hide_index=True
            )
        
        with tab3:
            st.subheader("Processing Details")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**File Statistics:**")
                st.write(f"- Total Chapters: {stats['chapter_count']}")
                st.write(f"- Total Words: {stats['total_words']:,}")
                st.write(f"- Total Characters: {stats['total_characters']:,}")
                st.write(f"- Average Words/Chapter: {stats['avg_chapter_words']:.1f}")
            
            with col2:
                st.write("**Sample Chapter (First):**")
                if chapters:
                    first = chapters[0]
                    st.write(f"**Number:** {first['chapter_number']}")
                    st.write(f"**Title:** {first['title']}")
                    st.write(f"**Content Preview:**")
                    preview = first['content'][:200]
                    st.write(preview + ("..." if len(first['content']) > 200 else ""))
        
        st.divider()
        
        # Download section
        st.subheader("💾 Download Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            formatted_output = format_chapters(chapters)
            
            st.download_button(
                label="📥 Download Formatted Output (.txt)",
                data=formatted_output.encode('utf-8'),
                file_name="novels_processed.txt",
                mime="text/plain",
                help="Download the processed and formatted chapters",
                use_container_width=True
            )
        
        with col2:
            # Also offer raw JSON-like format
            json_format = "[\n"
            for ch in chapters:
                json_format += f"""  {{
    "chapter_number": {ch['chapter_number']},
    "title": "{ch['title']}",
    "is_published": true,
    "word_count": {len(ch['content'].split())}
  }},
"""
            json_format = json_format.rstrip(",\n") + "\n]"
            
            st.download_button(
                label="📥 Download Metadata (.txt)",
                data=json_format.encode('utf-8'),
                file_name="chapters_metadata.txt",
                mime="text/plain",
                help="Download metadata about chapters",
                use_container_width=True
            )
        
        # Reset button
        if st.button("🔄 Reset & Upload New File", use_container_width=True):
            st.session_state.processed = False
            st.session_state.chapters = []
            st.session_state.raw_content = ""
            st.rerun()
    
    else:
        st.info("👆 Upload a TXT file to get started")


if __name__ == "__main__":
    # Initialize session state
    if "processed" not in st.session_state:
        st.session_state.processed = False
    if "chapters" not in st.session_state:
        st.session_state.chapters = []
    if "raw_content" not in st.session_state:
        st.session_state.raw_content = ""
    
    main()
