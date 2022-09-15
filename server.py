from flask import Flask, escape, render_template, request, redirect
from werkzeug.utils import secure_filename
import PyPDF2
import subprocess
import os
import random

app = Flask(__name__)

def pdf_check(file):
    try:
        pdf = PyPDF2.PdfFileReader(open(file, "rb"))
    except:
        return False
    else:
        return True

def size_check(file):
    pdf = PyPDF2.PdfFileReader(open(file, "rb"))
    print(pdf.getDocumentInfo())
    ptSqr = pdf.getPage(0).mediaBox[2] * pdf.getPage(0).mediaBox[3]
    if ptSqr > 400000:
        print("A4  " + str(ptSqr))
        return "A4", ptSqr
    elif ptSqr < 150000:
        print("Label  " + str(ptSqr))
        return "label", ptSqr
    else:
        print("Unknown paper size")
        return "unknown", ptSqr

def label_print(file):
    print("calling lpr command")
    return subprocess.call(["lp", "-o" "fit-to-page", file])

@app.route('/')
def root():
    return redirect("/upload", code=302)

@app.route('/upload')
def upload_page():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        file = "uploads/" + secure_filename(f.filename)
        f.save(file)
        if pdf_check(file):
            (printSize, actualPrintSize) = size_check(file)
            if printSize == "A4":
                label_print(file)
                return redirect("/upload", code=302)
            return "great pdf but size is not A4"
        else:
            return "file is not a usable pdf"
    else:
        return redirect("/upload", code=302)

@app.route('/printrandom')
def print_random():
    try:
        pdfFiles = [x for x in os.listdir('files') if ".pdf" in x.lower()]
        if(len(pdfFiles) <= 0):
            return dict(Message='No PDF files found, please add some pdf files'), 500
        file = random.choice(pdfFiles)
        print('selected %s to print' % file)
        return dict(Message='No Op', File=file), 500
        if pdf_check(file):
            (printSize, actualPrintSize) = size_check(file)
            if printSize == "A4":
                printReturnCode = label_print(file)
                return dict(Message=str(printReturnCode)), 200 
            return dict(Message="great pdf but size is not A4 (size is %s)" % 
                    actualPrintSize, CanvasPrintSize=actualPrintSize), 400
        else:
            return dict(Message="file is not a usable pdf"),400
    except Exception as ex:
        print('Exception: %s' % str(ex))
        return dict(Message='Exception thrown while trying to print a random file', 
                Exception=str(ex))
