import litellm
import nbformat
import logging
import re
from typing import Dict, List, Optional, Tuple, Union, Any, Set


class Grader:
    def __init__(self, answer_notebook_path: str, model: str = "gpt-4.1-nano"):
        """
        Initialize the Grader with an answer notebook path and model.
        
        Args:
            answer_notebook_path: Path to the instructor's answer notebook
            model: The LLM model to use for grading (default: gpt-4.1-nano)
        """
        self.answer_notebook_path = answer_notebook_path
        self.answer_notebook = self.load_notebook(answer_notebook_path)
        self.model = model
        # Cache for grade_id to cell mapping
        self._grade_id_to_cell_map = None
        # Configure logging
        self.logger = logging.getLogger(__name__)

    def load_notebook(self, notebook_path: str) -> nbformat.NotebookNode:
        """
        Load a Jupyter notebook from a file path.
        
        Args:
            notebook_path: Path to the notebook file
            
        Returns:
            The loaded notebook as a nbformat.NotebookNode
        """
        return nbformat.read(notebook_path, as_version=4)
    
    def is_grade_cell(self, cell: Dict[str, Any]) -> bool:
        """
        Check if a cell is marked for grading.
        
        Args:
            cell: A notebook cell
            
        Returns:
            True if the cell is marked for grading, False otherwise
        """
        return (
            'nbgrader' in cell.get('metadata', {}) and 
            cell['metadata']['nbgrader'].get('grade', False)
        )
    
    def get_grade_id_to_cell_map(self) -> Dict[str, List[int]]:
        """
        Create a mapping from grade_id to cell indices in the answer notebook.
        Handles duplicate grade_ids by mapping each to a list of cell indices.
        
        Returns:
            A dictionary mapping grade_id to a list of cell indices
        """
        if self._grade_id_to_cell_map is not None:
            return self._grade_id_to_cell_map
        
        grade_id_to_cells = {}
        for i, cell in enumerate(self.answer_notebook.cells):
            if self.is_grade_cell(cell):
                grade_id = cell['metadata']['nbgrader']['grade_id']
                if grade_id not in grade_id_to_cells:
                    grade_id_to_cells[grade_id] = []
                grade_id_to_cells[grade_id].append(i)
        
        # Log any duplicate grade_ids
        duplicates = {grade_id: indices for grade_id, indices in grade_id_to_cells.items() if len(indices) > 1}
        if duplicates:
            self.logger.warning(f"Found duplicate grade_ids: {duplicates}")
        
        self._grade_id_to_cell_map = grade_id_to_cells
        return grade_id_to_cells
    
    def get_cell_by_grade_id(self, notebook: nbformat.NotebookNode, grade_id: str) -> Optional[Dict[str, Any]]:
        """
        Find a cell in a notebook by its grade_id.
        If multiple cells have the same grade_id, returns the first one.
        
        Args:
            notebook: The notebook to search in
            grade_id: The grade_id to look for
            
        Returns:
            The cell with the matching grade_id, or None if not found
        """
        for cell in notebook.cells:
            if (
                'nbgrader' in cell.get('metadata', {}) and
                cell['metadata']['nbgrader'].get('grade_id', '') == grade_id
            ):
                return cell
        return None
    
    def get_cell_content(self, cell: Dict[str, Any]) -> str:
        """
        Extract the content from a cell.
        
        Args:
            cell: A notebook cell
            
        Returns:
            The source content of the cell as a string
        """
        return cell.get('source', '')
    
    def get_context_cells(self, notebook: nbformat.NotebookNode, cell_idx: int, 
                          num_before: int = 1, num_after: int = 0) -> List[Dict[str, Any]]:
        """
        Get neighboring cells around a specified cell for context.
        
        Args:
            notebook: The notebook to get cells from
            cell_idx: Index of the target cell
            num_before: Number of cells to get before the target cell
            num_after: Number of cells to get after the target cell
            
        Returns:
            List of neighboring cells
        """
        start_idx = max(0, cell_idx - num_before)
        end_idx = min(len(notebook.cells), cell_idx + num_after + 1)
        return notebook.cells[start_idx:end_idx]
    
    def format_prompt(self, question: str, reference_answer: str, student_answer: str, points: Union[int, float]) -> str:
        """
        Format the prompt template with the given values.
        
        Args:
            question: The question text
            reference_answer: The reference answer from the instructor
            student_answer: The student's answer
            points: The maximum points for this question
            
        Returns:
            Formatted prompt string
        """
        return self.prompt.format(
            question=question,
            reference_answer=reference_answer,
            student_answer=student_answer,
            points=points
        )
    
    def call_llm(self, prompt: str) -> str:
        """
        Call the LLM with the given prompt.
        
        Args:
            prompt: The prompt to send to the LLM
            
        Returns:
            The LLM's response as a string
        """
        try:
            response = litellm.completion(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,  # Low temperature for more consistent grading
                max_tokens=1000,  # Adjust based on expected response length
            )
            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f"Error calling LLM: {str(e)}")
            raise
    
    def parse_llm_response(self, response: str, max_points: Union[int, float]) -> Dict[str, Any]:
        """
        Parse the LLM's response to extract the score and feedback.
        
        Args:
            response: The LLM's response string
            max_points: The maximum possible points for this question
            
        Returns:
            Dictionary with score and feedback
        """
        try:
            # Extract score using regex
            score_match = re.search(r'Score:\s*(\d+(?:\.\d+)?)\s*(?:out of|\/)\s*\d+(?:\.\d+)?', response)
            if score_match:
                score = float(score_match.group(1))
            else:
                # Try a simpler pattern if the first one fails
                score_match = re.search(r'Score:\s*(\d+(?:\.\d+)?)', response)
                if score_match:
                    score = float(score_match.group(1))
                else:
                    self.logger.warning(f"Could not extract score from response: {response}")
                    score = 0
            
            # Extract feedback
            feedback_match = re.search(r'Feedback:(.*?)(?:$|Score:)', response, re.DOTALL)
            if feedback_match:
                feedback = feedback_match.group(1).strip()
            else:
                # If no specific feedback section, use the whole response as feedback
                # but remove the score part if present
                feedback = re.sub(r'Score:\s*\d+(?:\.\d+)?(?:\s*(?:out of|\/)\s*\d+(?:\.\d+)?)?', '', response).strip()
            
            # Ensure score is within bounds
            score = max(0, min(score, max_points))
            
            return {
                "score": score,
                "max_score": max_points,
                "feedback": feedback
            }
        except Exception as e:
            self.logger.error(f"Error parsing LLM response: {str(e)}")
            return {
                "score": 0,
                "max_score": max_points,
                "feedback": f"Error parsing response: {str(e)}. Original response: {response}"
            }

    @property
    def prompt(self):
        """
        Default prompt template for grading.
        """
        return """
        You are an expert grader for a machine learning course. You will be grading a student's answer to a question.

        Question:
        {question}

        Reference Answer:
        {reference_answer}

        Student Answer:
        {student_answer}

        The question is worth {points} points.

        Please grade the student's answer and provide feedback. Return your response in the following format:
        Score: [score out of {points}]
        Feedback: [your feedback explaining the score]
        """

    def get_all_grade_ids(self) -> List[str]:
        """
        Get all the grade ids from the answer notebook.
        If there are duplicate grade_ids, they will appear multiple times in the result list,
        in the order they appear in the notebook.
        
        Returns:
            List of grade_ids from cells marked for grading
        """
        grade_ids = []
        for cell in self.answer_notebook.cells:
            if self.is_grade_cell(cell):
                grade_id = cell['metadata']['nbgrader']['grade_id']
                grade_ids.append(grade_id)
        
        # Log if there are any duplicate grade_ids
        unique_ids = set(grade_ids)
        if len(unique_ids) < len(grade_ids):
            # Find the duplicates
            id_counts = {}
            for grade_id in grade_ids:
                id_counts[grade_id] = id_counts.get(grade_id, 0) + 1
            duplicates = {grade_id: count for grade_id, count in id_counts.items() if count > 1}
            self.logger.warning(f"Found duplicate grade_ids: {duplicates}")
        
        return grade_ids

    def grade_user_response(self, grade_id: str, student_notebook: nbformat.NotebookNode) -> Dict[str, Any]:
        """
        Grade the user's response to a question based on the answer notebook and
        the student notebook.

        It uses the question_id to locate the solution from the
        `answer_notebook`, the response from `student_notebook` and makes a call
        to an llm to grade the resposne

        The function might look at neighboring cells to get more context about
        the question, the solution, or grading cells.
        
        Args:
            grade_id: The grade_id of the cell to grade
            student_notebook: The student's notebook
            
        Returns:
            Dictionary with grading results
        """
        # Find the cells in both notebooks
        answer_cell = self.get_cell_by_grade_id(self.answer_notebook, grade_id)
        student_cell = self.get_cell_by_grade_id(student_notebook, grade_id)
        
        if not answer_cell:
            self.logger.error(f"Answer cell with grade_id {grade_id} not found")
            return {
                "grade_id": grade_id,
                "score": 0,
                "max_score": 0,
                "feedback": f"Error: Answer cell with grade_id {grade_id} not found",
                "error": True
            }
        
        # Get the points for this question
        points = answer_cell['metadata']['nbgrader'].get('points', 0)
        
        if not student_cell:
            self.logger.warning(f"Student cell with grade_id {grade_id} not found")
            return {
                "grade_id": grade_id,
                "score": 0,
                "max_score": points,
                "feedback": "No answer provided",
                "error": False
            }
        
        # Get the cell contents
        answer_content = self.get_cell_content(answer_cell)
        student_content = self.get_cell_content(student_cell)
        
        # If student answer is empty, return zero score
        if not student_content.strip():
            return {
                "grade_id": grade_id,
                "score": 0,
                "max_score": points,
                "feedback": "No answer provided",
                "error": False
            }
        
        # Get context (question prompt)
        # Find the index of the answer cell
        answer_cell_idx = None
        for i, cell in enumerate(self.answer_notebook.cells):
            if cell is answer_cell:
                answer_cell_idx = i
                break
        
        question_text = ""
        if answer_cell_idx is not None and answer_cell_idx > 0:
            # Get the cell before the answer cell (likely the question)
            question_cell = self.answer_notebook.cells[answer_cell_idx - 1]
            question_text = self.get_cell_content(question_cell)
        
        # Format the prompt
        prompt = self.format_prompt(
            question=question_text,
            reference_answer=answer_content,
            student_answer=student_content,
            points=points
        )
        
        try:
            # Call the LLM for grading
            llm_response = self.call_llm(prompt)
            
            # Parse the response
            grading_result = self.parse_llm_response(llm_response, max_points=points)
            
            # Return the result
            return {
                "grade_id": grade_id,
                "score": grading_result["score"],
                "max_score": grading_result["max_score"],
                "feedback": grading_result["feedback"],
                "error": False
            }
        except Exception as e:
            self.logger.error(f"Error grading response for {grade_id}: {str(e)}")
            return {
                "grade_id": grade_id,
                "score": 0,
                "max_score": points,
                "feedback": f"Error during grading: {str(e)}",
                "error": True
            }

    def grade_user_notebook(self, student_notebook_path: str) -> Dict[str, Any]:
        """
        The function grades the user's notebook based on the answer notebook.
        
        Args:
            student_notebook_path: Path to the student's notebook
            
        Returns:
            Dictionary with grading results
        """
        student_notebook = self.load_notebook(student_notebook_path)
        
        # Get all grade IDs to assess
        grade_ids = self.get_all_grade_ids()
        
        # Grade each response
        results = []
        for grade_id in grade_ids:
            result = self.grade_user_response(grade_id, student_notebook)
            results.append(result)
        
        # Calculate total score
        total_score = sum(result["score"] for result in results)
        max_score = sum(result["max_score"] for result in results)
        
        return {
            "total_score": total_score,
            "max_score": max_score,
            "percentage": (total_score / max_score * 100) if max_score > 0 else 0,
            "results": results,
            "student_notebook_path": student_notebook_path
        }
        
    def write_feedback_to_notebook(self, student_notebook_path: str, results: Dict[str, Any]) -> str:
        """
        Write feedback and scores into the student notebook's cell outputs.
        
        For each graded cell, adds HTML-formatted feedback as a display_data output.
        Also adds a summary cell at the end with the total score and breakdown.
        
        Args:
            student_notebook_path: Path to the student's notebook
            results: Dictionary with grading results from grade_user_notebook
            
        Returns:
            Path to the updated notebook with feedback
        """
        import copy
        import os
        from pathlib import Path
        
        # Load the student notebook to modify
        student_notebook = self.load_notebook(student_notebook_path)
        
        # Create a deep copy to avoid modifying the original
        feedback_notebook = copy.deepcopy(student_notebook)
        
        # Process each graded cell and add feedback
        for result in results["results"]:
            grade_id = result["grade_id"]
            score = result["score"]
            max_score = result["max_score"]
            feedback = result["feedback"]
            
            # Find the cell with this grade_id
            for cell in feedback_notebook.cells:
                if ('nbgrader' in cell.get('metadata', {}) and 
                    cell['metadata']['nbgrader'].get('grade_id') == grade_id):
                    
                    # Add HTML output with feedback
                    html_feedback = f"""
                    <div style="background-color: #f9f9f9; padding: 10px; border-radius: 5px; border-left: 5px solid #3498db;">
                        <h3 style="color: #3498db;">Grading Feedback</h3>
                        <p><strong>Score: {score}/{max_score}</strong></p>
                        <p>{feedback}</p>
                    </div>
                    """
                    
                    # Create or initialize cell outputs list if it doesn't exist
                    if not hasattr(cell, 'outputs'):
                        cell.outputs = []
                    
                    # Add a display_data output with HTML content
                    output = nbformat.v4.new_output('display_data', 
                                                   data={'text/html': html_feedback})
                    cell.outputs.append(output)
                    
                    break
        
        # Create a summary cell at the end
        total_score = results["total_score"]
        max_score = results["max_score"]
        percentage = results["percentage"]
        
        # Create a table with breakdown of scores
        table_rows = []
        for result in results["results"]:
            grade_id = result["grade_id"]
            score = result["score"]
            max_score = result["max_score"]
            table_rows.append(f"| {grade_id} | {score} | {max_score} | {score/max_score*100:.1f}% |")
        
        table_header = "| Question | Score | Max Score | Percentage |"
        table_separator = "| --- | --- | --- | --- |"
        table_body = "\n".join(table_rows)
        score_table = f"{table_header}\n{table_separator}\n{table_body}"
        
        summary_text = f"""
        ## Grading Summary
        
        Total Score: {total_score}/{max_score} ({percentage:.1f}%)
        
        ### Score Breakdown
        
        {score_table}
        """
        
        # Add the summary cell to the notebook
        summary_cell = nbformat.v4.new_markdown_cell(source=summary_text)
        feedback_notebook.cells.append(summary_cell)
        
        # Create a new file path for the feedback notebook
        notebook_path = Path(student_notebook_path)
        output_path = notebook_path.with_stem(f"{notebook_path.stem}_feedback")
        
        # Write the updated notebook to the new path
        nbformat.write(feedback_notebook, output_path)
        
        return str(output_path)
        
    def compare_student_submissions(self, submission_paths: List[str]) -> Dict[str, Any]:
        """
        Compare grading results across multiple student submissions to analyze
        consistency and identify patterns.
        
        Args:
            submission_paths: List of paths to student notebook submissions
            
        Returns:
            Dictionary with comparative analysis results
        """
        # Grade all submissions first
        all_results = []
        for path in submission_paths:
            try:
                result = self.grade_user_notebook(path)
                all_results.append(result)
            except Exception as e:
                self.logger.error(f"Error grading {path}: {str(e)}")
                # Continue with other submissions
        
        if not all_results:
            return {
                "error": True,
                "message": "No submissions were successfully graded"
            }
        
        # Extract all unique grade_ids across submissions
        all_grade_ids = set()
        for result in all_results:
            for item in result["results"]:
                all_grade_ids.add(item["grade_id"])
        
        # Initialize statistics for each grade_id
        grade_id_stats = {}
        for grade_id in all_grade_ids:
            grade_id_stats[grade_id] = {
                "scores": [],
                "max_score": 0,  # Will be set to the same value for all submissions
                "mean": 0.0,
                "median": 0.0,
                "std_dev": 0.0,
                "min": 0.0,
                "max": 0.0,
                "histogram": {},  # Frequency distribution of scores
            }
        
        # Collect scores for each grade_id across all submissions
        for result in all_results:
            for item in result["results"]:
                grade_id = item["grade_id"]
                score = item["score"]
                max_score = item["max_score"]
                
                grade_id_stats[grade_id]["scores"].append(score)
                grade_id_stats[grade_id]["max_score"] = max_score  # Should be consistent across submissions
                
                # Update histogram
                score_bin = round(score, 1)  # Round to nearest 0.1 for binning
                if score_bin not in grade_id_stats[grade_id]["histogram"]:
                    grade_id_stats[grade_id]["histogram"][score_bin] = 0
                grade_id_stats[grade_id]["histogram"][score_bin] += 1
        
        # Calculate statistics for each grade_id
        import numpy as np
        import statistics
        
        for grade_id, stats in grade_id_stats.items():
            scores = stats["scores"]
            if scores:
                stats["mean"] = statistics.mean(scores)
                stats["median"] = statistics.median(scores)
                stats["std_dev"] = statistics.stdev(scores) if len(scores) > 1 else 0.0
                stats["min"] = min(scores)
                stats["max"] = max(scores)
                
                # Sort histogram by score
                stats["histogram"] = dict(sorted(stats["histogram"].items()))
        
        # Calculate overall statistics
        total_scores = [result["total_score"] for result in all_results]
        max_scores = [result["max_score"] for result in all_results]  # Should be the same for all
        percentages = [result["percentage"] for result in all_results]
        
        overall_stats = {
            "mean_score": statistics.mean(total_scores),
            "median_score": statistics.median(total_scores),
            "std_dev_score": statistics.stdev(total_scores) if len(total_scores) > 1 else 0.0,
            "min_score": min(total_scores),
            "max_score": max(total_scores),
            "mean_percentage": statistics.mean(percentages),
            "median_percentage": statistics.median(percentages),
            "std_dev_percentage": statistics.stdev(percentages) if len(percentages) > 1 else 0.0,
            "min_percentage": min(percentages),
            "max_percentage": max(percentages),
        }
        
        # Generate consistency metrics
        consistency_metrics = {
            "grade_id_coefficient_of_variation": {},  # Lower is more consistent
            "overall_coefficient_of_variation": overall_stats["std_dev_score"] / overall_stats["mean_score"] if overall_stats["mean_score"] else 0,
        }
        
        for grade_id, stats in grade_id_stats.items():
            if stats["mean"] > 0:
                consistency_metrics["grade_id_coefficient_of_variation"][grade_id] = stats["std_dev"] / stats["mean"]
        
        return {
            "submission_count": len(all_results),
            "grade_id_stats": grade_id_stats,
            "overall_stats": overall_stats,
            "consistency_metrics": consistency_metrics,
            "submissions_analyzed": [result["student_notebook_path"] for result in all_results]
        }
    
    def run_benchmarks(self, reference_results: Dict[str, Any], submission_paths: List[str] = None) -> Dict[str, Any]:
        """
        Run benchmarking tests to validate scoring consistency and performance.
        
        This method assesses the grading system's consistency by comparing results
        against a reference standard and analyzing variability across submissions.
        
        Args:
            reference_results: Reference grading results to compare against
            submission_paths: Optional list of student submission paths to analyze
                              If None, will use submissions from compare_student_submissions
            
        Returns:
            Dictionary with benchmark results and performance metrics
        """
        import time
        import statistics
        
        # Initialize benchmark results
        benchmark_results = {
            "consistency": {},
            "performance": {},
            "fairness": {},
        }
        
        # Run comparison if submission paths are provided
        comparison_results = None
        if submission_paths:
            start_time = time.time()
            comparison_results = self.compare_student_submissions(submission_paths)
            elapsed_time = time.time() - start_time
            
            # Record performance metrics
            benchmark_results["performance"]["comparison_time"] = elapsed_time
            benchmark_results["performance"]["average_grading_time"] = elapsed_time / len(submission_paths) if submission_paths else 0
        
        # Assess consistency relative to reference results
        if reference_results and comparison_results:
            # Compare each grade_id's statistics to reference expectations
            for grade_id, stats in comparison_results["grade_id_stats"].items():
                # Find corresponding reference result
                ref_item = None
                for item in reference_results["results"]:
                    if item["grade_id"] == grade_id:
                        ref_item = item
                        break
                
                if ref_item:
                    # Calculate consistency metrics
                    benchmark_results["consistency"][grade_id] = {
                        "reference_score": ref_item["score"],
                        "mean_score": stats["mean"],
                        "deviation_from_reference": abs(ref_item["score"] - stats["mean"]),
                        "normalized_deviation": abs(ref_item["score"] - stats["mean"]) / ref_item["max_score"] if ref_item["max_score"] else 0,
                        "coefficient_of_variation": stats["std_dev"] / stats["mean"] if stats["mean"] else 0,
                    }
        
        # Assess fairness (if we have comparison results)
        if comparison_results:
            # Fairness can be assessed by looking at the distribution of scores
            # and checking if any questions have unusually high variance or skewed distributions
            grade_id_stats = comparison_results["grade_id_stats"]
            
            # Calculate fairness metrics for each grade_id
            for grade_id, stats in grade_id_stats.items():
                scores = stats["scores"]
                max_score = stats["max_score"]
                
                if scores and max_score:
                    # Calculate normalized scores (0-1 scale)
                    normalized_scores = [score / max_score for score in scores]
                    
                    # Calculate fairness metrics
                    benchmark_results["fairness"][grade_id] = {
                        "score_distribution": stats["histogram"],
                        "normalized_std_dev": stats["std_dev"] / max_score,
                        "skewness": self._calculate_skewness(normalized_scores) if len(normalized_scores) > 2 else 0,
                        "mean_normalized_score": statistics.mean(normalized_scores),
                    }
        
        # Overall benchmark assessment
        if comparison_results:
            benchmark_results["overall"] = {
                "submission_count": comparison_results["submission_count"],
                "consistency_score": self._calculate_consistency_score(benchmark_results["consistency"]) if "consistency" in benchmark_results else None,
                "fairness_score": self._calculate_fairness_score(benchmark_results["fairness"]) if "fairness" in benchmark_results else None,
                "overall_benchmark_score": None,  # Will be calculated below
            }
            
            # Calculate overall benchmark score if both consistency and fairness scores exist
            if benchmark_results["overall"]["consistency_score"] is not None and benchmark_results["overall"]["fairness_score"] is not None:
                # Weighted average of consistency (60%) and fairness (40%)
                benchmark_results["overall"]["overall_benchmark_score"] = (
                    0.6 * benchmark_results["overall"]["consistency_score"] +
                    0.4 * benchmark_results["overall"]["fairness_score"]
                )
        
        return benchmark_results
    
    def _calculate_skewness(self, data):
        """
        Calculate the skewness of a distribution.
        Skewness measures the asymmetry of the probability distribution.
        
        Args:
            data: List of values
            
        Returns:
            Skewness value
        """
        import numpy as np
        if len(data) < 3:
            return 0
        
        n = len(data)
        mean = np.mean(data)
        std_dev = np.std(data, ddof=1)  # Sample standard deviation
        
        if std_dev == 0:
            return 0
            
        # Calculate skewness
        skewness = (np.sum((data - mean) ** 3) / n) / (std_dev ** 3)
        return skewness
    
    def _calculate_consistency_score(self, consistency_data):
        """
        Calculate an overall consistency score from consistency metrics.
        
        Args:
            consistency_data: Dictionary with consistency metrics for each grade_id
            
        Returns:
            Consistency score (0-100 scale, higher is better)
        """
        if not consistency_data:
            return None
            
        # Calculate average normalized deviation from reference
        normalized_deviations = [
            metrics["normalized_deviation"] 
            for grade_id, metrics in consistency_data.items()
        ]
        
        if not normalized_deviations:
            return None
            
        avg_deviation = sum(normalized_deviations) / len(normalized_deviations)
        
        # Convert to a 0-100 scale (lower deviation = higher consistency)
        # 0 deviation = 100 score, 0.5+ deviation = 0 score
        consistency_score = max(0, 100 * (1 - 2 * avg_deviation))
        
        return consistency_score
    
    def _calculate_fairness_score(self, fairness_data):
        """
        Calculate an overall fairness score from fairness metrics.
        
        Args:
            fairness_data: Dictionary with fairness metrics for each grade_id
            
        Returns:
            Fairness score (0-100 scale, higher is better)
        """
        if not fairness_data:
            return None
            
        # Calculate average normalized standard deviation (lower is better)
        normalized_std_devs = [
            metrics["normalized_std_dev"] 
            for grade_id, metrics in fairness_data.items()
        ]
        
        if not normalized_std_devs:
            return None
            
        avg_std_dev = sum(normalized_std_devs) / len(normalized_std_devs)
        
        # Calculate average absolute skewness (lower is better)
        skewness_values = [
            abs(metrics["skewness"])
            for grade_id, metrics in fairness_data.items()
            if "skewness" in metrics
        ]
        
        avg_skewness = sum(skewness_values) / len(skewness_values) if skewness_values else 0
        
        # Convert to a 0-100 scale
        # 0 std_dev and skewness = 100 score
        # 0.5+ std_dev or 2+ skewness = 0 score
        std_dev_score = max(0, 100 * (1 - 2 * avg_std_dev))
        skewness_score = max(0, 100 * (1 - 0.5 * avg_skewness))
        
        # Weighted average (std_dev weighted higher as it's more important for fairness)
        fairness_score = 0.7 * std_dev_score + 0.3 * skewness_score
        
        return fairness_score