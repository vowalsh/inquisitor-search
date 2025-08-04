# Inquisitor

**Lightweight Python CLI for Perplexity-style answers**

Inquisitor combines live web search with LLM synthesis to deliver real-time, cited answers directly in your terminal. Get comprehensive, up-to-date information with transparent source attribution.

## Features

- **Live Web Search** - Real-time results using SerpAPI
- **LLM Synthesis** - AI-powered answer generation with OpenAI
- **Inline Citations** - Transparent source attribution with [1], [2] references
- **Beautiful Output** - Colored terminal display with clear formatting
- **Fast & Lightweight** - Minimal dependencies, maximum performance
- **Interactive Mode** - Continuous Q&A sessions
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

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

4. **Get API Keys:**
   - **SerpAPI**: Sign up at [serpapi.com](https://serpapi.com/) for web search
   - **OpenAI**: Get your key at [platform.openai.com](https://platform.openai.com/api-keys)

## Usage

### Interactive Mode
```bash
python inquisitor.py
```

### Single Query
```bash
python inquisitor.py "What are the latest developments in AI?"
```

### Options
```bash
python inquisitor.py --help
python inquisitor.py --no-color "Python 3.12 features"
python inquisitor.py --results 5 "Climate change solutions"
```

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

## Architecture

- **`inquisitor.py`** - Main CLI interface and orchestration
- **`search.py`** - Web search functionality using SerpAPI
- **`llm.py`** - LLM synthesis with OpenAI integration
- **`formatting.py`** - Output formatting and terminal display

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

[Add your license here]

## Contributing

[Add contribution guidelines here]
