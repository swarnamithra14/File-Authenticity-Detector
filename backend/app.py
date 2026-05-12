from flask import Flask, render_template, request, send_file
import os
import subprocess
import mimetypes

from utils import generate_sha256
from metadata import extract_metadata
from hidden_detector import detect_hidden_content
from scorer import calculate_score
from report_generator import generate_report
from spam_detector import analyze_spam

app = Flask(__name__, template_folder='../templates')

UPLOAD_FOLDER = '../uploads'
ASSEMBLY_PATH = '../assembly/detector.exe'
SPAM_ASM_PATH = '../assembly/spam_detector.exe'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# 🔹 HOME
@app.route('/')
def home():
    return render_template('index.html')


# 🔹 PAGES
@app.route('/spam')
def spam_page():
    return render_template('spam.html')


@app.route('/file')
def file_page():
    return render_template('upload.html')


# 🔥 SPAM ANALYSIS (ASM + PYTHON)
@app.route('/analyze_spam', methods=['POST'])
def analyze_spam_route():

    text = request.form.get('text', '').strip()
    filepath = None

    # 📄 If file uploaded
    if 'file' in request.files and request.files['file'].filename != '':
        file = request.files['file']
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Read file content for Python
        try:
            with open(filepath, 'r', errors='ignore') as f:
                text = f.read()
        except:
            text = ""

    # ❌ No input
    if not text:
        return render_template(
            'spam.html',
            result="No input provided",
            score=0,
            keywords=[],
            asm_result="Not executed"
        )

    # 🧠 PYTHON ANALYSIS
    result_py, score, keywords = analyze_spam(text)

    # ⚙️ ASM ANALYSIS
    asm_result = "Not executed"

    if filepath:
        try:
            result = subprocess.run(
                [SPAM_ASM_PATH, filepath],
                capture_output=True,
                text=True
            )
            asm_result = result.stdout.strip()
        except Exception as e:
            asm_result = "ASM Error"

    # 🔥 COMBINE RESULTS
    if "SPAM" in asm_result:
        score = min(score + 10, 100)

    return render_template(
        'spam.html',
        result=result_py,
        score=score,
        keywords=keywords,
        asm_result=asm_result
    )


# 🔥 FILE AUTHENTICITY MODULE
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file uploaded"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    hash_value = generate_sha256(filepath)

    mime_type, _ = mimetypes.guess_type(filepath)
    if mime_type is None:
        mime_type = "Unknown"

    try:
        result = subprocess.run(
            [ASSEMBLY_PATH, filepath],
            capture_output=True,
            text=True
        )

        output = result.stdout.strip()

        file_ext = os.path.splitext(file.filename)[1].lower()

        ext_map = {
            ".pdf": "PDF",
            ".jpg": "JPG",
            ".jpeg": "JPG",
            ".png": "PNG",
            ".docx": "DOCX"
        }

        expected = ext_map.get(file_ext, "Unknown")

        if "PDF" in output:
            actual = "PDF"
        elif "JPG" in output:
            actual = "JPG"
        elif "PNG" in output:
            actual = "PNG"
        elif "DOCX" in output:
            actual = "DOCX"
        else:
            actual = "Unknown"

        metadata = extract_metadata(filepath, actual)
        hidden_result = detect_hidden_content(filepath)

        score, reasons = calculate_score(expected, actual, mime_type, metadata, hidden_result)

        if expected != actual:
            final_result = f"""⚠️ Suspicious File!
Extension: {expected}
Actual Type: {actual}"""
        else:
            final_result = f"""✅ File is authentic
Type: {actual}"""

    except Exception as e:
        final_result = f"Error running assembly: {str(e)}"
        metadata = {"Error": "Metadata extraction failed"}
        hidden_result = "Error"
        score = 0
        reasons = ["Processing error"]

    global last_report_data
    last_report_data = {
        "name": file.filename,
        "result": final_result,
        "hash": hash_value,
        "mime": mime_type,
        "score": score,
        "reasons": reasons,
        "metadata": metadata,
        "hidden": hidden_result
    }

    return render_template(
        'result.html',
        result=final_result,
        hash_value=hash_value,
        mime_type=mime_type,
        metadata=metadata,
        hidden_result=hidden_result,
        score=score,
        reasons=reasons
    )


# 🔥 DOWNLOAD REPORT
@app.route('/download_report')
def download_report():
    filepath = generate_report(last_report_data)
    return send_file(filepath, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)