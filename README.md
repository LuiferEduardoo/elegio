# Elegio

Open source project to help choose a presidential candidate for the 2026 republic in an intelligent way, through a test, viewing their proposals, filtering positions, comparing candidates, and more.

## 🎯 Overview

Elegio is a non-partisan platform designed to help voters make informed decisions by:
- Taking a comprehensive test to match with candidates
- Viewing and analyzing candidate proposals
- Filtering candidates by political positions
- Comparing candidates side by side
- Understanding the impact of proposals through AI analysis

## 🏗️ Architecture

```
elegio/
├── api/          # Backend FastAPI
├── frontend/     # Next.js web application
└── analysis/     # AI-powered proposal analysis
```

## 🚀 Tech Stack

### Backend
- **FastAPI** - High-performance async web framework
- **MySQL** - Relational database
- **SQLAlchemy 2.0** - Modern async ORM
- **Alembic** - Database migration tool
- **Pydantic v2** - Data validation

### Frontend
- **Next.js** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling

### AI
- **Gemini API** - Proposal analysis and insights
- **sentence-transformers** (`intfloat/multilingual-e5-large`) - 1024-dim multilingual embeddings for proposal chunks
- **Qdrant** - Vector database (cosine similarity) for semantic search over proposal chunks
- **rank-bm25** - In-memory lexical index fused with the dense results via Reciprocal Rank Fusion

## 📦 Installation

### Prerequisites
- Python 3.11+
- Node.js 20+
- MySQL 8+
- Docker (for the Qdrant vector store used by the search endpoint and the analysis pipelines)

### Backend Setup

```bash
cd api
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

Configure environment variables in `api/.env`:

```env
DATABASE_URL=mysql+aiomysql://user:password@localhost:3306/elegio
SECRET_KEY=your_secret_key
```

Run migrations:

```bash
alembic upgrade head
```

Start the server:

```bash
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Configure `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🛠️ Development

### Backend Commands
```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Run tests
pytest
```

### Frontend Commands
```bash
# Build for production
npm run build

# Run tests
npm test
```

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Reporting Issues
- Use the issue tracker to report bugs or suggest features
- Provide clear descriptions and steps to reproduce
- Include relevant screenshots when applicable

### Pull Requests
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes following our coding standards
4. Write tests for new functionality
5. Ensure all tests pass
6. Commit with conventional commits (`feat:`, `fix:`, `docs:`, etc.)
7. Push to your branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Coding Standards
- **Python**: Follow PEP 8, use Black formatter
- **TypeScript/React**: Use Prettier and ESLint
- Write meaningful commit messages
- Document complex logic

### Areas Where We Need Help
- [ ] Frontend UI improvements
- [ ] Additional test coverage
- [ ] Documentation enhancements
- [ ] Mobile responsiveness
- [ ] Accessibility improvements
- [ ] Internationalization (i18n)

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built for the community, by the community
- Non-partisan and open source
- Focused on informed voting

---

**Note**: This project is politically neutral and does not endorse any candidate or political party.
