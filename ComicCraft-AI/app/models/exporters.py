from fpdf import FPDF


def save_pdf(content, file_path="comic_story.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for line in content.split("\n"):
        pdf.multi_cell(0, 10, line)

    pdf.output(file_path)

    return file_path