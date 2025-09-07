import os
import re
import PyPDF2
import shutil
from pathlib import Path

def convert_pdf_to_txt(pdf_path, txt_path):
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n\n"
            with open(txt_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(text)
            return True
    except:
        return False

def search(s, build_folder="build"):
    r = []
    for root, _, files in os.walk(build_folder):
        for f in files:
            if f.endswith('.txt'):
                try:
                    pdf_name = f.replace('.txt', '.pdf')
                    with open(os.path.join(root, f), 'r', encoding='utf-8') as file:
                        content = file.read().lower()
                        words = re.findall(r'\w+', content)
                        if any((s in w or w in s or abs(len(w)-len(s))<=2) and (w[:3]==s[:3] if min(len(w),len(s))>=3 else w==s) for w in words):
                            r.append(pdf_name)
                except:
                    continue
    return r

build_folder = "build"
pdf_folder = "pdf"

os.makedirs(pdf_folder, exist_ok=True)
os.makedirs(build_folder, exist_ok=True)

for pdf_file in Path(pdf_folder).glob("*.pdf"):
    txt_file = os.path.join(build_folder, f"{pdf_file.stem}.txt")
    if not os.path.exists(txt_file):
        convert_pdf_to_txt(pdf_file, txt_file)

while True:
    if (i := input(">>> ").strip().lower()) in ['exit','выход','quit','q']:
        break
    results = search(i)
    print('\n'.join(results) if results else "Файлы не найдены")

shutil.rmtree(build_folder)