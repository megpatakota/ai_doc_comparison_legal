from src.process import extract_text_from_docx, batch_text
from src.llm_section_extract import process_batches
from src.io import save_sections

v1 = extract_text_from_docx("data/input/v1.docx")
v2 = extract_text_from_docx("data/input/v2.docx")

v1_batches = batch_text(v1)
v2_batches = batch_text(v2)

all_v1_sections = process_batches(v1_batches)
all_v2_sections = process_batches(v2_batches)

print("All extracted sections from v1_batches:")
for section in all_v1_sections:
    print(section.model_dump())

save_sections(all_v1_sections, 'data/output/v1_sections.json')
save_sections(all_v2_sections, 'data/output/v2_sections.json')