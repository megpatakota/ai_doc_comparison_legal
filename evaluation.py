import json
import os
from typing import Dict
import litellm
from src.file_io import load_txt, save_to_json
from src.base import EvaluationResults
from config import MODEL_NAME
import jinja2
from dotenv import load_dotenv

load_dotenv()

output_folder = "data/output"


def evaluate_output(text: str) -> Dict[str, float]:
    """Evaluate the LLM-generated output using LiteLLM with OpenAI models."""

    with open("templates/evaluation.j2") as f:
        evaluation = jinja2.Template(f.read()).render()

    response = litellm.completion(
        model=MODEL_NAME,  # Adjust the model as needed
        messages=[{"role": "user", "content": evaluation}],
        response_format=EvaluationResults,
    )

    evaluation_results = json.loads(response["choices"][0]["message"]["content"])

    scores = [result["score"] for result in evaluation_results["results"]]

    # Multiply by 4 because each criterion is scored out of 4
    grade = (sum(scores) / (len(scores) * 4)) * 100

    evaluation_results["grade"] = grade
    return evaluation_results


def main():
    file1_path = os.path.join(output_folder, "compare_output_pipeline1.txt")
    file2_path = os.path.join(output_folder, "compare_output_pipeline2.txt")

    text1 = load_txt(file1_path)
    text2 = load_txt(file2_path)

    print("Evaluating first output...")
    scores1 = evaluate_output(text1)
    print("\nEvaluating second output...")
    scores2 = evaluate_output(text2)

    results = {"output_1": scores1, "output_2": scores2}

    output_file = os.path.join(output_folder, "evaluation_results.json")
    save_to_json(results, output_file)

    print(f"Evaluation results saved to {output_file}")


if __name__ == "__main__":
    main()
