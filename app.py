"""
Arabic Novel Parser - Streamlit Web Application

A production-ready web app for parsing Arabic novels into structured chapters.
Supports file upload, text pasting, processing, preview, copy, and download.
"""

import streamlit as st
import streamlit.components.v1 as components
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
            .copy-button {
                background-color: #0066cc;
                color: white;
                padding: 0.75rem 1.5rem;
                border: none;
                border-radius: 0.5rem;
                cursor: pointer;
                font-weight: bold;
                font-size: 16px;
                width: 100%;
                transition: background-color 0.3s;
            }
            .copy-button:hover {
                background-color: #0052a3;
            }
        </style>
    """, unsafe_allow_html=True)


def process_content(content: str) -> bool:
    """
    Process content and store in session state.
    
    Args:
        content: Raw text content to process
        
    Returns:
        True if successful, False otherwise
    """
    try:
        if not content or not content.strip():
            st.error("❌ Content is empty. Please enter or upload content with chapters.")
            return False
        
        # Parse chapters
        chapters = parse_chapters(content)
        
        # Validate
        ChapterParser.validate_chapters(chapters)
        
        # Store in session state
        st.session_state.chapters = chapters
        st.session_state.raw_content = content
        st.session_state.processed = True
        
        st.success(f"✅ Successfully processed {len(chapters)} chapters!")
        return True
        
    except UnicodeDecodeError:
        st.error("❌ File encoding error. Please ensure the file is UTF-8 encoded.")
        return False
    except ValueError as e:
        st.error(f"❌ Parsing error: {str(e)}")
        return False
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
        return False


def render_copy_button(text: str, label: str = "📋 Copy to Clipboard"):
    """Render a copy-to-clipboard button using a Streamlit component."""
    escaped_text = (
        text.replace('\\', '\\\\')
        .replace('`', '\\`')
        .replace('</script>', '<\\/script>')
        .replace('</textarea>', '<\\/textarea>')
    )

    button_html = f"""
    <div style="display: flex; flex-direction: column; gap: 0.5rem;">
        <button id="copy-btn" style="
            background-color: #0066cc;
            color: white;
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 0.5rem;
            cursor: pointer;
            font-weight: bold;
            font-size: 16px;
            width: 100%;
            transition: background-color 0.3s;
        ">{label}</button>
        <div id="copy-status" style="font-size: 0.9rem; min-height: 1.2rem;"></div>
    </div>
    <script>
        const copyButton = document.getElementById('copy-btn');
        const copyStatus = document.getElementById('copy-status');
        const originalLabel = copyButton.textContent;
        const textToCopy = `{escaped_text}`;

        function setStatus(message, color) {{
            copyStatus.textContent = message;
            copyStatus.style.color = color;
        }}

        async function copyText() {{
            try {{
                if (navigator.clipboard && window.isSecureContext) {{
                    await navigator.clipboard.writeText(textToCopy);
                }} else {{
                    const textarea = document.createElement('textarea');
                    textarea.value = textToCopy;
                    textarea.style.position = 'fixed';
                    textarea.style.left = '-9999px';
                    textarea.style.top = '-9999px';
                    document.body.appendChild(textarea);
                    textarea.focus();
                    textarea.select();
                    document.execCommand('copy');
                    document.body.removeChild(textarea);
                }}

                copyButton.textContent = '✅ Copied!';
                copyButton.style.backgroundColor = '#28a745';
                setStatus('Copied to clipboard.', '#0f5132');

                setTimeout(() => {{
                    copyButton.textContent = originalLabel;
                    copyButton.style.backgroundColor = '#0066cc';
                    setStatus('', '');
                }}, 2000);
            }} catch (error) {{
                console.error(error);
                setStatus('Copy failed. Use the download button if needed.', '#842029');
            }}
        }}

        copyButton.addEventListener('click', copyText);
        copyButton.addEventListener('mouseover', () => {{
            copyButton.style.backgroundColor = '#0052a3';
        }});
        copyButton.addEventListener('mouseout', () => {{
            if (copyButton.textContent === originalLabel) {{
                copyButton.style.backgroundColor = '#0066cc';
            }}
        }});
    </script>
    """
    components.html(button_html, height=90)


def main():
    """Main application function."""
    setup_page()
    
    # Header
    st.title("📖 Arabic Novel Parser")
    st.markdown("✨ **Transform your Arabic novels into structured, organized chapters** ✨")
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Information")
        st.markdown("""
        ### 🚀 How it works:
        1. **Upload** a TXT file OR **paste** chapters
        2. Click **Process**
        3. **Preview** results
        4. **Copy** or **Download** formatted output
        
        ### 📝 Expected Format:
        ```
        **الفصل 1: Title Here**
        Content of chapter 1...
        
        **الفصل 2: Another Title**
        Content of chapter 2...
        ```
        
        ### ✨ Features:
        - ✅ Upload TXT files
        - ✅ Paste text directly
        - ✅ Automatic chapter detection
        - ✅ UTF-8 Arabic text support
        - ✅ Large file handling (100k+ words)
        - ✅ **Copy to clipboard**
        - ✅ Download formatted output
        - ✅ Real-time statistics
        """)
    
    # Main content - Input section
    st.subheader("📤 Input Methods")
    
    # Tabs for upload or paste
    input_tab1, input_tab2 = st.tabs(["📁 Upload File", "📝 Paste Text"])
    
    with input_tab1:
        st.write("Upload a TXT file containing your chapters")
        uploaded_file = st.file_uploader(
            "Choose a TXT file",
            type=["txt"],
            help="Select your Arabic novel file (UTF-8 encoded)",
            key="file_uploader"
        )
        
        if uploaded_file is not None:
            col1, col2 = st.columns([3, 1])
            
            with col2:
                if st.button("🔄 Process File", use_container_width=True, key="upload_process"):
                    with st.spinner("Processing your file..."):
                        try:
                            content = uploaded_file.read().decode('utf-8')
                            process_content(content)
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
            
            with col1:
                st.info(f"📄 File: {uploaded_file.name} ({len(uploaded_file.getvalue() / 1024):.1f} KB)")
    
    with input_tab2:
        st.write("Paste your chapters directly")
        pasted_content = st.text_area(
            "Paste your chapters here",
            height=250,
            placeholder="""**الفصل 1: Title**
