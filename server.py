from flask import Flask, escape, render_template, request, redirect
from werkzeug.utils import secure_filename
import PyPDF2
import subprocess

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
        return "A4"
    elif ptSqr < 150000:
        print("Label  " + str(ptSqr))
        return "label"
    else:
        print("Unknown paper size")
        return "unknown"

def label_print(file):
    print("calling lpr command")
    subprocess.call(["lp", "-o" "fit-to-page", file])

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
            if size_check(file) == "A4":
                label_print(file)
                return redirect("/upload", code=302)
            return "great pdf but size is not A4"
        else:
            return "file is not a usable pdf"
    else:
        return redirect("/upload", code=302)app.route('/uploader', methods = ['GET', 'POST'])

@app.route('/printrandom')
def print_random():
    file = 'files/random.pdf'
    if pdf_check(file):
        if size_check(file) == "A4":
            label_print(file)
            return redirect("/upload", code=302)
        return "great pdf but size is not A4"
    else:
        return "file is not a usable pdf"
    else:
        return redirect("/upload", code=302)
