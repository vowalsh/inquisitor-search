#!/usr/bin/env python3
"""
Inquisitor - Lightweight Python CLI for Perplexity-style answers.
Combines live web search with LLM synthesis for cited, real-time answers.
"""

import argparse
import sys
import os
from typing import Optional
from datetime import datetime

from search import WebSearcher
from llm import LLMSynthesizer
from formatting import OutputFormatter
from cache import QACache, CachedQA


class InquisitorCLI:
    """Main CLI application for Inquisitor."""
    
    def __init__(self, use_colors: bool = True, num_results: int = 8, use_cache: bool = True, streaming: bool = True):
        self.formatter = OutputFormatter(use_colors=use_colors)
        self.num_results = num_results
        self.use_cache = use_cache
        self.streaming = streaming
        
        try:
            self.searcher = WebSearcher()
            self.synthesizer = LLMSynthesizer()
            self.cache = QACache()
        except ValueError as e:
            self.formatter.print_error(str(e))
            sys.exit(1)
    
    def process_query(self, query: str, force_refresh: bool = False) -> bool:
        """
        Process a single query through the full pipeline.
        
        Args:
            query: User's search query
            force_refresh: If True, skip cache and force fresh search
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Step 1: Check cache (unless force refresh is requested)
            if self.use_cache and not force_refresh:
                cached_answer = self.cache.find_exact_match(query)
                if cached_answer:
                    self.formatter.print_success("Found exact match in cache")
                    print()  # Add spacing
                    self.formatter.print_response(cached_answer.answer, cached_answer.search_results)
                    return True
                
                # Check for similar questions
                similar_questions = self.cache.find_similar_questions(query, min_similarity=0.8, max_results=1)
                if similar_questions:
                    qa, similarity = similar_questions[0]  # Get the best match
                    self.formatter.print_success(f"Found similar question in cache (similarity: {similarity:.1%})")
                    print(f"Original question: {qa.question}")
                    print()  # Add spacing
                    self.formatter.print_response(qa.answer, qa.search_results)
                    return True
            
            # Step 2: Search
            self.formatter.print_status("Searching the web")
            search_results = self.searcher.search(query, num_results=self.num_results)
            
            if not search_results:
                self.formatter.print_error("No search results found")
                return False
            
            self.formatter.print_success(f"Found {len(search_results)} results")
            
            # Step 3: Synthesize
            if self.streaming:
                self.formatter.print_status("Generating answer")
                print()  # Add spacing before streaming output
                answer = self.synthesizer.synthesize_answer(query, search_results, streaming=True)
                print()  # Add spacing after streaming output
            else:
                self.formatter.print_status("Synthesizing answer")
                answer = self.synthesizer.synthesize_answer(query, search_results, streaming=False)
                self.formatter.print_success("Answer generated")
                print()  # Add spacing
                # Display the answer
                self.formatter.print_response(answer, search_results)
            
            # Step 4: Cache the result
            if self.use_cache:
                self.cache.store_qa(query, answer, search_results)
            
            # Step 5: Display citations (for streaming mode, we already printed the answer)
            if self.streaming:
                print()  # Add spacing before citations
                self.formatter.print_citations(search_results)
            
            return True
            
        except Exception as e:
            self.formatter.print_error(f"Failed to process query: {e}")
            return False
    
    def interactive_mode(self):
        """Run Inquisitor in interactive mode."""
        print(self.formatter.format_success("Welcome to Inquisitor! Ask me anything."))
        print("Type 'quit', 'exit', or press Ctrl+C to exit.")
        if self.use_cache:
            print("Cache commands: '/cache list', '/cache search <term>', '/cache stats', '/cache clear'")
        print()
        
        while True:
            try:
                query = input("❓ Your question: ").strip()
                
                if not query:
                    continue
                
                if query.lower() in ['quit', 'exit', 'q']:
                    print(self.formatter.format_success("Goodbye!"))
                    break
                
                # Handle cache commands in interactive mode
                if query.startswith('/cache'):
                    if not self.use_cache:
                        self.formatter.print_error("Cache is disabled")
                        continue
                    
                    parts = query.split(' ', 2)
                    if len(parts) < 2:
                        print(self.formatter.format_info("Cache commands: list, search <term>, stats, clear"))
                        continue
                    
                    command = parts[1].lower()
                    
                    if command == 'list':
                        self.list_cache_command()
                    elif command == 'search' and len(parts) >= 3:
                        self.search_cache_command(parts[2])
                    elif command == 'search':
                        print(self.formatter.format_info("Usage: /cache search <search term>"))
                    elif command == 'stats':
                        self.cache_stats_command()
                    elif command == 'clear':
                        self.clear_cache_command()
                    else:
                        print(self.formatter.format_info("Cache commands: list, search <term>, stats, clear"))
                    
                    print()
                    continue
                
                print()  # Add spacing before processing
                success = self.process_query(query)
                
                if success:
                    print("\n" + "─" * 50 + "\n")  # Separator between queries
                
            except KeyboardInterrupt:
                print(f"\n{self.formatter.format_success('Goodbye!')}")
                break
            except EOFError:
                print(f"\n{self.formatter.format_success('Goodbye!')}")
                break

    def list_cache_command(self, count: int = 10):
        """List recent cached Q&As."""
        if not self.use_cache:
            self.formatter.print_error("Cache is disabled")
            return
        
        recent_entries = self.cache.get_recent_entries(count)
        
        if not recent_entries:
            print(self.formatter.format_info("No cached entries found"))
            return
        
        print(self.formatter.format_success(f"Recent {len(recent_entries)} cached Q&As:"))
        print()
        
        for i, qa in enumerate(recent_entries, 1):
            cache_time = datetime.fromisoformat(qa.timestamp)
            print(f"{self.formatter.format_info(f'{i}.')} {qa.question}")
            print(f"   {cache_time.strftime('%Y-%m-%d %H:%M')}")
            print(f"   {qa.answer[:100]}{'...' if len(qa.answer) > 100 else ''}")
            print()

    def search_cache_command(self, search_term: str):
        """Search through cached Q&As."""
        if not self.use_cache:
            self.formatter.print_error("Cache is disabled")
            return
        
        matches = self.cache.find_similar_questions(search_term, min_similarity=0.8, max_results=10)
        
        if not matches:
            print(self.formatter.format_info(f"No cached entries found matching '{search_term}'"))
            return
        
        print(self.formatter.format_success(f"Found {len(matches)} cached entries matching '{search_term}':"))
        print()
        
        for i, (qa, similarity) in enumerate(matches, 1):
            cache_time = datetime.fromisoformat(qa.timestamp)
            print(f"{self.formatter.format_info(f'{i}.')} {qa.question} (similarity: {similarity:.1%})")
            print(f"   {cache_time.strftime('%Y-%m-%d %H:%M')}")
            print(f"   {qa.answer[:100]}{'...' if len(qa.answer) > 100 else ''}")
            print()

    def cache_stats_command(self):
        """Show cache statistics."""
        if not self.use_cache:
            self.formatter.print_error("Cache is disabled")
            return
        
        stats = self.cache.get_cache_stats()
        
        print(self.formatter.format_success("Cache Statistics:"))
        print(f"Total entries: {stats['total_entries']}")
        print(f"Cache size: {stats['cache_size_mb']} MB")
        
        if stats['newest_entry']:
            newest = datetime.fromisoformat(stats['newest_entry'])
            print(f"Newest entry: {newest.strftime('%Y-%m-%d %H:%M')}")
        
        if stats['oldest_entry']:
            oldest = datetime.fromisoformat(stats['oldest_entry'])
            print(f"Oldest entry: {oldest.strftime('%Y-%m-%d %H:%M')}")

    def clear_cache_command(self):
        """Clear all cached entries."""
        if not self.use_cache:
            self.formatter.print_error("Cache is disabled")
            return
        
        self.cache.clear_cache()
        print(self.formatter.format_success("Cache cleared successfully"))


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Inquisitor - Get real-time, cited answers from the web",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  inquisitor                              # Interactive mode
  inquisitor "What is the capital of France?"  # Single query
  inquisitor --no-color "Python 3.12 features"  # No color output
  inquisitor --cache-search "python"     # Search cached Q&As
  inquisitor --cache-list                 # List recent cached entries
  inquisitor --cache-stats                # Show cache statistics
  inquisitor --cache-clear                # Clear cache
        """
    )
    
    parser.add_argument(
        "query",
        nargs="?",
        help="Search query (if not provided, enters interactive mode)"
    )
    
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output"
    )
    
    parser.add_argument(
        "--results",
        type=int,
        default=8,
        help="Number of search results to fetch (default: 8)"
    )
    
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Disable caching"
    )
    
    parser.add_argument(
        "--force-refresh",
        action="store_true",
        help="Force fresh search, skip cache"
    )
    
    parser.add_argument(
        "--cache-search",
        type=str,
        help="Search through cached Q&As"
    )
    
    parser.add_argument(
        "--cache-list",
        action="store_true",
        help="List recent cached Q&As"
    )
    
    parser.add_argument(
        "--cache-stats",
        action="store_true",
        help="Show cache statistics"
    )
    
    parser.add_argument(
        "--cache-clear",
        action="store_true",
        help="Clear all cached entries"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="Inquisitor 1.0.0"
    )
    
    parser.add_argument(
        "--no-streaming",
        action="store_true",
        help="Disable streaming output (show complete answer at once)"
    )
    
    args = parser.parse_args()
    
    # Initialize CLI
    use_colors = not args.no_color
    use_cache = not args.no_cache
    streaming = not args.no_streaming  # Default to True, disable with --no-streaming
    cli = InquisitorCLI(use_colors=use_colors, num_results=args.results, use_cache=use_cache, streaming=streaming)
    
    # Handle cache commands
    if args.cache_search:
        cli.search_cache_command(args.cache_search)
        return
    
    if args.cache_list:
        cli.list_cache_command()
        return
    
    if args.cache_stats:
        cli.cache_stats_command()
        return
    
    if args.cache_clear:
        cli.clear_cache_command()
        return
    
    if args.query:
        # Single query mode
        success = cli.process_query(args.query, force_refresh=args.force_refresh)
        sys.exit(0 if success else 1)
    else:
        # Interactive mode
        cli.interactive_mode()


if __name__ == "__main__":
    main()