Content here...

**الفصل 2: Another Title**
More content...""",
            key="paste_area",
            help="Paste Arabic novel chapters formatted with **الفصل X: Title**"
        )
        
        col1, col2 = st.columns([3, 1])
        
        with col2:
            if st.button("🔄 Process Text", use_container_width=True, key="paste_process"):
                with st.spinner("Processing your text..."):
                    if process_content(pasted_content):
                        st.session_state.paste_area = ""
                        st.rerun()
        
        with col1:
            if pasted_content:
                char_count = len(pasted_content)
                st.info(f"📊 Characters: {char_count:,}")
    
    # Display results if processing completed
    if st.session_state.get("processed", False):
        st.divider()
        
        chapters = st.session_state.chapters
        
        # Statistics row
        st.subheader("📊 Statistics")
        stats = get_stats(chapters)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📖 Chapters Found", stats["chapter_count"])
        with col2:
            st.metric("📝 Total Words", f"{stats['total_words']:,}")
        with col3:
            st.metric("📄 Characters", f"{stats['total_characters']:,}")
        with col4:
            st.metric("📈 Avg/Chapter", f"{stats['avg_chapter_words']:.0f} words")
        
        st.divider()
        
        # Tabs for different views
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Preview", "📄 Chapter List", "⚙️ Details", "💾 Export"])
        
        with tab1:
            st.subheader("📋 Processed Output Preview")
            
            # Format chapters
            formatted_output = format_chapters(chapters)
            
            # Display with scrollable text area
            st.text_area(
                "Your formatted output",
                value=formatted_output,
                height=400,
                disabled=True,
                key="preview"
            )
            
            # Copy button for preview
            st.markdown("---")
            st.write("**Copy this output to use elsewhere:**")
            render_copy_button(formatted_output, "📋 Copy Formatted Output")
        
        with tab2:
            st.subheader("📄 Chapters Overview")
            
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
            st.subheader("⚙️ Processing Details")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**📈 File Statistics:**")
                st.write(f"- Total Chapters: **{stats['chapter_count']}**")
                st.write(f"- Total Words: **{stats['total_words']:,}**")
                st.write(f"- Total Characters: **{stats['total_characters']:,}**")
                st.write(f"- Average Words/Chapter: **{stats['avg_chapter_words']:.1f}**")
            
            with col2:
                st.write("**🎯 Sample Chapter (First):**")
                if chapters:
                    first = chapters[0]
                    st.write(f"**Number:** {first['chapter_number']}")
                    st.write(f"**Title:** {first['title']}")
                    st.write(f"**Content Preview:**")
                    preview = first['content'][:300]
                    st.write(preview + ("..." if len(first['content']) > 300 else ""))
        
        with tab4:
            st.subheader("💾 Export & Download")
            
            formatted_output = format_chapters(chapters)
            
            # Download formatted output
            st.markdown("#### 📥 Download Formatted Output")
            st.download_button(
                label="📥 Download as .txt",
                data=formatted_output.encode('utf-8'),
                file_name="chapters_processed.txt",
                mime="text/plain",
                help="Download the processed and formatted chapters",
                use_container_width=True
            )
            
            st.markdown("---")
            
            st.markdown("#### 📋 Copy to Clipboard")
            render_copy_button(formatted_output, "📋 Copy All Processed Data")
            
            st.markdown("---")
            
            # Download metadata
            st.markdown("#### 📄 Download Metadata")
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
                label="📄 Download Metadata as .txt",
                data=json_format.encode('utf-8'),
                file_name="chapters_metadata.txt",
                mime="text/plain",
                help="Download chapter metadata and statistics",
                use_container_width=True
            )
        
        st.divider()
        
        # Reset button
        col1, col2, col3 = st.columns(3)
        with col2:
            if st.button("🔄 Reset & Process New Content", use_container_width=True):
                st.session_state.processed = False
                st.session_state.chapters = []
                st.session_state.raw_content = ""
                st.rerun()
    
    else:
        st.info("👆 Upload a file or paste content above to get started!")


if __name__ == "__main__":
    # Initialize session state
    if "processed" not in st.session_state:
        st.session_state.processed = False
    if "chapters" not in st.session_state:
        st.session_state.chapters = []
    if "raw_content" not in st.session_state:
        st.session_state.raw_content = ""
    
    main()
