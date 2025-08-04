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
- **Smart Caching** - Intelligent Q&A caching with similarity matching for instant retrieval
- **Cache Search** - Find previous Q&As with powerful search functionality
- **Random Questions** - Generate and answer random interesting questions for discovery
- **Interactive Mode** - Continuous Q&A sessions with cache commands
- **Verbose Mode** - Debug output for troubleshooting and development
- **Fast & Lightweight** - Minimal dependencies, maximum performance
- **Flexible** - Single queries, interactive sessions, or batch operations

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

# Disable caching for this query
inquisitor --no-cache "Your question"

# Enable cache retrieval (check for similar questions)
inquisitor --use-cache "Your question"
```

### Interactive Cache Commands
In interactive mode, use these cache commands:
```
❓ Your question: /cache list          # List recent entries
❓ Your question: /cache search python # Search for "python"
❓ Your question: /cache stats         # Show statistics
❓ Your question: /cache clear         # Clear cache
```

### Additional Options
```bash
# Get help
inquisitor --help

# Disable colored output
inquisitor --no-color "Python 3.12 features"

# Specify number of search results (default: 8)
inquisitor --results 5 "Climate change solutions"

# Disable streaming output
inquisitor --no-streaming "Explain machine learning"

# Generate a random interesting question
inquisitor --random

# Enable verbose debug output
inquisitor --verbose "Debug this query"

# Show version
inquisitor --version
```

## Caching System

Inquisitor features an intelligent caching system that:
- **Automatically stores** all Q&A pairs with timestamps and sources
- **Detects similar questions** using fuzzy matching (70%+ similarity threshold)
- **Provides instant retrieval** for exact and similar questions
- **Enables offline access** to previous answers
- **Supports full-text search** across cached content

### Cache Behavior
- **Default**: Cache is always enabled for storage, retrieval requires `--use-cache` flag
- **Storage**: All answers are automatically cached unless `--no-cache` is used
- **Retrieval**: Similar questions are only suggested when `--use-cache` flag is provided
- **Override**: Use `--force-refresh` to bypass cache and get fresh results

### Cache Management
- **Location**: `~/.inquisitor_cache/qa_cache.json`
- **Expiration**: 30 days (configurable)
- **Size limit**: 1000 entries (configurable)
- **Automatic cleanup**: Removes expired and excess entries

### Cache Features
- Stores questions, answers, source links, and metadata
- Similarity matching for related questions
- Full-text search across Q&As
- Statistics and management commands
- JSON format for easy inspection and backup

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

### Example Output

```
❯ inquisitor "Compare the GDP of top 4 G7 countries"
⏳ Searching the web...
✓ Found 6 results
⏳ Generating answer...

==================================================
                Inquisitor Answer                 
==================================================

When comparing the GDP of the top 4 G7 countries, we can look at the nominal GDP figures for these nations. According to the data provided, the top 4 G7 countries by nominal GDP are as follows:


1. United States: $27,720,700,000,000 [5]
2. China: $17,794,800,000,000 [5]
3. Germany: $4,525,700,000,000 [5]
4. Japan: $4,204,490,000,000 [5]


These figures highlight the economic strength of these countries within the G7 group. The United States leads by a significant margin, followed by China, with Germany and Japan rounding out the top 4.


It's important to note that the G7 countries collectively represent 28.4% of global GDP (PPP) as of today, a decrease from around 50% in the 1980s [2]. This indicates the evolving landscape of the global economy and the shifting contributions of different countries to the world's GDP.


In summary, the GDP of the top 4 G7 countries ranks the United States as the largest economy, followed by China, Germany, and Japan in that order based on nominal GDP figures [5].



Sources:

[1] Visualizing the G7 Economies by GDP Size
    https://www.visualcapitalist.com/visualizing-the-g7-economies-by-gdp-size/
    This chart breaks down the G7 economy, highlighting each member state's share of PPP-adjusted GDP. Data is sourced from the International Monetary Fund (2024)

[2] G7 vs. the World: GDP, Population, and Military Strength
    https://www.visualcapitalist.com/g7-vs-the-world-gdp-population-and-military-strength/
    G7 countries represent 28.4% of global GDP (PPP) today, down from about 50% in the 1980s · The G7 accounts for only 9.6% of the world's ...

[3] GDP international comparisons: Economic indicators
    https://commonslibrary.parliament.uk/research-briefings/sn02784/
    GDP measures the size of the economy. Find the latest GDP growth data for the UK and comparisons with other G7 economies.

[4] List of countries by GDP (nominal)
    https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)
    Countries are sorted by nominal GDP estimates from financial and statistical institutions, which are calculated at market or government official exchange rates.

[5] GDP by Country
    https://www.worldometers.info/gdp/gdp-by-country/
    GDP by Country ; 1, United States, $27,720,700,000,000 ; 2, China, $17,794,800,000,000 ; 3, Germany, $4,525,700,000,000 ; 4, Japan, $4,204,490,000,000 ...

[6] Infographic: Comparison of the GDP of BRICS and G7 ...
    https://www.reddit.com/r/Popular_Science_Ru/comments/1i7z568/%D0%B8%D0%BD%D1%84%D0%BE%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D0%BA%D0%B0_%D1%81%D1%80%D0%B0%D0%B2%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5_%D0%B2%D0%B2%D0%BF_%D1%81%D1%82%D1%80%D0%B0%D0%BD_%D0%B1%D1%80%D0%B8%D0%BA%D1%81_%D0%B8_%D0%B1%D0%BE%D0%BB%D1%8C%D1%88%D0%BE%D0%B9/?tl=en
    BRICS+, which includes 10 countries, will account for approximately 29% of global GDP in 2025, while the G7 will remain dominant (45%). Among ...

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

- **Python 3.7+** (tested up to Python 3.12)
- **Internet connection** for web search and LLM synthesis
- **SerpAPI account** - Free tier available at [serpapi.com](https://serpapi.com/)
- **OpenAI API account** - Get your key at [platform.openai.com](https://platform.openai.com/api-keys)

### Dependencies
- `requests>=2.31.0` - HTTP requests
- `openai>=1.0.0` - OpenAI API client
- `colorama>=0.4.6` - Cross-platform colored terminal text
- `python-dotenv>=1.0.0` - Environment variable management
- `rich>=13.0.0` - Rich text and beautiful formatting for charts

## License

MIT License - see [LICENSE](LICENSE) file for details.
