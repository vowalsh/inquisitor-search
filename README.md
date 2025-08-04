# Inquisitor

**Lightweight Python CLI for Perplexity-style answers**

Inquisitor combines live web search with LLM synthesis to deliver real-time, cited answers directly in your terminal. Get comprehensive, up-to-date information with transparent source attribution.

## Features

- **Live Web Search** - Real-time results using SerpAPI
- **LLM Synthesis** - AI-powered answer generation with OpenAI
- **Streaming Output** - Real-time answer generation like ChatGPT and Perplexity (enabled by default)
- **Inline Citations** - Transparent source attribution with [1], [2] references
- **Beautiful Output** - Colored terminal display with clear formatting
- **Visual Data Charts** - Automatic generation of terminal charts and graphs for numeric/statistical topics
- **Fast & Lightweight** - Minimal dependencies, maximum performance
- **Interactive Mode** - Continuous Q&A sessions
- **Smart Caching** - Cache answers for instant retrieval and offline access
- **Cache Search** - Find previous Q&As with powerful search functionality
- **Flexible** - Single queries or interactive sessions

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd inquisitor-search
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install the package (for CLI command):**
   ```bash
   pip install -e .
   ```
   This installs the `inquisitor` command globally so you can run it from anywhere.

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

5. **Get API Keys:**
   - **SerpAPI**: Sign up at [serpapi.com](https://serpapi.com/) for web search
   - **OpenAI**: Get your key at [platform.openai.com](https://platform.openai.com/api-keys)

## Usage

### Interactive Mode
```bash
inquisitor
```

### Single Query
```bash
inquisitor "What are the latest developments in AI?"
```

### Cache Commands
```bash
# Search cached Q&As
inquisitor --cache-search "python"

# List recent cached entries
inquisitor --cache-list

# Show cache statistics
inquisitor --cache-stats

# Clear cache
inquisitor --cache-clear

# Force fresh search (skip cache)
inquisitor --force-refresh "What is Python?"

# Disable caching
inquisitor --no-cache "Your question"
```

### Interactive Cache Commands
In interactive mode, use these cache commands:
```
❓ Your question: /cache list          # List recent entries
❓ Your question: /cache search python # Search for "python"
❓ Your question: /cache stats         # Show statistics
❓ Your question: /cache clear         # Clear cache
```

### Options
```bash
inquisitor --help
inquisitor --no-color "Python 3.12 features"
inquisitor --results 5 "Climate change solutions"
inquisitor --no-streaming "Explain machine learning"
inquisitor --no-cache "Disable caching for this query"
```

## Caching System

Inquisitor automatically caches Q&A pairs for:
- **Instant retrieval** of repeated questions
- **Offline access** to previous answers
- **Similar question detection** with smart matching
- **Search functionality** across cached content

Cache features:
- Stores questions, answers, and source links
- Automatic expiration (30 days by default)
- Size limits (1000 entries by default)
- Similarity matching for related questions
- Full-text search across Q&As

Cache location: `~/.inquisitor_cache/qa_cache.json`

## Example Output

```
==================================================
                Inquisitor Answer                
==================================================

Python 3.12 introduces several significant improvements including enhanced error messages [1], performance optimizations with up to 15% speed increases [2], and new syntax features like f-string debugging [3]. The release also includes improved type hints and better memory management [4].

Sources:

[1] Python 3.12 Release Notes - Official Documentation
    https://docs.python.org/3.12/whatsnew/3.12.html
    Comprehensive overview of new features and improvements...

[2] Python Performance Benchmarks
    https://speed.python.org/
    Detailed performance comparisons showing speed improvements...
```

## Visual Data Charts

Inquisitor automatically detects numeric and statistical content in answers and generates beautiful terminal charts and visualizations using the Rich library.

### Automatic Chart Generation

When your query returns data with:
- **Percentages** (e.g., "market share: 45%")
- **Currency values** (e.g., "revenue: $2.5 billion")
- **Statistical data** (e.g., "population: 1,400,000")
- **Comparative numbers** (e.g., growth rates, rankings)

Inquisitor will automatically generate:
- **Horizontal bar charts** for comparing multiple data points
- **Summary tables** with formatted values and data types
- **Visual panels** with color-coded information

### Example Queries That Generate Charts

```bash
# Market data
inquisitor "What are the market shares of major smartphone companies?"

# Financial information
inquisitor "Compare the GDP of G7 countries"

# Statistical comparisons
inquisitor "What are the unemployment rates in European countries?"

# Performance metrics
inquisitor "Show me the top programming languages by popularity percentage"
```

### Chart Features

- **Smart detection** - Automatically identifies chart-worthy content
- **Multiple formats** - Bar charts and comparison tables
- **Color coding** - Different colors for different data types
- **Responsive design** - Adapts to terminal width
- **Clean presentation** - Integrated seamlessly with answer text

## Architecture

- **`inquisitor.py`** - Main CLI interface and orchestration
- **`search.py`** - Web search functionality using SerpAPI
- **`llm.py`** - LLM synthesis with OpenAI integration
- **`formatting.py`** - Output formatting and terminal display
- **`cache.py`** - Q&A caching and retrieval system
- **`charts.py`** - Terminal chart and visualization generation

## Configuration

Environment variables in `.env`:
- `SERPAPI_KEY` - Your SerpAPI key for web search
- `OPENAI_API_KEY` - Your OpenAI API key for synthesis

## Requirements

- Python 3.7+
- Internet connection
- SerpAPI account (free tier available)
- OpenAI API account

## License

MIT License - see [LICENSE](LICENSE) file for details.
