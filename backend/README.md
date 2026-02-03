# Blog Generation Backend

FastAPI backend for AI-powered blog generation with document import and export capabilities.

## Features

- 🔐 **Authentication**: JWT-based auth with session management
- 📝 **Blog Generation**: AI-powered blog creation using GroqAI and LangChain
- 📄 **Document Import**: Upload and process PDF, DOCX, and TXT files
- 💾 **Vector Storage**: ChromaDB for document embeddings and semantic search
- 📥 **Export**: Download blogs as PDF or DOCX
- 📊 **History Tracking**: Track all generated blogs per user
- 🎯 **Dynamic Categorization**: Automatic topic categorization
- 🌐 **Multi-language**: Support for multiple languages

## Tech Stack

- **FastAPI**: Modern Python web framework
- **MongoDB**: Document database with Motor async driver
- **ChromaDB**: Vector database for embeddings
- **LangChain**: LLM orchestration framework
- **LangGraph**: Workflow management for blog generation
- **GroqAI**: Fast LLM inference

## Setup

### Prerequisites

- Python 3.10+
- MongoDB (running locally or remote)
- ChromaDB (optional, for document-based generation)
- GroqAI API key

### Installation

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate virtual environment:
```bash
# Windows
.\\venv\\Scripts\\activate

# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy `.env.example` to `.env` and configure:
```bash
cp .env.example .env
```

5. Update `.env` with your configuration:
```env
MONGODB_URL=mongodb://localhost:27017
GROQ_API_KEY=your-groq-api-key
CHROMADB_HOST=localhost
CHROMADB_PORT=8000
JWT_SECRET_KEY=your-secret-key
```

### Running the Application

Development mode:
```bash
python -m uvicorn app.main:app --reload --port 8000
```

Or:
```bash
python app/main.py
```

The API will be available at `http://localhost:8000`

API documentation (Swagger): `http://localhost:8000/docs`

## API Endpoints

### Authentication

- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/auth/logout` - Logout user
- `GET /api/v1/auth/me` - Get current user profile

### Blogs

- `POST /api/v1/blogs/generate` - Generate a blog
- `GET /api/v1/blogs/history` - Get blog history (paginated)
- `GET /api/v1/blogs/{blog_id}` - Get specific blog
- `DELETE /api/v1/blogs/{blog_id}` - Delete blog
- `GET /api/v1/blogs/{blog_id}/download/{format}` - Download blog (pdf/docx)

### Documents

- `POST /api/v1/documents/upload` - Upload document (PDF/TXT/DOCX)
- `GET /api/v1/documents` - List user's documents
- `GET /api/v1/documents/{doc_id}` - Get document details
- `DELETE /api/v1/documents/{doc_id}` - Delete document

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Settings and configuration
│   ├── auth/                # Authentication
│   │   ├── jwt.py          # JWT utilities
│   │   └── dependencies.py # Auth dependencies
│   ├── database/           # Database connections
│   │   ├── mongodb.py      # MongoDB setup
│   │   └── chromadb.py     # ChromaDB setup
│   ├── models/             # Data models
│   │   ├── user.py
│   │   ├── blog.py
│   │   ├── document.py
│   │   └── session.py
│   ├── schemas/            # Pydantic schemas
│   │   ├── auth.py
│   │   ├── blog.py
│   │   └── document.py
│   ├── routers/            # API routes
│   │   ├── auth.py
│   │   ├── blogs.py
│   │   └── documents.py
│   └── services/           # Business logic
│       ├── llm_service.py
│       ├── graph_service.py
│       ├── document_service.py
│       ├── export_service.py
│       └── session_service.py
├── tests/                  # Tests
├── requirements.txt
├── .env.example
└── README.md
```

## Environment Variables

See `.env.example` for all available configuration options.

## Development

### Running Tests

```bash
pytest tests/ -v
```

### Code Quality

The project follows PEP 8 style guidelines.

## License

MIT
