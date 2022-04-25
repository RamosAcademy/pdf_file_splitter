import os
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
from pdfminer.high_level import extract_text

"""JOSH CHEAT SHEET"""
name_of_pdf = 'Autostack 03.22.pdf'
search_string = 'INV4'
# search_string = 'ABTL'
""""""

path = os.path.join(os.getcwd(), 'Output')
path2 = os.path.join(os.getcwd(), 'Output/Processed')
os.mkdir(path)
os.mkdir(path2)

pdf_file_path = name_of_pdf
file_base_name = pdf_file_path.replace('.pdf', '')

output_folder_path = os.path.join(os.getcwd(), 'Output')

pdf = PdfFileReader(pdf_file_path)

for page_num in range(pdf.numPages):
    pdfWriter = PdfFileWriter()
    pdfWriter.addPage(pdf.getPage(page_num))

    with open(os.path.join(output_folder_path, f'{page_num}.pdf'), 'wb') as f:
        pdfWriter.write(f)
        f.close()

dir_list = os.listdir(path)
num_of_files = len(dir_list) - 1
for invoice in range(num_of_files):
    current_file = f"{path}/{invoice}.pdf"
    text = extract_text(current_file)

    invoice_num = str(text[text.find(search_string):text.find(search_string) + 11]).strip()
    pdf = PdfFileReader(current_file)
    if text.find('1 of 1') != -1:
        pdfWriter = PdfFileWriter()
        pdfWriter.addPage(pdf.getPage(0))
        with open(f"{path}/Processed/{invoice_num}.pdf", 'wb') as f:
            pdfWriter.write(f)
            f.close()
    elif text.find('1 of ') != -1:
        pdf_merger = PdfFileMerger()
        index = text.find('1 of ')
        num_of_docs = int(text[index + 5])
        for i in range(num_of_docs):
            paths = f"{path}/{invoice + i}.pdf"
            pdf_merger.append(PdfFileReader(paths, strict=False))
        pdf_merger.write(f"{path}/Processed/{invoice_num}.pdf")
        pdf_merger.close()
