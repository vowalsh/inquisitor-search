#!/usr/bin/env python3
"""
Inquisitor - Lightweight Python CLI for Perplexity-style answers.
Combines live web search with LLM synthesis for cited, real-time answers.
"""

import argparse
import sys
import os
from typing import Optional

from search import WebSearcher
from llm import LLMSynthesizer
from formatting import OutputFormatter


class InquisitorCLI:
    """Main CLI application for Inquisitor."""
    
    def __init__(self, use_colors: bool = True, num_results: int = 8):
        self.formatter = OutputFormatter(use_colors=use_colors)
        self.num_results = num_results
        
        try:
            self.searcher = WebSearcher()
            self.synthesizer = LLMSynthesizer()
        except ValueError as e:
            self.formatter.print_error(str(e))
            sys.exit(1)
    
    def process_query(self, query: str) -> bool:
        """
        Process a single query through the full pipeline.
        
        Args:
            query: User's search query
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Step 1: Search
            self.formatter.print_status("Searching the web")
            search_results = self.searcher.search(query, self.num_results)
            
            if not search_results:
                self.formatter.print_error("No search results found")
                return False
            
            self.formatter.print_success(f"Found {len(search_results)} results")
            
            # Step 2: Synthesize
            self.formatter.print_status("Synthesizing answer")
            answer = self.synthesizer.synthesize_answer(query, search_results)
            
            self.formatter.print_success("Answer generated")
            print()  # Add spacing
            
            # Step 3: Display
            self.formatter.print_response(answer, search_results)
            
            return True
            
        except Exception as e:
            self.formatter.print_error(f"Failed to process query: {e}")
            return False
    
    def interactive_mode(self):
        """Run Inquisitor in interactive mode."""
        print(self.formatter.format_success("Welcome to Inquisitor! Ask me anything."))
        print("Type 'quit', 'exit', or press Ctrl+C to exit.\n")
        
        while True:
            try:
                query = input("❓ Your question: ").strip()
                
                if not query:
                    continue
                
                if query.lower() in ['quit', 'exit', 'q']:
                    print(self.formatter.format_success("Goodbye!"))
                    break
                
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


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Inquisitor - Get real-time, cited answers from the web",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  inquisitor.py                           # Interactive mode
  inquisitor.py "What is the capital of France?"  # Single query
  inquisitor.py --no-color "Python 3.12 features"  # No color output
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
        "--version",
        action="version",
        version="Inquisitor 1.0.0"
    )
    
    args = parser.parse_args()
    
    # Initialize CLI
    use_colors = not args.no_color
    cli = InquisitorCLI(use_colors=use_colors, num_results=args.results)
    
    if args.query:
        # Single query mode
        success = cli.process_query(args.query)
        sys.exit(0 if success else 1)
    else:
        # Interactive mode
        cli.interactive_mode()


if __name__ == "__main__":
    main()
