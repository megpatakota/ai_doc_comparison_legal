from jinja2 import Environment, FileSystemLoader
from litellm import completion

from .file_io import load_from_json, load_sections, load_txt, write_text_to_file


def compare_sections():

    standard_sections = load_from_json("data/output/standardized_sections.json")

    doc_a_id = standard_sections["sections"][0]["doc_a_section"]["doc_id"]
    doc_a = load_txt(f"data/temp/v{doc_a_id}.txt")

    if doc_a_id == "1":
        doc_b_id = "2"
    else:
        doc_b_id = "1"

    doc_b = load_txt(f"data/temp/v{doc_b_id}.txt")

    doc_a_lines = [line.strip() for line in doc_a.split("</line_id>")]
    doc_b_lines = [line.strip() for line in doc_b.split("</line_id>")]

    comparisons = []

    for section in standard_sections["sections"]:
        doc_a_section = section["doc_a_section"]
        doc_a_content = "\n".join(
            doc_a_lines[
                int(doc_a_section["start_id"]) : int(doc_a_section["end_id"]) + 1
            ]
        )

        doc_b_content_list = []
        for doc_b_section in section["doc_b_sections"]:
            content = f"{doc_b_section['title']}\n"
            content += "\n".join(
                doc_b_lines[
                    int(doc_b_section["start_id"]) : int(doc_b_section["end_id"]) + 1
                ]
            )
            doc_b_content_list.append(content)
        doc_b_content = "\n".join(doc_b_content_list)

        comparisons.append(
            {
                "standardised_title": section["standardised_title"],
                "doc_a_content": doc_a_content,
                "doc_b_content": doc_b_content,
            }
        )
    print(comparisons[0])

    mapped_doc_b_sections = [
        doc_b_section["title"]
        for mapping in standard_sections["sections"]
        for doc_b_section in mapping["doc_b_sections"]
    ]

    doc_b_sections = load_sections(f"data/output/v{doc_b_id}_sections.json")

    unmapped_sections = [
        doc_b_section
        for doc_b_section in doc_b_sections
        if doc_b_section.title not in mapped_doc_b_sections
    ]

    unmapped_sections_text = ""
    for section in unmapped_sections:
        unmapped_sections_text += f"{section.title}\n"
        unmapped_sections_text += "\n".join(
            doc_b_lines[int(section.start_id) : int(section.end_id) + 1]
        )
        unmapped_sections_text += "\n\n"

    env = Environment(loader=FileSystemLoader("templates"))
    compare_template = env.get_template("compare.j2")
    compare_template = compare_template.render(
        doc_a_file_name=f"v{doc_a_id}.docx",
        doc_b_file_name=f"v{doc_b_id}.docx",
        comparisons=comparisons,
        unmapped_sections_text=unmapped_sections_text,
    )
    response = completion(
        model="gpt-4o-mini",
        temperature=1,  # Adjust the temperature to control the randomness of the output
        messages=[{"role": "user", "content": compare_template}],
        # response_format=StandardizedSections,
    )

    response = response.choices[0].message["content"]
    write_text_to_file(response, "data/output/compare_output_pipeline1.txt")
    return response
