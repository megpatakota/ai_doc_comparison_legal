import json
import os
from typing import Dict
import litellm
from src.file_io import load_txt, save_to_json
from config import MODEL_NAME
import jinja2

output_folder = "data/output"


def evaluate_output(text: str) -> Dict[str, float]:
    """Evaluate the LLM-generated output using LiteLLM with OpenAI models."""
    
    with open('templates/evaluation.j2') as f:
        evaluation = jinja2.Template(f.read()).render()
    
    response = litellm.completion(
        model=MODEL_NAME,  # Adjust the model as needed
        messages=[{"role": "user", "content": evaluation}]
    )
    
    try:
        scores = json.loads(response["choices"][0]["message"]["content"])
    except (KeyError, json.JSONDecodeError):
        scores = {criterion: 0.0 for criterion in rubric}  # Default to zero in case of failure
    
    scores["total_score"] = sum(scores.values()) / len(rubric)  # Average score
    return scores

def main():
    file1_path = os.path.join(output_folder, 'compare_output_pipeline1.txt')
    file2_path = os.path.join(output_folder, 'compare_output_pipeline2.txt')
    
    text1 = load_txt(file1_path)
    text2 = load_txt(file2_path)
    
    print("Evaluating first output...")
    scores1 = evaluate_output(text1)
    print("\nEvaluating second output...")
    scores2 = evaluate_output(text2)
    
    results = {
        "output_1": scores1,
        "output_2": scores2
    }
    
    output_file = os.path.join(output_folder, 'evaluation_results.json')
    save_to_json(results, output_file)
    
    print(f"Evaluation results saved to {output_file}")

if __name__ == "__main__":
    main()
