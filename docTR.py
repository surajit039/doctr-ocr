from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import re

model = ocr_predictor(pretrained=True)
image = DocumentFile.from_images("tmp1.jpg")
extracted = model(image)
#print(extracted.pages[0])
for page in extracted.pages:
    text_file = open("extracted.txt", "w")
    for block in page.blocks:
        for line in block.lines:
            word_list = list()
            for word in line.words:
                string = str(word)
                match = re.search(r"value='(.*?)'", string)
                extracted_value = match.group(1)
                text_file.write(f"{extracted_value} ")
            text_file.write("\n")
        text_file.write("\n\n\n")
    text_file.close()

