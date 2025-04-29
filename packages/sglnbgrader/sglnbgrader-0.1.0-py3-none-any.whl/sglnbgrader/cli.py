import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from .grader import Grader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize Typer app and console
app = typer.Typer(help="Grade Jupyter notebooks using LLM")
console = Console()

def grade_single_notebook(
    answer_path: str,
    student_path: str,
    model: str = "gpt-4.1-nano",
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Grade a single student notebook against an answer notebook.
    
    Args:
        answer_path: Path to the instructor's answer notebook
        student_path: Path to the student's notebook
        model: The LLM model to use for grading
        verbose: Whether to display detailed grading information
        
    Returns:
        Grading results
    """
    with console.status(f"Grading [bold blue]{student_path}[/]..."):
        logger.info(f"Grading {student_path} using {answer_path} as reference")
        grader = Grader(answer_path, model=model)
        results = grader.grade_user_notebook(student_path)
    
    # Display summary
    display_results(results, verbose)
    
    return results

def display_results(results: Dict[str, Any], verbose: bool = False):
    """Display grading results in a nicely formatted way."""
    console.print()
    console.print(Panel(
        f"[bold green]Total Score:[/] {results['total_score']:.1f}/{results['max_score']} "
        f"([bold]{'%.2f' % results['percentage']}%[/])",
        title="Grading Results",
        expand=False
    ))
    
    if verbose:
        # Display detailed results for each question
        table = Table(title="Question-by-Question Breakdown")
        table.add_column("Question ID", style="cyan")
        table.add_column("Score", style="green")
        table.add_column("Max", style="blue")
        table.add_column("Feedback", style="yellow")
        
        for item in results["results"]:
            table.add_row(
                item["grade_id"],
                f"{item['score']:.1f}",
                f"{item['max_score']:.1f}",
                item["feedback"][:50] + "..." if len(item["feedback"]) > 50 else item["feedback"]
            )
            
        console.print(table)

def grade_multiple_notebooks(
    answer_path: str,
    submissions_dir: str,
    output_dir: Optional[str] = None,
    model: str = "gpt-4.1-nano",
    verbose: bool = False
) -> Dict[str, Dict[str, Any]]:
    """
    Grade multiple student notebooks in a directory.
    
    Args:
        answer_path: Path to the instructor's answer notebook
        submissions_dir: Directory containing student submissions
        output_dir: Directory to save grading results (optional)
        model: The LLM model to use for grading
        verbose: Whether to display detailed grading information
        
    Returns:
        Dictionary mapping student notebook paths to grading results
    """
    # Find all notebook files in the submissions directory
    submissions_path = Path(submissions_dir)
    notebook_files = list(submissions_path.glob("*.ipynb"))
    
    if not notebook_files:
        console.print(f"[bold red]No notebook files found in {submissions_dir}[/]")
        return {}
    
    console.print(f"Found [bold green]{len(notebook_files)}[/] notebook files to grade")
    
    # Initialize the grader (only need to load the answer notebook once)
    with console.status(f"Initializing grader with answer notebook..."):
        grader = Grader(answer_path, model=model)
    
    # Grade each notebook
    results = {}
    summary_table = Table(title="Grading Summary")
    summary_table.add_column("Notebook", style="cyan")
    summary_table.add_column("Score", style="green")
    summary_table.add_column("Max", style="blue")
    summary_table.add_column("Percentage", style="yellow")
    
    for notebook_path in notebook_files:
        notebook_name = notebook_path.name
        with console.status(f"Grading [bold blue]{notebook_name}[/]..."):
            logger.info(f"Grading {notebook_name}")
            try:
                result = grader.grade_user_notebook(str(notebook_path))
                results[str(notebook_path)] = result
                
                summary_table.add_row(
                    notebook_name,
                    f"{result['total_score']:.1f}",
                    f"{result['max_score']:.1f}",
                    f"{result['percentage']:.2f}%"
                )
            except Exception as e:
                logger.error(f"Error grading {notebook_name}: {str(e)}")
                console.print(f"[bold red]Error grading {notebook_name}: {str(e)}[/]")
    
    # Display summary
    console.print(summary_table)
    
    # Save results if output_dir is provided
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save aggregate results
        with open(output_path / "all_results.json", "w") as f:
            json.dump(results, f, indent=2)
        
        # Save individual results
        for notebook_path, result in results.items():
            notebook_name = Path(notebook_path).stem
            with open(output_path / f"{notebook_name}_results.json", "w") as f:
                json.dump(result, f, indent=2)
        
        console.print(f"[bold green]Results saved to {output_dir}[/]")
    
    return results

@app.command("single")
def single_command(
    answer: str = typer.Option(..., help="Path to instructor's answer notebook"),
    student: str = typer.Option(..., help="Path to student notebook"),
    model: str = typer.Option("gpt-4.1-nano", help="LLM model to use for grading"),
    output: Optional[str] = typer.Option(None, help="Path to save grading results (optional)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed grading information")
):
    """Grade a single notebook."""
    results = grade_single_notebook(answer, student, model, verbose)
    if output:
        with open(output, "w") as f:
            json.dump(results, f, indent=2)
        console.print(f"[bold green]Results saved to {output}[/]")

@app.command("batch")
def batch_command(
    answer: str = typer.Option(..., help="Path to instructor's answer notebook"),
    submissions: str = typer.Option(..., help="Directory containing student submissions"),
    model: str = typer.Option("gpt-4.1-nano", help="LLM model to use for grading"),
    output: Optional[str] = typer.Option(None, help="Directory to save grading results (optional)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed grading information")
):
    """Grade multiple notebooks in a directory."""
    grade_multiple_notebooks(answer, submissions, output, model, verbose)

if __name__ == "__main__":
    app()