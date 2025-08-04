"""
LLM synthesis functionality for Inquisitor CLI.
Handles generating AI responses with citations from search results.
"""

import os
from typing import List, Optional
from openai import OpenAI
from dotenv import load_dotenv
from search import SearchResult

load_dotenv()


class LLMSynthesizer:
    """Handles LLM-powered synthesis of search results into cited answers."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = model
        
        if not (api_key or os.getenv("OPENAI_API_KEY")):
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
    
    def synthesize_answer(self, query: str, search_results: List[SearchResult]) -> str:
        """
        Generate a synthesized answer from search results with inline citations.
        
        Args:
            query: Original user query
            search_results: List of SearchResult objects
            
        Returns:
            Synthesized answer with inline citations
        """
        if not search_results:
            return "No search results available to synthesize an answer."
        
        # Format search results for the prompt
        results_text = self._format_results_for_prompt(search_results)
        
        # Create the synthesis prompt
        prompt = self._create_synthesis_prompt(query, results_text)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=800
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise Exception(f"LLM synthesis failed: {e}")
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the LLM."""
        return """You are an expert research assistant that synthesizes information from web search results into clear, accurate answers with proper citations.

Your task is to:
1. Analyze the provided search results
2. Create a comprehensive, well-structured answer to the user's question
3. Include inline citations using square brackets with numbers [1], [2], etc.
4. Only cite information that directly comes from the search results
5. If information conflicts between sources, acknowledge this
6. Be concise but thorough
7. Use a conversational, informative tone

IMPORTANT: Always include citations for factual claims. Use the exact numbering from the search results provided."""
    
    def _create_synthesis_prompt(self, query: str, results_text: str) -> str:
        """Create the synthesis prompt combining query and results."""
        return f"""User Question: {query}

{results_text}

Please provide a comprehensive answer to the user's question based on the search results above. Include inline citations using square brackets [1], [2], etc. that correspond to the numbered search results. Only include information that can be found in the provided search results."""
    
    def _format_results_for_prompt(self, search_results: List[SearchResult]) -> str:
        """Format search results for the LLM prompt."""
        formatted = "Search Results:\n\n"
        for i, result in enumerate(search_results, 1):
            formatted += f"[{i}] Title: {result.title}\n"
            formatted += f"URL: {result.url}\n"
            formatted += f"Content: {result.snippet}\n\n"
        
        return formatted
