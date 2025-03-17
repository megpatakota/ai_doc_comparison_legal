import json
import os
import logging
from typing import Dict
import litellm
from src.file_io import load_txt, save_to_json
from src.base import EvaluationResults
from config import MODEL_NAME
import jinja2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

output_folder = "data/output"


def evaluate_output(text: str) -> Dict[str, float]:
    """Evaluate the LLM-generated output using LiteLLM with OpenAI models."""
    logger.info("Loading evaluation template from templates/evaluation.j2")
    try:
        with open("templates/evaluation.j2") as f:
            evaluation = jinja2.Template(f.read()).render()
    except Exception as e:
        logger.error("Failed to load or render evaluation template: %s", e)
        raise

    logger.info("Requesting LLM completion using model %s", MODEL_NAME)
    try:
        response = litellm.completion(
            model=MODEL_NAME,  # Adjust the model as needed
            messages=[{"role": "user", "content": evaluation}],
            response_format=EvaluationResults,
        )
    except Exception as e:
        logger.error("LLM completion request failed: %s", e)
        raise

    try:
        evaluation_results = json.loads(response["choices"][0]["message"]["content"])
    except Exception as e:
        logger.error("Failed to parse LLM response: %s", e)
        raise

    scores = [result["score"] for result in evaluation_results["results"]]
    # Multiply by 4 because each criterion is scored out of 4
    grade = (sum(scores) / (len(scores) * 4)) * 100
    evaluation_results["grade"] = grade
    logger.info("Evaluation completed with grade: %.2f", grade)
    return evaluation_results


def run_eval():
    logger.info("Starting evaluation process")
    file1_path = os.path.join(output_folder, "final_output_main_llm.txt")
    file2_path = os.path.join(output_folder, "final_output_simple_llm.txt")

    logger.info("Loading text files:\n%s\n%s", file1_path, file2_path)
    text1 = load_txt(file1_path)
    text2 = load_txt(file2_path)

    logger.info("Evaluating first output...")
    scores1 = evaluate_output(text1)
    logger.info("Evaluating second output...")
    scores2 = evaluate_output(text2)

    results = {"output_main_llm": scores1, "output_simple_llm": scores2}

    output_file = os.path.join(output_folder, "evaluation_results.json")
    save_to_json(results, output_file)
    logger.info("Evaluation results saved to %s", output_file)

run_eval()