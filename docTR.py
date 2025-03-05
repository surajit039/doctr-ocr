from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import os, re
import tkinter as tk
from tkinter import filedialog, messagebox


def process_images(filepaths,model):
    for filepath in filepaths:
        filename = os.path.splitext(os.path.basename(filepath))[0]
        image = DocumentFile.from_images(filepath)
        extracted = model(image)
        text_file = open(f"{filename}-extracted.txt", "w")
        for page in extracted.pages:
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
def process_pdfs(filepaths,model):
    for filepath in filepaths:
        filename = os.path.splitext(os.path.basename(filepath))[0]
        pdf = DocumentFile.from_pdf(filepath)
        extracted = model(pdf)
        for i in range(len(extracted.pages)):
            text_file = open(f"{filename}-page{i+1}-extracted.txt", "w")
            page = extracted.pages[i]
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

class FilePickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("docTR by Mindee")
        self.root.geometry("600x300")
        
        self.file_label = tk.Label(root, text="No files selected", wraplength=300)
        self.file_label.pack(pady=10)
        
        self.select_button = tk.Button(root, text="Select Files", command=self.open_file_dialog)
        self.select_button.pack(pady=10)
        
        self.process_button = tk.Button(root, text="Recognise Characters", command=self.process_files)
        self.process_button.pack(pady=10)
        
        self.selected_files = []

    def open_file_dialog(self):
        file_paths = filedialog.askopenfilenames(
            title="Select Files",
            filetypes=(("Image and PDF Files", "*.jpg *.png *.pdf"),)) 
        
        if file_paths:
            self.selected_files = list(file_paths)
            self.file_label.config(text="\n".join(self.selected_files))

    def process_files(self):
        if not self.selected_files:
            messagebox.showwarning("Warning", "No files selected!")
            return
        
        jpg_png_files = [f for f in self.selected_files if f.lower().endswith(('.jpg', '.png'))]
        pdf_files = [f for f in self.selected_files if f.lower().endswith('.pdf')]
        
        if jpg_png_files or pdf_files:
            model = ocr_predictor(pretrained=True)
            if jpg_png_files:
                process_images(jpg_png_files,model)
            if pdf_files:
                process_pdfs(pdf_files,model)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = FilePickerApp(root)
    root.mainloop()
