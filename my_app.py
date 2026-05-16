

from flask import Flask, Response, render_template,request
from flask import Flask, request, jsonify

import numpy as np
import io


# Python Scripts Imports
from python_scripts import ph

app = Flask(__name__)

# Render page
@app.route("/", methods=['GET',"POST"])
def home():
    
    return render_template('index.html')

# Analyze and Sanitize
@app.route("/analyze", methods=["POST"])
def analyze():

    print("running...")

    csv_text = request.data.decode("utf-8")
    print(csv_text)

    data = np.loadtxt(
        io.StringIO(csv_text),
        delimiter=","
    )

    print(data.shape)
    rows = len(data)
    print(rows)
    print(data)

    image_buffer = ph.ph_diagram (data)

    return Response (
        image_buffer.getvalue(),
        mimetype="image/png"
    )

    
# Compute Persisyent Homology
# Returns Persistence Diagram
@app.route("/compute", methods=["POST"])
def compute():
    return None


    

# Initiating the application
if __name__ == '__main__':
    # Running the application and leaving the debug mode ON
    app.run(debug=True)