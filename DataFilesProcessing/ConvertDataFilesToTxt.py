import subprocess
import os
import re

path = r"/home/artyom/PycharmProjects/DocumentFlowEfficiency/dms"
dirs = os.listdir(path)
rtf_pattern = re.compile(r".*\.rtf$")
odt_pattern = re.compile(r".*\.odt$")
pdf_pattern = re.compile(r".*\.pdf$")
docx_pattern = re.compile(r".*\.docx$")
doc_pattern = re.compile(r".*\.doc$")
dotx_pattern = re.compile(r".*\.dotx$")

for dir in dirs:
    files = os.listdir(path + "/" + dir)
    for i in range(len(files)):
        t = os.path.join(path, dir, files[i])
        if rtf_pattern.match(files[i]) is not None:
            subprocess.call(["soffice", "--headless", "--convert-to", "txt:Text",
                             os.path.join(path, dir, files[i]), "--outdir",
                             os.path.join(path, dir)])
        if odt_pattern.match(files[i]) is not None:
            subprocess.call(["soffice", "--headless", "--convert-to", "txt:Text",
                             os.path.join(path, dir, files[i]), "--outdir",
                             os.path.join(path, dir)])
        if pdf_pattern.match(files[i]) is not None:
            subprocess.call(["pdftotext", os.path.join(path, dir, files[i]),
                             os.path.join(path, dir, files[i] + ".pdf")])
        if docx_pattern.match(files[i]) is not None:
            subprocess.call(["soffice", "--headless", "--convert-to", "txt:Text",
                             os.path.join(path, dir, files[i]), "--outdir",
                             os.path.join(path, dir)])
        if doc_pattern.match(files[i]) is not None:
            subprocess.call(["soffice", "--headless", "--convert-to", "txt:Text",
                             os.path.join(path, dir, files[i]), "--outdir",
                             os.path.join(path, dir)])
        if dotx_pattern.match(files[i]) is not None:
            subprocess.call(["soffice", "--headless", "--convert-to", "txt:Text",
                             os.path.join(path, dir, files[i]), "--outdir",
                             os.path.join(path, dir)])
print("done!")
