# Blog Generation with LangGraph and Groq

A powerful blog generation application that leverages LangGraph and Groq's LLM capabilities to create high-quality blog content. The application features a user-friendly Streamlit interface and a FastAPI backend.

## Features

- **Intuitive UI**: Built with Streamlit for easy blog topic input and LLM model selection
- **Flexible LLM Support**: Integration with Groq's powerful language models
- **Modular Architecture**: Well-organized codebase with separate modules for UI, LLM integration, and graph processing
- **FastAPI Backend**: Robust API server handling blog generation requests

## Project Structure

```
src/
├── graphs/         # LangGraph configuration and setup
├── llms/           # LLM integration (Groq)
├── nodes/          # Graph nodes for processing
├── states/         # State management
└── ui/             # Streamlit UI components
```

## Prerequisites

- Python 3.x
- Virtual environment (recommended)

## Installation

1. Clone the repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   - Copy `_copy.env` to `.env`
   - Add your Groq API key to `.env`

## Running the Application

1. Start the FastAPI backend:
   ```bash
   python app.py
   ```

2. Launch the Streamlit UI:
   ```bash
   streamlit run src/ui/BlogUi.py
   ```

3. Access the UI through your web browser at `http://localhost:8501`

## Usage

1. Enter your desired blog topic in the text input field
2. Select the LLM type (Groq)
3. Choose a specific model from the available options
4. Click "Generate Blog" to create your content
5. The generated blog will appear below the form

## Configuration

UI settings can be modified in `src/ui/uiconfigfile.ini`:
- Page title
- Available LLM options
- Model selections

## Project Components

- `app.py`: FastAPI server handling blog generation requests
- `src/ui/BlogUi.py`: Streamlit interface for user interaction
- `src/llms/groqllm.py`: Groq LLM integration
- `src/graphs/graph_builder.py`: LangGraph configuration
- `src/nodes/blog_node.py`: Processing nodes for blog generation
- `src/states/blogstate.py`: State management for the generation process