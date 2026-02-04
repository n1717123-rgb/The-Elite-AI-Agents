"""
Research tools for accessing academic databases
Includes Arxiv, PubMed, Google Scholar integration
"""
import arxiv
import requests
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
from tenacity import retry, stop_after_attempt, wait_exponential
from src.utils.logging import get_logger
from src.utils.exceptions import ResearchSourceError

logger = get_logger(__name__)


@dataclass
class ResearchPaper:
    """Research paper data model"""
    title: str
    authors: List[str]
    abstract: str
    published: datetime
    url: str
    source: str
    citations: Optional[int] = None
    doi: Optional[str] = None
    pdf_url: Optional[str] = None


class ArxivTool:
    """Arxiv research paper search"""
    
    def __init__(self, max_results: int = 10):
        self.max_results = max_results
        logger.info(f"ArxivTool initialized | max_results={max_results}")
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def search(self, query: str) -> List[ResearchPaper]:
        """
        Search Arxiv for papers
        
        Args:
            query: Search query
            
        Returns:
            List of research papers
        """
        try:
            logger.info(f"Searching Arxiv | query='{query}'")
            
            search = arxiv.Search(
                query=query,
                max_results=self.max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            papers = []
            for result in search.results():
                paper = ResearchPaper(
                    title=result.title,
                    authors=[author.name for author in result.authors],
                    abstract=result.summary,
                    published=result.published,
                    url=result.entry_id,
                    source="arxiv",
                    doi=result.doi,
                    pdf_url=result.pdf_url
                )
                papers.append(paper)
            
            logger.info(f"Arxiv search completed | found={len(papers)} papers")
            return papers
            
        except Exception as e:
            logger.error(f"Arxiv search failed | error={str(e)}")
            raise ResearchSourceError(f"Arxiv search failed: {str(e)}")


class PubMedTool:
    """PubMed/Medline research paper search"""
    
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    
    def __init__(self, max_results: int = 10):
        self.max_results = max_results
        logger.info(f"PubMedTool initialized | max_results={max_results}")
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def search(self, query: str) -> List[ResearchPaper]:
        """
        Search PubMed for papers
        
        Args:
            query: Search query
            
        Returns:
            List of research papers
        """
        try:
            logger.info(f"Searching PubMed | query='{query}'")
            
            # Search PubMed IDs
            search_url = f"{self.BASE_URL}esearch.fcgi"
            search_params = {
                "db": "pubmed",
                "term": query,
                "retmax": self.max_results,
                "retmode": "json"
            }
            
            response = requests.get(search_url, params=search_params, timeout=10)
            response.raise_for_status()
            
            id_list = response.json().get("esearchresult", {}).get("idlist", [])
            
            if not id_list:
                logger.warning("PubMed search returned no results")
                return []
            
            # Fetch paper details
            fetch_url = f"{self.BASE_URL}esummary.fcgi"
            fetch_params = {
                "db": "pubmed",
                "id": ",".join(id_list),
                "retmode": "json"
            }
            
            response = requests.get(fetch_url, params=fetch_params, timeout=10)
            response.raise_for_status()
            
            results = response.json().get("result", {})
            
            papers = []
            for pmid in id_list:
                if pmid in results:
                    data = results[pmid]
                    paper = ResearchPaper(
                        title=data.get("title", ""),
                        authors=[author.get("name", "") for author in data.get("authors", [])],
                        abstract="",  # Would need separate fetch for abstract
                        published=datetime.strptime(data.get("pubdate", "2024"), "%Y") if data.get("pubdate") else datetime.now(),
                        url=f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                        source="pubmed",
                        doi=data.get("elocationid", "").replace("doi: ", "")
                    )
                    papers.append(paper)
            
            logger.info(f"PubMed search completed | found={len(papers)} papers")
            return papers
            
        except Exception as e:
            logger.error(f"PubMed search failed | error={str(e)}")
            raise ResearchSourceError(f"PubMed search failed: {str(e)}")


class WebSearchTool:
    """Web search using DuckDuckGo (free, no API key)"""
    
    def __init__(self, max_results: int = 10):
        self.max_results = max_results
        logger.info(f"WebSearchTool initialized | max_results={max_results}")
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def search(self, query: str) -> List[Dict[str, str]]:
        """
        Search the web for general information
        
        Args:
            query: Search query
            
        Returns:
            List of search results with title, url, snippet
        """
        try:
            logger.info(f"Searching web | query='{query}'")
            
            # Using DuckDuckGo's instant answer API (simplified)
            url = "https://api.duckduckgo.com/"
            params = {
                "q": query,
                "format": "json",
                "no_html": 1
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            results = []
            
            # Abstract/Summary
            if data.get("Abstract"):
                results.append({
                    "title": data.get("Heading", ""),
                    "url": data.get("AbstractURL", ""),
                    "snippet": data.get("Abstract", "")
                })
            
            # Related topics
            for topic in data.get("RelatedTopics", [])[:self.max_results]:
                if "Text" in topic:
                    results.append({
                        "title": topic.get("Text", "")[:100],
                        "url": topic.get("FirstURL", ""),
                        "snippet": topic.get("Text", "")
                    })
            
            logger.info(f"Web search completed | found={len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"Web search failed | error={str(e)}")
            raise ResearchSourceError(f"Web search failed: {str(e)}")
