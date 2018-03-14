import os
import re

path = r"C:\Users\Артем\Documents\dms"
dirs = os.listdir(path)
rtf_pattern = re.compile(r".*\.rtf$")
odt_pattern = re.compile(r".*\.odt$")
pdf_pattern = re.compile(r".*\.pdf$")
docx_pattern = re.compile(r".*\.docx$")
doc_pattern = re.compile(r".*\.doc$")
dotx_pattern = re.compile(r".*\.dotx$")

for dir in dirs:
    files = os.listdir(path + "\\" + dir)
    for i in range(len(files)):
        if rtf_pattern.match(files[i]) is not None:
            os.rename(path + '\\' + dir + '\\' + files[i], path + '\\' + dir + '\\' + "{0}.rtf".format(i))
        if odt_pattern.match(files[i]) is not None:
            os.rename(path + '\\' + dir + '\\' + files[i], path + '\\' + dir + '\\' + "{0}.odt".format(i))
        if pdf_pattern.match(files[i]) is not None:
            os.rename(path + '\\' + dir + '\\' + files[i], path + '\\' + dir + '\\' + "{0}.pdf".format(i))
        if docx_pattern.match(files[i]) is not None:
            os.rename(path + '\\' + dir + '\\' + files[i], path + '\\' + dir + '\\' + "{0}.docx".format(i))
        if doc_pattern.match(files[i]) is not None:
            os.rename(path + '\\' + dir + '\\' + files[i], path + '\\' + dir + '\\' + "{0}.doc".format(i))
        if dotx_pattern.match(files[i]) is not None:
            os.rename(path + '\\' + dir + '\\' + files[i], path + '\\' + dir + '\\' + "{0}.dotx".format(i))

print("done!")
            
