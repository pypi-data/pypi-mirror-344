# Copyright (c) 2025 RePromptsQuest
# Licensed under the MIT License

import os
import streamlit as st
from backend import backend, prompt_generator

# ----------------------------
# Streamlit Page Configuration
# ----------------------------
st.set_page_config(
    page_title="Repmt - Repository Prompt Generator",
    layout="wide",
    page_icon="🔍"
)

# ----------------------------
# Custom CSS for Styling
# ----------------------------
st.markdown("""
<style>
    .header {
        color: #2c3e50;
        border-bottom: 2px solid #4F8BF9;
        padding-bottom: 10px;
    }
    .info-box {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        color: #212529;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    .stButton>button {
        background-color: #4F8BF9;
        color: white;
        border-radius: 5px;
    }
    .stTextArea textarea {
        font-family: 'Courier New', monospace;
        background-color: #f8f9fa;
        color: #212529;
    }
    .copy-btn {
        margin-bottom: 10px;
    }
    code {
        color: #e83e8c;
        background-color: #f8f9fa;
        padding: 2px 4px;
        border-radius: 4px;
    }
    .issue-search {
        margin-top: 20px;
    }
    .generate-btn {
        margin-top: 10px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Header Section
# ----------------------------
st.title("🔍 Repmt - Repository Prompt Generator")
st.markdown("""
<div class="info-box">
    <h4 style="color: #2c3e50;">📦 Installation Guide</h4>
    <p>Install with pip: <code>pip install repmt</code></p>
    <p>Uninstall when done: <code>pip uninstall repmt</code></p>
</div>
""", unsafe_allow_html=True)
st.markdown("""
This tool analyzes the repository in the current directory and generates various prompts for GPT.
It automatically ignores virtual environments and dependency folders.
""")

# ----------------------------
# Repository Discovery & Analysis
# ----------------------------
repo_path = os.getcwd()
st.info(f"**Analyzing repository at:** `{repo_path}`")

with st.spinner("🔍 Scanning repository structure..."):
    repo_structure = backend.get_directory_structure(repo_path)
    repo_analysis  = backend.scan_repo(repo_path)

st.subheader("📂 Directory Structure")
st.code(repo_structure, language="bash")

# ----------------------------
# Sidebar: Prompt Options
# ----------------------------
with st.sidebar:
    st.markdown("### ⚙️ Analysis Options")
    prompt_option = st.selectbox(
        "Select Prompt Type",
        [
            "README.md Prompt",
            "Repository Overview",
            "Code Flow",
            "Structure Understanding",
            "Module Specific Prompt",
            "Search for Issue"
        ]
    )

    # Ensure our list always exists
    if 'selected_modules' not in st.session_state:
        st.session_state.selected_modules = []

    if prompt_option == "Module Specific Prompt":
        st.markdown("---")
        st.markdown("### 🗂 Module Selection")
        with st.expander("Repository Structure", expanded=True):
            for module_path in sorted(repo_analysis.keys()):
                # sanitize the key so slashes/ backslashes don’t break Streamlit widget keys
                widget_key = f"module_{module_path.replace(os.sep, '_')}"
                # checkbox’s value reflects membership in selected_modules
                checked = st.checkbox(
                    module_path, 
                    key=widget_key, 
                    value=(module_path in st.session_state.selected_modules)
                )
                # add or remove cleanly
                if checked and module_path not in st.session_state.selected_modules:
                    st.session_state.selected_modules.append(module_path)
                if not checked and module_path in st.session_state.selected_modules:
                    st.session_state.selected_modules.remove(module_path)

# ----------------------------
# Prompt Generation Logic
# ----------------------------
generated_prompt = ""
if prompt_option == "README.md Prompt":
    generated_prompt = prompt_generator.generate_readme_prompt(repo_structure, repo_analysis)
elif prompt_option == "Repository Overview":
    generated_prompt = prompt_generator.generate_overview_prompt(repo_structure, repo_analysis)
elif prompt_option == "Code Flow":
    generated_prompt = prompt_generator.generate_flow_prompt(repo_structure, repo_analysis)
elif prompt_option == "Structure Understanding":
    generated_prompt = prompt_generator.generate_structure_prompt(repo_structure, repo_analysis)
elif prompt_option == "Module Specific Prompt":
    if st.session_state.selected_modules:
        generated_prompt = prompt_generator.generate_module_prompt(
            st.session_state.selected_modules,
            repo_structure,
            repo_analysis
        )
    else:
        st.warning("⚠️ Please select at least one module from the repository structure")
elif prompt_option == "Search for Issue":
    st.markdown("### 🔎 Search for Issue")
    issue_description = st.text_area(
        "Describe the issue you're looking for:",
        placeholder="e.g., 'Authentication not working' or 'Database connection error'",
        height=100,
        key="issue_description"
    )
    if st.button(
        "Generate Prompt", 
        key="generate_issue_prompt", 
        type="primary", 
        help="Click to generate prompt based on the issue description",
        use_container_width=True,
        disabled=not issue_description
    ):
        generated_prompt = prompt_generator.generate_issue_search_prompt(
            repo_structure,
            repo_analysis,
            issue_description
        )

# ----------------------------
# Display & Copy/Download
# ----------------------------
if generated_prompt:
    st.subheader("📝 Generated Prompt")
    if st.button("📋 Copy Prompt", key="copy_button", help="Click to copy prompt to clipboard"):
        st.write(
            '<script>navigator.clipboard.writeText(`' 
            + generated_prompt.replace('`', '\\`') + '`);</script>',
            unsafe_allow_html=True
        )
        st.success("Prompt copied to clipboard!")
    st.text_area("Prompt Content", generated_prompt, height=400, label_visibility="collapsed", key="prompt_area")
    st.download_button("Download Prompt", generated_prompt, file_name="repository_prompt.txt")
