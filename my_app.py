

from flask import Flask, Response, render_template, request, jsonify
from werkzeug.exceptions import RequestEntityTooLarge



# Local Python Imports
from python_scripts import ph
from services.upload_service import process_csv
from exceptions import UploadValidationError




app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024



# Home page route
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

    # process file
    result = process_csv(file)

    return jsonify({
    "success": True,
    **result
    })

    



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