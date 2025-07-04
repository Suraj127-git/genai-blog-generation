import streamlit as st
import requests
import os
from uiconfigfile import Config
import json

# Resolve config file path and initialize
base_dir = os.path.dirname(__file__)
config_path = os.path.join(base_dir, 'uiconfigfile.ini')
config = Config(config_file=config_path)

# Page config & title
st.set_page_config(page_title=config.get_page_title(), layout="wide")

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    .blog-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    .blog-title {
        color: #2c3e50;
        border-bottom: 3px solid #3498db;
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
    }
    .blog-meta {
        background: black;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        border-left: 4px solid #3498db;
    }
    .section-header {
        color: #34495e;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #ecf0f1;
    }
    .content-text {
        line-height: 1.8;
        color: #2c3e50;
        text-align: justify;
        font-size: 1.1rem;
    }
    .sidebar-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        text-align: center;
    }
    .generate-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.75rem 2rem;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        cursor: pointer;
        width: 100%;
        margin-top: 1rem;
    }
    .status-success {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    .status-error {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown(f"""
<div class="main-header">
    <h1 style="margin: 0; font-size: 2.5rem;">🚀 {config.get_page_title()}</h1>
    <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">Generate engaging blog content with AI</p>
</div>
""", unsafe_allow_html=True)

# Sidebar inputs
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <h2 style="margin: 0;">⚙️ Blog Settings</h2>
    </div>
    """, unsafe_allow_html=True)
    
    topic = st.text_input(
        "📝 Enter Blog Topic", 
        placeholder="e.g., The Future of AI",
        help="Enter a topic you want to write about"
    )
    
    language = st.selectbox(
        "🌍 Select Language", 
        ["English", "Hindi"], 
        index=0,
        help="Choose the language for your blog"
    )
    
    llm_type = st.selectbox(
        "🤖 Select LLM Type", 
        config.get_llm_options(),
        help="Choose the AI model provider"
    )
    
    model = st.selectbox(
        "🧠 Select Model",
        config.get_groq_model_options() if llm_type == "Groq" else config.get_ollama_model_options(),
        help="Choose the specific model to use"
    )
    
    generate = st.button("✨ Generate Blog", type="primary", use_container_width=True)

# Function to display blog content with copy/download options
def display_blog_content(blog_data):
    """Display blog content with copy and download options"""
    
    # Convert to pretty JSON string
    json_str = json.dumps(blog_data, indent=2, ensure_ascii=False)
    
    # Display meta information
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="blog-meta">
            <strong>🌍 Language:</strong> {language}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="blog-meta">
            <strong>🤖 Model:</strong> {llm_type} - {model}
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="blog-meta">
            <strong>📝 Topic:</strong> {topic}
        </div>
        """, unsafe_allow_html=True)
    
    # Content display area
    st.markdown("""
    <div class="blog-container">
        <h3 style="color: #2c3e50; margin-bottom: 1rem;">📄 Generated Blog Content</h3>
        <p style="color: #7f8c8d; margin-bottom: 1.5rem;">
            Your blog has been generated successfully! Use the options below to copy or download the content.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        # Download as JSON
        st.download_button(
            label="📥 Download JSON",
            data=json_str,
            file_name=f"{topic.replace(' ', '_')}_blog.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col2:
        # Download as Text (try to extract readable content)
        try:
            if isinstance(blog_data, dict):
                title = blog_data.get("title", "Generated Blog")
                content = blog_data.get("content", "")
                text_content = f"# {title}\n\n{content}"
            else:
                text_content = str(blog_data)
            
            st.download_button(
                label="📝 Download Text",
                data=text_content,
                file_name=f"{topic.replace(' ', '_')}_blog.txt",
                mime="text/plain",
                use_container_width=True
            )
        except:
            st.download_button(
                label="📝 Download Text",
                data=json_str,
                file_name=f"{topic.replace(' ', '_')}_blog.txt",
                mime="text/plain",
                use_container_width=True
            )
    
    with col3:
        # Copy to clipboard info
        st.markdown("""
        <div style="background: #e8f4f8; padding: 0.75rem; border-radius: 8px; text-align: center;">
            <small style="color: #2c3e50;">💡 Use Ctrl+A, Ctrl+C to copy from the text area below</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Expandable JSON viewer
    with st.expander("🔍 View/Copy JSON Content", expanded=True):
        st.text_area(
            label="Generated Blog JSON",
            value=json_str,
            height=400,
            help="You can select all (Ctrl+A) and copy (Ctrl+C) this content",
            label_visibility="collapsed"
        )
    
    # Try to extract and show readable content if possible
    try:
        if isinstance(blog_data, dict):
            title = blog_data.get("title", "")
            content = blog_data.get("content", "")
            
            if title or content:
                with st.expander("📖 Readable Content Preview", expanded=False):
                    if title:
                        st.markdown(f"**Title:** {title}")
                    if content:
                        st.markdown(f"**Content:** {content}")
    except:
        pass

# Main content area
if generate:
    if not topic:
        st.markdown("""
        <div class="status-error">
            <strong>⚠️ Error:</strong> Please enter a blog topic to generate content.
        </div>
        """, unsafe_allow_html=True)
    else:
        with st.spinner("🔄 Generating your amazing blog content..."):
            payload = {
                "topic": topic,
                "llm": llm_type,
                "model": model,
                "language": language.lower()
            }
            
            try:
                resp = requests.post("http://localhost:8000/blogs", json=payload)
                
                if resp.status_code != 200:
                    try:
                        err = resp.json()
                        msg = err.get("detail") or err.get("error", {}).get("message") or str(err)
                    except Exception:
                        msg = resp.text
                    
                    st.markdown(f"""
                    <div class="status-error">
                        <strong>❌ Generation Failed:</strong> {msg}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    # Success message
                    st.markdown("""
                    <div class="status-success">
                        <strong>✅ Success:</strong> Your blog has been generated successfully!
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Process and display the response
                    raw = resp.json()
                    data = raw.get("data") or raw
                    content_block = data.get("blog") or data
                    
                    # Display the formatted blog content
                    display_blog_content(content_block)
                    
                    # Add download button
                    if isinstance(content_block, dict):
                        blog_text = f"# {content_block.get('title', 'Blog')}\n\n{content_block.get('content', '')}"
                        st.download_button(
                            label="📥 Download Blog as Text",
                            data=blog_text,
                            file_name=f"{topic.replace(' ', '_')}_blog.txt",
                            mime="text/plain"
                        )
            
            except requests.exceptions.RequestException as e:
                st.markdown(f"""
                <div class="status-error">
                    <strong>🔌 Connection Error:</strong> Could not connect to the blog generation service. Please check if the server is running.
                </div>
                """, unsafe_allow_html=True)

else:
    # Welcome message when no blog is generated
    st.markdown("""
    <div class="blog-container" style="text-align: center; padding: 3rem;">
        <h2 style="color: #7f8c8d; margin-bottom: 1rem;">👋 Welcome to AI Blog Generator</h2>
        <p style="color: #95a5a6; font-size: 1.1rem; line-height: 1.6;">
            Use the sidebar to configure your blog settings and generate engaging content with AI.<br>
            Simply enter a topic, choose your preferences, and let our AI create amazing blog content for you!
        </p>
        <div style="margin-top: 2rem;">
            <p style="color: #3498db; font-size: 1rem;">
                💡 <strong>Tip:</strong> Try topics like "The Future of AI", "Sustainable Living", or "Digital Marketing Trends"
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)