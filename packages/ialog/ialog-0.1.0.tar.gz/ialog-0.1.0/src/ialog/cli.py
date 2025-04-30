"""
CLI interface for ialog
"""

import argparse
import json
import os
import sys
from typing import List, Optional, Dict
from datetime import datetime

import requests
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

console = Console()

# Available models and their context windows
SUPPORTED_MODELS = {
    "mixtral-8x7b-32768": 32768,
    "llama2-70b-4096": 4096,
    "gemma-7b-it": 8192,
}

# Analysis types and their descriptions
ANALYSIS_TYPES = {
    "general": "General log analysis with patterns and issues",
    "security": "Focus on security issues and vulnerabilities",
    "performance": "Analyze performance bottlenecks and optimization opportunities",
    "error": "Deep dive into errors and exceptions",
    "audit": "Compliance and audit-focused analysis"
}

def load_config():
    """Load configuration from environment variables and config file"""
    load_dotenv()
    
    config = {
        "api_key": os.getenv("GROQ_API_KEY"),
        "model": os.getenv("GROQ_MODEL", "mixtral-8x7b-32768"),
        "base_url": os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1")
    }
    
    return config

def get_analysis_prompt(logs: str, analysis_type: str) -> Dict[str, str]:
    """Generate appropriate prompt based on analysis type"""
    prompts = {
        "general": f"""Analyze these logs and provide insights:
{logs}

Provide a detailed analysis including:
1. Key events and patterns
2. Potential issues or anomalies
3. Recommendations for improvement
4. Any security concerns""",

        "security": f"""Perform a security-focused analysis of these logs:
{logs}

Focus on:
1. Security vulnerabilities and threats
2. Suspicious activities or patterns
3. Access control issues
4. Security best practices recommendations
5. Potential compliance violations""",

        "performance": f"""Analyze these logs for performance issues:
{logs}

Provide insights on:
1. Performance bottlenecks
2. Resource usage patterns
3. Slow operations and their impact
4. Optimization recommendations
5. System efficiency metrics""",

        "error": f"""Perform error analysis on these logs:
{logs}

Focus on:
1. Error patterns and frequencies
2. Root cause analysis
3. Impact assessment
4. Prevention recommendations
5. Error handling improvements""",

        "audit": f"""Conduct an audit analysis of these logs:
{logs}

Include:
1. Compliance violations
2. Policy adherence
3. Access patterns
4. Data handling practices
5. Audit trail completeness"""
    }
    
    return prompts.get(analysis_type, prompts["general"])

def analyze_logs(logs: str, config: Dict[str, str], analysis_type: str = "general") -> Optional[str]:
    """Analyze logs using Groq API"""
    if not config["api_key"]:
        console.print("[red]Error: GROQ_API_KEY environment variable not set[/red]")
        return None
        
    headers = {
        "Authorization": f"Bearer {config['api_key']}",
        "Content-Type": "application/json"
    }
    
    prompt = get_analysis_prompt(logs, analysis_type)
    
    data = {
        "model": config["model"],
        "messages": [
            {"role": "system", "content": "You are an expert log analyst specializing in security, performance, and system analysis."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": min(SUPPORTED_MODELS[config["model"]] - 1000, 2000)  # Leave room for prompt
    }
    
    try:
        response = requests.post(
            f"{config['base_url']}/chat/completions",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        console.print(f"[red]Error calling Groq API: {str(e)}[/red]")
        return None

def show_models():
    """Display available models and their capabilities"""
    table = Table(title="Supported Models")
    table.add_column("Model Name", style="cyan")
    table.add_column("Max Context", style="green")
    
    for model, context in SUPPORTED_MODELS.items():
        table.add_row(model, f"{context:,} tokens")
    
    console.print(table)

def show_analysis_types():
    """Display available analysis types"""
    table = Table(title="Analysis Types")
    table.add_column("Type", style="cyan")
    table.add_column("Description", style="green")
    
    for analysis_type, description in ANALYSIS_TYPES.items():
        table.add_row(analysis_type, description)
    
    console.print(table)

def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="AI-powered log analysis tool"
    )
    parser.add_argument(
        "log_file",
        help="Path to the log file to analyze",
        nargs="?"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "-m", "--model",
        choices=list(SUPPORTED_MODELS.keys()),
        default="mixtral-8x7b-32768",
        help="Language model to use for analysis"
    )
    parser.add_argument(
        "-t", "--type",
        choices=list(ANALYSIS_TYPES.keys()),
        default="general",
        help="Type of analysis to perform"
    )
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List available language models"
    )
    parser.add_argument(
        "--list-types",
        action="store_true",
        help="List available analysis types"
    )
    parser.add_argument(
        "-o", "--output",
        choices=["text", "json", "markdown"],
        default="text",
        help="Output format"
    )
    
    return parser.parse_args(args)

def format_output(analysis: str, output_format: str) -> str:
    """Format the analysis output according to the specified format"""
    if output_format == "json":
        # Try to structure the analysis into sections
        sections = {
            "analysis": analysis,
            "timestamp": datetime.now().isoformat(),
            "format_version": "1.0"
        }
        return json.dumps(sections, indent=2)
    elif output_format == "markdown":
        return f"# Log Analysis Results\n\n{analysis}"
    else:
        return analysis

def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI."""
    parsed_args = parse_args(args)
    
    if parsed_args.list_models:
        show_models()
        return 0
        
    if parsed_args.list_types:
        show_analysis_types()
        return 0
    
    if not parsed_args.log_file:
        console.print("[red]Error: Log file is required unless using --list-models or --list-types[/red]")
        return 1
    
    try:
        with open(parsed_args.log_file, 'r') as f:
            logs = f.read()
            
        config = load_config()
        config["model"] = parsed_args.model
        
        if parsed_args.verbose:
            console.print(f"[blue]Using model: {parsed_args.model}[/blue]")
            console.print(f"[blue]Analysis type: {parsed_args.type}[/blue]")
        
        analysis = analyze_logs(logs, config, parsed_args.type)
        
        if analysis:
            formatted_output = format_output(analysis, parsed_args.output)
            
            if parsed_args.output == "json":
                console.print_json(formatted_output)
            elif parsed_args.output == "markdown":
                console.print(Markdown(formatted_output))
            else:
                console.print(Panel(
                    formatted_output,
                    title="Log Analysis Results",
                    border_style="blue"
                ))
        else:
            console.print("[red]Failed to analyze logs[/red]")
            
        return 0
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 