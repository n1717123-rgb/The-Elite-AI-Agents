"""
AI Deep Research Agent - Streamlit UI
Professional interface with modern design
"""
import asyncio
import streamlit as st
from datetime import datetime
from pathlib import Path

from src.agents.research_agent import DeepResearchAgent, ResearchResult
from src.models.config import ModelConfig, ResearchConfig, APIConfig, AppConfig
from src.utils.logging import setup_logging, get_logger
from src.utils.exceptions import APIKeyMissingError, ResearchAgentError

# Page configuration
st.set_page_config(
    page_title="AI Deep Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.75rem;
        border: none;
        transition: transform 0.2s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
    }
    .paper-card {
        background: #f8f9fa;
        border-left: 4px solid #667eea;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 4px;
    }
    .finding-item {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 0.75rem;
        margin: 0.5rem 0;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize app config and logging
@st.cache_resource
def init_app():
    """Initialize application"""
    app_config = AppConfig()
    setup_logging(app_config)
    return app_config

app_config = init_app()
logger = get_logger(__name__)

# Session state initialization
if "research_history" not in st.session_state:
    st.session_state.research_history = []

def init_agent(api_key: str, provider: str = "openai", model: str = "gpt-4-turbo-preview") -> DeepResearchAgent:
    """Initialize research agent with configuration"""
    api_config = APIConfig()
    
    if provider == "openai":
        api_config.openai_api_key = api_key
        model_config = ModelConfig(provider="openai", model_name=model)
    elif provider == "anthropic":
        api_config.anthropic_api_key = api_key
        model_config = ModelConfig(provider="anthropic", model_name="claude-3-sonnet-20240229")
    else:
        api_config.google_api_key = api_key
        model_config = ModelConfig(provider="google", model_name="gemini-pro")
    
    research_config = ResearchConfig()
    
    agent = DeepResearchAgent(
        model_config=model_config,
        research_config=research_config,
        api_config=api_config
    )
    
    return agent

# Main UI
def main():
    # Header
    st.markdown('<h1 class="main-header">🔬 AI Deep Research Agent</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Production-grade academic research powered by LLMs</p>', unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Provider selection
        provider = st.selectbox(
            "LLM Provider",
            ["openai", "anthropic", "google"],
            help="Select your preferred LLM provider"
        )
        
        # Model selection based on provider
        if provider == "openai":
            model = st.selectbox(
                "Model",
                ["gpt-4-turbo-preview", "gpt-4", "gpt-3.5-turbo"],
                help="OpenAI model to use"
            )
            api_key = st.text_input(
                "OpenAI API Key",
                type="password",
                help="Enter your OpenAI API key"
            )
        elif provider == "anthropic":
            model = "claude-3-sonnet-20240229"
            api_key = st.text_input(
                "Anthropic API Key",
                type="password",
                help="Enter your Anthropic API key"
            )
        else:
            model = "gemini-pro"
            api_key = st.text_input(
                "Google API Key",
                type="password",
                help="Enter your Google API key"
            )
        
        st.divider()
        
        # Research configuration
        st.subheader("Research Settings")
        
        max_papers = st.slider(
            "Max Papers",
            min_value=5,
            max_value=20,
            value=10,
            help="Maximum number of papers to retrieve"
        )
        
        sources = st.multiselect(
            "Data Sources",
            ["arxiv", "pubmed", "web"],
            default=["arxiv", "pubmed"],
            help="Select research sources"
        )
        
        st.divider()
        
        # Info
        st.info("💡 **Tip:** Start with a specific research question for best results!")
        
        if st.button("📚 View Research History"):
            if st.session_state.research_history:
                st.write(f"**{len(st.session_state.research_history)}** past researches")
            else:
                st.write("No research history yet")
    
    # Main content area
    query = st.text_area(
        "🔍 Enter your research question:",
        height=100,
        placeholder="Example: What are the latest developments in transformer architectures for computer vision?",
        help="Be specific for better results"
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        research_button = st.button("🚀 Start Research", use_container_width=True)
    
    # Research execution
    if research_button:
        if not api_key:
            st.error("⚠️ Please provide an API key in the sidebar")
            return
        
        if not query or len(query.strip()) < 5:
            st.error("⚠️ Please enter a valid research question (min 5 characters)")
            return
        
        if not sources:
            st.error("⚠️ Please select at least one data source")
            return
        
        try:
            with st.spinner("🔬 Conducting deep research..."):
                # Initialize agent
                agent = init_agent(api_key, provider, model)
                
                # Update research config
                agent.research_config.max_papers = max_papers
                agent.research_config.sources = sources
                
                # Run research
                result: ResearchResult = asyncio.run(agent.research(query))
                
                # Save to history
                st.session_state.research_history.append({
                    "query": query,
                    "timestamp": result.timestamp,
                    "papers_found": len(result.papers)
                })
                
                # Display results
                st.success("✅ Research completed!")
                
                # Summary section
                st.markdown("### 📝 Research Summary")
                st.markdown(f"<div class='paper-card'>{result.summary}</div>", unsafe_allow_html=True)
                
                # Key findings
                st.markdown("### 💡 Key Findings")
                for i, finding in enumerate(result.key_findings, 1):
                    st.markdown(f"<div class='finding-item'><strong>{i}.</strong> {finding}</div>", unsafe_allow_html=True)
                
                # Papers section
                st.markdown(f"### 📚 Top Papers ({len(result.papers)})")
                
                for i, paper in enumerate(result.papers, 1):
                    with st.expander(f"📄 {i}. {paper.title}"):
                        st.markdown(f"**Authors:** {', '.join(paper.authors[:5])}")
                        st.markdown(f"**Published:** {paper.published.strftime('%Y-%m-%d')}")
                        st.markdown(f"**Source:** {paper.source.upper()}")
                        
                        if paper.abstract:
                            st.markdown("**Abstract:**")
                            st.write(paper.abstract[:500] + "..." if len(paper.abstract) > 500 else paper.abstract)
                        
                        if paper.url:
                            st.markdown(f"[🔗 View Paper]({paper.url})")
                
                # Metadata
                with st.expander("ℹ️ Research Metadata"):
                    st.json(result.metadata)
                
                # Download option
                st.divider()
                
                # Export results
                export_data = {
                    "query": result.query,
                    "summary": result.summary,
                    "findings": result.key_findings,
                    "papers": [
                        {
                            "title": p.title,
                            "authors": p.authors,
                            "url": p.url,
                            "source": p.source
                        }
                        for p in result.papers
                    ],
                    "timestamp": result.timestamp.isoformat()
                }
                
                import json
                st.download_button(
                    label="📥 Download Results (JSON)",
                    data=json.dumps(export_data, indent=2),
                    file_name=f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
                
        except APIKeyMissingError as e:
            st.error(f"⚠️ API Key Error: {str(e)}")
            logger.error(f"API key error: {e}")
        
        except ResearchAgentError as e:
            st.error(f"⚠️ Research Error: {str(e)}")
            logger.error(f"Research error: {e}")
        
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")
            logger.error(f"Unexpected error: {e}", exc_info=True)
    
    # Footer
    st.divider()
    st.markdown(
        """
        <div style='text-align: center; color: #666; padding: 1rem;'>
            <p>Built with ❤️ using Streamlit, LangChain, and cutting-edge LLMs</p>
            <p>🔬 AI Deep Research Agent v1.0.0 | Production-Grade Research Tool</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
