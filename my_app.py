

from flask import Flask, Response, render_template,request
from flask import Flask, request, jsonify
import pandas as pd

import numpy as np
import io
import csv
import magic


# Python Scripts Imports
from python_scripts import ph

app = Flask(__name__)

class UploadValidationError(Exception):
    pass

# Render page
@app.route("/", methods=['GET',"POST"])
def home():
    
    return render_template('index.html')


# Upload sanitization
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

MAX_ROWS = 10000
MAX_COLS = 100
MAX_CELL_LENGTH = 1000

ALLOWED_MIMES = {
    "text/csv",
    "text/plain",
    "application/csv",
    "application/vnd.ms-excel",
}

def validate_csv_upload(file):

    # Check extension first (cheap check)
    if not file.filename.lower().endswith(".csv"):
        raise UploadValidationError(
            "Only CSV files are allowed"
        )

    # Check actual MIME signature
    header = file.stream.read(2048)
    file.stream.seek(0)

    mime = magic.from_buffer(header, mime=True)

    if mime not in ALLOWED_MIMES:
         raise UploadValidationError(
            "Invalid CSV file"
        )

def dangerous_cell(value):
    return (
        isinstance(value, str)
        and value.startswith(("=", "+", "-", "@"))
    )





# Upload file Route
@app.route("/upload", methods=["POST"])
def upload():

    print("Uploading...")
    try:

        if "file" not in request.files:
            raise UploadValidationError(
                "No file uploaded"
            )


        file = request.files["file"]

        validate_csv_upload(file)

        raw = file.stream.read()

        text = raw.decode("utf-8")

        reader = csv.reader(io.StringIO(text))

        rows = []

        for row_num, row in enumerate(reader):

            if row_num > 10000:
                raise UploadValidationError(
                    "Too many rows"
                )

            if len(row) > 100:
                raise UploadValidationError(
                    "Too many columns"
                )

            clean_row = []

            for cell in row:

                if len(cell) > 1000:
                    raise UploadValidationError(
                        "Cell too large"
                    )

                if dangerous_cell(cell):
                    raise UploadValidationError(
                        "Formula cells are not allowed"
                    )

                clean_row.append(cell)

            rows.append(clean_row)

        return jsonify({
            "success": True,
            "rows": len(rows)
        })

    except UploadValidationError as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

    except Exception:

        # Log actual exception internally
        app.logger.exception("Upload failed")

        # Generic message to user
        return jsonify({
            "success": False,
            "error": "Upload processing failed"
        }), 500



# Analyze and Sanitize
@app.route("/analyze", methods=["POST"])
def analyze():

    print("Analyzing...")

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    

    # return jsonify({
    #     "status": "success",
    #     "rows": len(df),
    #     "cols": len(df.columns),
    #     "columns": list(df.columns)
    # })

    return None

    
# Compute Persisyent Homology
# Returns Persistence Diagram
@app.route("/compute", methods=["POST"])
def compute():
    return None


    

# Initiating the application
if __name__ == '__main__':
    # Running the application and leaving the debug mode ON
    app.run(debug=True)