

from flask import Flask, Response, render_template, request, jsonify

# import pandas as pd
# import numpy as np

# import io
# import csv
# import magic


# Python Scripts Imports
from python_scripts import ph
from services.upload_service import process_csv
from exceptions import UploadValidationError

from werkzeug.exceptions import RequestEntityTooLarge


app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024



# Render page
@app.route("/", methods=['GET',"POST"])
def home():
    
    return render_template('index.html')





# Upload file Route
@app.route("/upload", methods=["POST"])
def upload():

    print("Uploading...")
    

    if "file" not in request.files:
        raise UploadValidationError(
                "No file uploaded"
        )


    file = request.files["file"]

    # validate_csv_upload(file)
    rows = process_csv(file)

        # raw = file.stream.read()

        # if not raw:
        #     raise UploadValidationError(
        #     "Empty file"
        #         )

        # text = raw.decode("utf-8")

        # reader = csv.reader(io.StringIO(text))

        # rows = []

        # for row_num, row in enumerate(reader):

        #     if row_num > 10000:
        #         raise UploadValidationError(
        #             "Too many rows"
        #         )

        #     if len(row) > 100:
        #         raise UploadValidationError(
        #             "Too many columns"
        #         )

        #     clean_row = []

        #     for cell in row:

        #         if len(cell) > 1000:
        #             raise UploadValidationError(
        #                 "Cell too large"
        #             )

        #         if dangerous_cell(cell):
        #             raise UploadValidationError(
        #                 "Formula cells are not allowed"
        #             )

        #         clean_row.append(cell)

        #     rows.append(clean_row)

    return jsonify({
        "success": True,
        "rows": len(rows)
    })

    # except UploadValidationError as e:

    #     return jsonify({
    #         "success": False,
    #         "error": str(e)
    #     }), 400

    # except Exception:

    #     # Log actual exception internally
    #     app.logger.exception("Upload failed")

    #     # Generic message to user
    #     return jsonify({
    #         "success": False,
    #         "error": "Upload processing failed"
    #     }), 500



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



##########################################
#  Error Handlers
##########################################
@app.errorhandler(UploadValidationError)
def handle_upload_validation_error(e):

    return jsonify({
        "success": False,
        "error": str(e)
    }), 400


@app.errorhandler(RequestEntityTooLarge)
def handle_large_file(e):

    return jsonify({
        "success": False,
        "error": "File exceeds 5MB limit"
    }), 413

@app.errorhandler(Exception)
def handle_general_exception(e):

    app.logger.exception("Unhandled exception")

    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500
    

# Initiating the application
if __name__ == '__main__':
    # Running the application and leaving the debug mode ON
    app.run(debug=True)