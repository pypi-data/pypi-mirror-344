# AI Readme

Generate a professional `README.md` automatically by analyzing project files using AI.

## Features

- English and Korean README generation.
- Support OpenAI, Claude, Gemini models.
- Detailed, professional README templates.
- Smart file ignoring (.git, node_modules, etc.).
- Easy .env based API key configuration.

## Installation

```bash
pip install ai-readme
```

## Usage

```bash
readme --lang en --provider openai
readme --lang ko --provider claude
readme --lang en --provider gemini
readme --lang en --provider openai --max_chars 20000
```

## Setting up API Keys

You must configure your API keys before using this tool.  
There are two ways:

### 1. Using a `.env` file (Recommended)

Create a `.env` file in your project root and add:

```
OPENAI_API_KEY=your-openai-api-key
CLAUDE_API_KEY=your-claude-api-key
GEMINI_API_KEY=your-gemini-api-key
```

The program automatically loads this file.

### 2. Setting environment variables manually

If you prefer, you can set them manually in your terminal session:

**Linux / macOS:**
```bash
export OPENAI_API_KEY=your-openai-api-key
```

**Windows CMD:**
```bash
set OPENAI_API_KEY=your-openai-api-key
```

**Windows PowerShell:**
```powershell
$env:OPENAI_API_KEY="your-openai-api-key"
```

## License

MIT License