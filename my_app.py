

from flask import Flask, Response, render_template, request, jsonify
from flask import abort, send_from_directory,send_file
from werkzeug.exceptions import RequestEntityTooLarge
import os


# Local Python Imports
from python_scripts import ph
from services.upload_service import process_csv
from exceptions import UploadValidationError





app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024


##################################
## Dashboard Home page Route    ##
##################################
@app.route("/", methods=['GET',"POST"])
def home():
    
    return render_template('dashboard.html')




##########################
## Upload file Route    ##
##########################
@app.route("/upload", methods=["POST"])
def upload():

    print("Uploading...")

    if "file" not in request.files:
        raise UploadValidationError(
                "No file uploaded"
        )

    file = request.files["file"]

    # process file
    result = process_csv(file)

    return jsonify({
    "success": True,
    **result
    })

 
    

##########################
## Diagrams Route       ##
##########################
# Compute Persisyent Homology
# Returns Persistence Diagram
@app.route("/diagrams", methods=["POST"])
def diagrams():

    print("diagrams")

    file = request.files.get("file")

    if not file:
        return {"error": "No file supplied"}, 400

    # Create plot
    image_bytes = ph.ph_diagram(file)

    return send_file(
        image_bytes,
        mimetype="image/png"
    )






##########################
## Barcodes Route       ##
##########################
@app.route("/barcodes", methods=["POST"])
def barcodes():

    print("barcodes")

    file = request.files.get("file")

    if not file:
        return {"error": "No file supplied"}, 400

    # Create plot
    image_bytes = ph.barcode(file)

    return send_file(
        image_bytes,
        mimetype="image/png"
    )



##################################
# Download example csv's route  ##
##################################
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DOWNLOAD_DIR = os.path.join(BASE_DIR, "csv_files")
ALLOWED_FILES = {"S1.csv", "S2.csv", "S3.csv","S1xS1.csv"}

@app.route("/download/<filename>")
def download(filename):

    if filename not in ALLOWED_FILES:
        abort(404)

    return send_from_directory(
        DOWNLOAD_DIR,
        filename,
        as_attachment=True
    )





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