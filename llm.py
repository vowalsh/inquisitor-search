"""
LLM synthesis functionality for Inquisitor CLI.
Handles generating AI responses with citations from search results.
"""

import os
import sys
from typing import List, Optional, Generator
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
    
    def synthesize_answer(self, query: str, search_results: List[SearchResult], streaming: bool = False) -> str:
        """
        Generate a synthesized answer from search results with inline citations.
        
        Args:
            query: Original user query
            search_results: List of SearchResult objects
            streaming: Whether to use streaming output
            
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
            if streaming:
                return self.print_streaming_answer(query, search_results)
            else:
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
    
    def synthesize_answer_streaming(self, query: str, search_results: List[SearchResult]) -> Generator[str, None, None]:
        """
        Generate a synthesized answer from search results with streaming output.
        
        Args:
            query: Original user query
            search_results: List of SearchResult objects
            
        Yields:
            Chunks of the synthesized answer as they are generated
        """
        if not search_results:
            yield "No search results available to synthesize an answer."
            return
        
        # Format search results for the prompt
        results_text = self._format_results_for_prompt(search_results)
        
        # Create the synthesis prompt
        prompt = self._create_synthesis_prompt(query, results_text)
        
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=800,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            yield f"\nError: LLM synthesis failed: {e}"
    
    def print_streaming_answer(self, query: str, search_results: List[SearchResult], formatter=None) -> str:
        """
        Print a synthesized answer with streaming output and return the complete answer.
        
        Args:
            query: Original user query
            search_results: List of SearchResult objects
            formatter: OutputFormatter instance for styling
            
        Returns:
            Complete synthesized answer
        """
        complete_answer = ""
        
        # Print the header first
        if formatter:
            print(formatter._format_header("Inquisitor Answer"))
            print()
        else:
            print("=" * 50)
            print("Inquisitor Answer".center(50))
            print("=" * 50)
            print()
        
        try:
            sentence_buffer = ""
            word_count = 0
            
            for chunk in self.synthesize_answer_streaming(query, search_results):
                complete_answer += chunk
                sentence_buffer += chunk
                
                # Count words for better formatting
                if ' ' in chunk:
                    word_count += chunk.count(' ')
                
                # Apply formatting to each chunk if formatter is available
                if formatter:
                    # Apply citation highlighting to the chunk
                    import re
                    if formatter.use_colors:
                        from colorama import Fore, Style
                        citation_pattern = r'\[(\d+)\]'
                        formatted_chunk = re.sub(
                            citation_pattern, 
                            f'{Fore.BLUE}[\\1]{Style.RESET_ALL}', 
                            chunk
                        )
                        print(formatted_chunk, end='', flush=True)
                    else:
                        print(chunk, end='', flush=True)
                else:
                    print(chunk, end='', flush=True)
                
                # Add intelligent paragraph breaks for better readability
                if '\n\n' in sentence_buffer:
                    # Natural paragraph break detected
                    sentence_buffer = ""
                    word_count = 0
                    print()  # Add extra spacing for paragraph breaks
                elif '. ' in chunk and word_count > 20:
                    # Add subtle spacing after sentences in long paragraphs
                    if sentence_buffer.count('. ') >= 1 and len(sentence_buffer) > 150:
                        # Reset counters but don't add line break yet
                        pass
                elif '\n' in chunk and word_count > 15:
                    # Natural line break with sufficient content
                    word_count = 0
                
            print()  # Add newline at the end
            print()  # Extra spacing before sources
            return complete_answer.strip()
            
        except KeyboardInterrupt:
            print("\n\nStreaming interrupted by user.")
            return complete_answer.strip()
        except Exception as e:
            error_msg = f"\nError during streaming: {e}"
            print(error_msg)
            return complete_answer + error_msg
    
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
