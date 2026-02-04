# 🔬 AI Deep Research Agent

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31-red.svg)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-Latest-yellow.svg)](https://langchain.com/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> **Production-grade deep research agent that combines academic databases (Arxiv, PubMed), web search, and LLM analysis to provide comprehensive research summaries. Built with modern LLM frameworks and ready for HuggingFace deployment.**

---

## ✨ Features

- 🔬 **Multi-Source Research**: Searches Arxiv, PubMed, and web simultaneously
- 🤖 **Multi-LLM Support**: Works with OpenAI GPT-4, Anthropic Claude, and Google Gemini
- 📊 **Structured Analysis**: Extracts key findings, generates summaries, and provides citations
- 💡 **Smart Synthesis**: Identifies patterns, consensus, and research gaps across papers
- 📥 **Export Results**: Download comprehensive research reports as JSON
- 🔒 **Secure**: Environment-based API key management, no hardcoded secrets
- 🐳 **Docker Ready**: One-command deployment with multi-stage optimized builds
- ⚡ **Fast**: Async operations with retry logic and rate limiting

---

## 🎬 Demo

![Research Agent Demo](docs/demo.png)

### Example Research Query

**Input:** "What are the latest developments in transformer architectures for computer vision?"

**Output:**
- Comprehensive summary of 10+ papers
- 5-7 key findings
- Citation graph and metadata
- Downloadable JSON report

---

## 🚀 Quick Start

### Option 1: Local Python

```bash
# Clone repository
git clone https://github.com/your-username/ai-deep-research-agent.git
cd ai-deep-research-agent

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Set up environment (copy and edit .env)
cp .env.example .env
# Add your API keys to .env

# Run application
streamlit run app.py
```

Open http://localhost:8501 in your browser!

### Option 2: Docker

```bash
# Build image
docker build -t ai-deep-research-agent .

# Run container
docker run -p 7860:7860 \
  -e OPENAI_API_KEY=your-key-here \
  ai-deep-research-agent
```

---

## 📋 Requirements

- Python 3.11+
- At least ONE of the following API keys:
  - OpenAI API key (GPT-4 recommended)
  - Anthropic API key (Claude 3)
  - Google API key (Gemini Pro)

---

## 🏗️ Architecture

```
ai-deep-research-agent/
├── src/
│   ├── agents/
│   │   └── research_agent.py    # Core research logic
│   ├── models/
│   │   └── config.py            # Type-safe configurations
│   ├── tools/
│   │   └── research_tools.py    # Arxiv, PubMed, Web search
│   └── utils/
│       ├── logging.py           # Structured logging
│       └── exceptions.py        # Custom exceptions
├── tests/                       # Test suite
├── app.py                      # Streamlit UI
├── Dockerfile                  # Production container
└── requirements.txt            # Dependencies
```

### Technology Stack

- **Frontend**: Streamlit with custom CSS
- **LLM Integration**: LangChain (OpenAI, Anthropic, Google)
- **Research Sources**: Arxiv API, PubMed/NCBI E-utilities, DuckDuckGo
- **Configuration**: Pydantic Settings
- **Logging**: Loguru (structured JSON logs)
- **Testing**: Pytest with 80%+ coverage

---

## 🔧 Configuration

### Environment Variables (.env)

```bash
# LLM API Keys (at least one required)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...

# Application Config
APP_LOG_LEVEL=INFO
APP_ENVIRONMENT=production
APP_MAX_REQUESTS_PER_MINUTE=10

# Research Config
RESEARCH_MAX_PAPERS=10
RESEARCH_MAX_DEPTH=3
```

### Model Configuration

Edit `src/models/config.py` to customize:
- LLM provider (OpenAI/Anthropic/Google)
- Model name (GPT-4, Claude 3 Sonnet, Gemini Pro)
- Temperature and max tokens
- Research depth and sources

---

## 📖 Usage Examples

### Basic Research

```python
from src.agents.research_agent import DeepResearchAgent
from src.models.config import ModelConfig, ResearchConfig, APIConfig

# Configure
api_config = APIConfig(openai_api_key="your-key")
model_config = ModelConfig(provider="openai", model_name="gpt-4-turbo-preview")
research_config = ResearchConfig(max_papers=10)

# Initialize agent
agent = DeepResearchAgent(model_config, research_config, api_config)

# Conduct research
result = await agent.research("What is the state of quantum computing?")

print(result.summary)
print(result.key_findings)
```

### Advanced: Custom Sources

```python
research_config = ResearchConfig(
    max_papers=20,
    sources=["arxiv", "pubmed"],  # Only academic sources
    enable_citations=True
)
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/unit/test_research_agent.py -v
```

---

## 🐳 Docker Deployment

### Build for Production

```bash
docker build -t yourusername/ai-deep-research-agent:latest .
```

### Deploy to HuggingFace Spaces

1. Create a new Space on HuggingFace
2. Select "Docker" as SDK
3. Clone this repository
4. Push to your Space repository:

```bash
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/ai-deep-research-agent
git push hf main
```

5. Add API keys in Space settings (Secrets)

---

## 📊 Performance

- **Average Query Time**: 15-30 seconds (depending on sources)
- **Papers Processed**: Up to 20 per query
- **Concurrent Users**: Supports multiple users with rate limiting
- **Memory Usage**: ~500MB (container)

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Run tests (`pytest`)
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [OpenAI](https://openai.com/), [Anthropic](https://anthropic.com/), [Google Gemini](https://deepmind.google/technologies/gemini/)
- Research sources: [Arxiv](https://arxiv.org/), [PubMed](https://pubmed.ncbi.nlm.nih.gov/)
- Inspired by [awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps)

---

## 📧 Contact

**Your Name**

Project Link: [https://github.com/your-username/ai-deep-research-agent](https://github.com/your-username/ai-deep-research-agent)

---

## 📊 Citation

If you use this project in your research, please cite:

```bibtex
@software{ai_deep_research_agent,
  author = {Your Name},
  title = {AI Deep Research Agent: Production-Grade Academic Research Tool},
  year = {2026},
  url = {https://github.com/your-username/ai-deep-research-agent}
}
```

---

<div align="center">
  <strong>⭐ Star this repository if you find it useful!</strong>
  <br>
  <sub>Built with ❤️ for researchers, students, and AI enthusiasts</sub>
</div>
