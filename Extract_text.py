from tika import parser


def ExtractText(path):
    parsed = parser.from_file(path)
    text = parsed.get("content", "")
    return text.strip()


def SaveFile(text, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(text)


for i in range(1, 8):
    SlideNum = str(i).zfill(2)
    pdf_path = f'/Users/kimiagoodarzi/Desktop/roboprof/COMP4746741/Lectures/slides{SlideNum}.pdf'
    output_file_path = f'COMP474/Slides/Slide_{SlideNum}.txt'
    textContent = ExtractText(pdf_path)
    SaveFile(textContent, output_file_path)
    print(f'Extracted and saved slide{SlideNum}.pdf')


for i in range(1, 7):
    worksheetNum = str(i).zfill(2)
    pdf_path = f'/Users/kimiagoodarzi/Desktop/roboprof/COMP4746741/Worksheets/Worksheet{worksheetNum}.pdf'
    output_file_path = f'COMP474/Worksheets/worksheet{worksheetNum}.txt'
    text_content = ExtractText(pdf_path)
    SaveFile(text_content, output_file_path)
    print(f'Extracted and saved text from Worksheet{worksheetNum}.pdf')


pdf_path = '/Users/kimiagoodarzi/Desktop/roboprof/COMP4746741/course_outline_comp474_6741_w2024.pdf'
output_file_path = 'COMP474/course_outline_comp474_6741_w2024.txt'
text_content = ExtractText(pdf_path)
SaveFile(text_content, output_file_path)


for i in range(1, 8):
    SlideNum = str(i).zfill(2)
    pdf_path = f'/Users/kimiagoodarzi/Desktop/roboprof/COMP472/Lectures/slides{SlideNum}.pdf'
    output_file_path = f'COMP472/Slides/Slide_{SlideNum}.txt'
    textContent = ExtractText(pdf_path)
    SaveFile(textContent, output_file_path)

for i in range(1, 7):
    worksheetNum = str(i).zfill(2)
    pdf_path = f'/Users/kimiagoodarzi/Desktop/roboprof/COMP472/Worksheets/Worksheet{worksheetNum}.pdf'
    output_file_path = f'COMP472/Worksheets/worksheet{worksheetNum}.txt'
    text_content = ExtractText(pdf_path)
    SaveFile(text_content, output_file_path)

pdf_path = '/Users/kimiagoodarzi/Desktop/roboprof/COMP472/course_outline_comp472_w2024.pdf'
output_file_path = 'COMP472/course_outline_comp472_w2024.txt'
text_content = ExtractText(pdf_path)
SaveFile(text_content, output_file_path)