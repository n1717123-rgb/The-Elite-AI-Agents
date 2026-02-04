"""
Deep Research Agent - Core Implementation
Orchestrates LLM with research tools for comprehensive research
"""
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import json

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage

from src.models.config import ModelConfig, ResearchConfig, APIConfig
from src.tools.research_tools import ArxivTool, PubMedTool, WebSearchTool, ResearchPaper
from src.utils.logging import get_logger
from src.utils.exceptions import APIKeyMissingError, ModelError, InvalidInputError

logger = get_logger(__name__)


@dataclass
class ResearchResult:
    """Research result data model"""
    query: str
    summary: str
    papers: List[ResearchPaper]
    key_findings: List[str]
    citations: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


class DeepResearchAgent:
    """
    Deep Research Agent with multi-source integration
    Combines academic papers, web search, and LLM analysis
    """
    
    def __init__(
        self,
        model_config: ModelConfig,
        research_config: ResearchConfig,
        api_config: APIConfig
    ):
        """
        Initialize research agent
        
        Args:
            model_config: LLM model configuration
            research_config: Research parameters
            api_config: API keys
        """
        self.model_config = model_config
        self.research_config = research_config
        self.api_config = api_config
        
        # Initialize LLM
        self.llm = self._init_llm()
        
        # Initialize research tools
        self.arxiv_tool = ArxivTool(max_results=research_config.max_papers)
        self.pubmed_tool = PubMedTool(max_results=research_config.max_papers)
        self.web_tool = WebSearchTool(max_results=research_config.max_papers)
        
        logger.info(f"DeepResearchAgent initialized | model={model_config.model_name} | sources={research_config.sources}")
    
    def _init_llm(self):
        """Initialize LLM based on provider"""
        try:
            if self.model_config.provider == "openai":
                if not self.api_config.openai_api_key:
                    raise APIKeyMissingError("OpenAI API key is required")
                return ChatOpenAI(
                    model=self.model_config.model_name,
                    temperature=self.model_config.temperature,
                    max_tokens=self.model_config.max_tokens,
                    api_key=self.api_config.openai_api_key
                )
            
            elif self.model_config.provider == "anthropic":
                if not self.api_config.anthropic_api_key:
                    raise APIKeyMissingError("Anthropic API key is required")
                return ChatAnthropic(
                    model=self.model_config.model_name,
                    temperature=self.model_config.temperature,
                    max_tokens=self.model_config.max_tokens,
                    api_key=self.api_config.anthropic_api_key
                )
            
            elif self.model_config.provider == "google":
                if not self.api_config.google_api_key:
                    raise APIKeyMissingError("Google API key is required")
                return ChatGoogleGenerativeAI(
                    model=self.model_config.model_name,
                    temperature=self.model_config.temperature,
                    max_output_tokens=self.model_config.max_tokens,
                    google_api_key=self.api_config.google_api_key
                )
            
            else:
                raise ValueError(f"Unsupported provider: {self.model_config.provider}")
                
        except Exception as e:
            logger.error(f"LLM initialization failed | error={str(e)}")
            raise ModelError(f"Failed to initialize LLM: {str(e)}")
    
    async def research(self, query: str) -> ResearchResult:
        """
        Conduct deep research on a topic
        
        Args:
            query: Research question/topic
            
        Returns:
            Comprehensive research results
        """
        if not query or len(query.strip()) < 5:
            raise InvalidInputError("Query must be at least 5 characters")
        
        logger.info(f"Starting research | query='{query}'")
        
        try:
            # Step 1: Gather papers from multiple sources
            all_papers = []
            
            if "arxiv" in self.research_config.sources:
                logger.info("Searching Arxiv...")
                arxiv_papers = self.arxiv_tool.search(query)
                all_papers.extend(arxiv_papers)
            
            if "pubmed" in self.research_config.sources:
                logger.info("Searching PubMed...")
                pubmed_papers = self.pubmed_tool.search(query)
                all_papers.extend(pubmed_papers)
            
            if "web" in self.research_config.sources or "google_scholar" in self.research_config.sources:
                logger.info("Searching web...")
                # Web search provides different structure, convert to papers
                web_results = self.web_tool.search(query)
            
            logger.info(f"Collected {len(all_papers)} papers")
            
            # Step 2: Analyze papers with LLM
            logger.info("Analyzing papers with LLM...")
            analysis = await self._analyze_papers(query, all_papers)
            
            # Step 3: Extract key findings
            key_findings = await self._extract_key_findings(query, all_papers, analysis)
            
            # Step 4: Generate final summary
            summary = await self._generate_summary(query, all_papers, key_findings)
            
            result = ResearchResult(
                query=query,
                summary=summary,
                papers=all_papers[:10],  # Top 10 papers
                key_findings=key_findings,
                metadata={
                    "total_papers": len(all_papers),
                    "sources": self.research_config.sources,
                    "model": self.model_config.model_name
                }
            )
            
            logger.info(f"Research completed | papers={len(all_papers)} | findings={len(key_findings)}")
            return result
            
        except Exception as e:
            logger.error(f"Research failed | error={str(e)}")
            raise
    
    async def _analyze_papers(self, query: str, papers: List[ResearchPaper]) -> str:
        """Analyze collected papers with LLM"""
        if not papers:
            return "No papers found for analysis."
        
        # Prepare paper context
        papers_context = "\n\n".join([
            f"**Paper {i+1}:**\n"
            f"Title: {paper.title}\n"
            f"Authors: {', '.join(paper.authors[:3])}\n"
            f"Abstract: {paper.abstract[:500]}...\n"
            f"Source: {paper.source}"
            for i, paper in enumerate(papers[:5])  # Top 5 papers
        ])
        
        system_prompt = """You are an expert research analyst. Your task is to analyze academic papers 
        and extract meaningful insights. Focus on methodology, key findings, and implications."""
        
        user_prompt = f"""Research Query: {query}

Papers to analyze:
{papers_context}

Please provide a comprehensive analysis covering:
1. Main themes and patterns across papers
2. Methodological approaches used
3. Key consensus and disagreements
4. Research gaps identified
"""
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        try:
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            logger.error(f"LLM analysis failed | error={str(e)}")
            return f"Analysis failed: {str(e)}"
    
    async def _extract_key_findings(self, query: str, papers: List[ResearchPaper], analysis: str) -> List[str]:
        """Extract key findings from analysis"""
        prompt = f"""Based on this research analysis, extract 5-7 key findings as bullet points:

Analysis:
{analysis}

Provide only the key findings, one per line, as concise statements."""
        
        try:
            messages = [HumanMessage(content=prompt)]
            response = self.llm.invoke(messages)
            
            # Parse findings
            findings = [
                line.strip().lstrip("-•").strip()
                for line in response.content.split("\n")
                if line.strip() and len(line.strip()) > 10
            ]
            
            return findings[:7]  # Max 7 findings
            
        except Exception as e:
            logger.error(f"Key findings extraction failed | error={str(e)}")
            return ["Failed to extract key findings"]
    
    async def _generate_summary(self, query: str, papers: List[ResearchPaper], findings: List[str]) -> str:
        """Generate final research summary"""
        findings_text = "\n".join([f"- {finding}" for finding in findings])
        
        prompt = f"""Create a comprehensive research summary for the query: "{query}"

Key Findings:
{findings_text}

Number of papers analyzed: {len(papers)}

Provide a well-structured summary (2-3 paragraphs) that:
1. Answers the research query
2. Synthesizes the key findings
3. Provides actionable insights
4. Mentions limitations or areas for further research
"""
        
        try:
            messages = [HumanMessage(content=prompt)]
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            logger.error(f"Summary generation failed | error={str(e)}")
            return f"Summary generation failed: {str(e)}"
