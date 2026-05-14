

from flask import Flask, Response, render_template,request
from flask import Flask, request, jsonify

import numpy as np
import io


# Python Scripts Imports
from python_scripts import ph

app = Flask(__name__)

@app.route("/", methods=['GET',"POST"])
def home():
    
    return render_template('index.html')


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

    # return jsonify({
    #     "rows": rows,
    #     "message": "Data received"
    # })
# @app.route('/tropical',methods=['GET',"POST"])
# def tropical():

#     if request.method == 'POST':
       
#         trop_poly = request.form.get('trop_poly')
#         poly_mode = request.form.get('mode')
#         # b = request.form.get('b')
#         print(trop_poly)
#         print(poly_mode)
#         return render_template('tropical.html',text_poly = trop_poly,
#                                mode=poly_mode )
#     return render_template('tropical.html',mode='V')



# @app.route('/ramsey')
# def ramsey():
#     return render_template('ramsey.html') 

# @app.route('/test')
# def test():
#     return render_template('test.html')

# @app.route('/base')
# def base():
#     return render_template('base.html')


# @app.route('/hadamard')
# def hadamard():
#     return render_template('hadamard.html')




# @app.route('/amoeba')
# def amoeba():
#     return render_template('amoeba.html')

#######################################
## RSA
#######################################

# Main RSA page
# @app.route('/rsa',methods=['GET',"POST"])
# def rsa():

#     if request.method == 'POST':

#         # Check/Get header by key='X-action'
#         action = request.headers.get('X-action')
        
#         if action == 'genKeys':

#             # Read Bit Encryption Selection
#             gen_json = request.get_json()
            
#             bitEncryption = gen_json.get('bitencryption')
            
#             # Generate Keys and Return JSON
#             return  my_rsa.genKeys(bitEncryption)

#         if action == 'enc':

#             # Read PUBLIC Key and plaintext
#             enc_json = request.get_json()
            
#             PUBLICKEY = enc_json.get('PUBLICKEY')
#             plainText = enc_json.get('plaintext')

#             # Encrypt and Return JSON
#             return  my_rsa.enc(PUBLICKEY,plainText)



#         if action == 'dec':
            
#             # Read PRIVATE Key and cyphertext
#             dec_json = request.get_json()
            
#             PRIVATEKEY = dec_json.get('PRIVATEKEY')
#             cypherText = dec_json.get('cyphertext')
            
#             # Decrypt and Return JSON
#             return my_rsa.dec(PRIVATEKEY,cypherText)

#         else:
#             return "No valid X-action found.", 400

#     return render_template('rsa.html')

# # Instructions
# @app.route("/rsa/instructions")
# def rsa_instructions():
#     return render_template('rsa_instructions.html')

# # RSA Algorithm
# @app.route("/rsa/algo")
# def rsa_algo():
#     return render_template('rsa_algo.html')

# # Details
# @app.route("/rsa/details")
# def rsa_details():
#     return render_template('rsa_details.html')

# # Disclaimer
# @app.route("/rsa/disclaimer")
# def rsa_disclaimer():
#     return render_template('rsa_disclaimer.html')

# # ERase after testing
# # jinja try




@app.route("/rsa/setecastronomy")
def setecastronomy():
    return render_template('setecastronomy.html')



    

# Initiating the application
if __name__ == '__main__':
    # Running the application and leaving the debug mode ON
    app.run(debug=True)