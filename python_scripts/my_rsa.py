
# Imports
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import base64
from flask import jsonify



# Generate Keys
def genKeys(bitEnc):

    # ===============================
    # 1️⃣ Generate RSA Key Pair
    # ===============================

    # Grab bitEnc and cast to int
    key_size = int(bitEnc)
    # Generate a private key
    private_key = rsa.generate_private_key(
    public_exponent=65537,  # Commonly used public exponent; safe and efficient
    key_size=key_size           # Key length in bits (2048 is standard secure size; can use 3072 or 4096 for higher security)
    )

    # Grab private numbers
    private_numbers = private_key.private_numbers()

    # Grab public numbers
    # public_numbers = public_key.public_numbers()

    # Public exponent
    e = private_numbers.public_numbers.e

    # Private exponent
    d = private_numbers.d

    # Prime factors an modulus
    p = private_numbers.p
    q = private_numbers.q
    n = private_numbers.public_numbers.n





    # Derive the public key from the private key
    public_key = private_key.public_key()

    # Save PRIVATE key to PEM file (unencrypted)
    pem_private = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,                   # Output format: PEM (Base64 + headers)
    format=serialization.PrivateFormat.PKCS8,              # Standard private key format
    encryption_algorithm=serialization.NoEncryption()      # Use BestAvailableEncryption(b"password") to encrypt
    ).decode("utf-8")  # 👈 critical line

    # Save PUBLIC key to PEM file
    pem_public = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,                   # PEM format again
    format=serialization.PublicFormat.SubjectPublicKeyInfo # Standard public key structure
    ).decode("utf-8")  # 👈 critical line


    formatted = format_rsa_components(p, q, n, e, d)
    # print(public_key)
    # print(private_key)
    # print(pem_public)
    # print(pem_private)
    # files = jsonify({
    #     "PUBLICKEY": pem_public,
    #     "PRIVATEKEY": pem_private
    # })

    # return {
    #     "PRIVATEKEY": pem_private,
    #     "PUBLICKEY": pem_public
    # }

    return jsonify({
        "PRIVATEKEY": pem_private,
        "PUBLICKEY": pem_public,
        "parameters": formatted
        # "p": str(p),
        # "q": str(q),
        # "n": str(n),
        # "d" :str(d),
        # "e": str(e)
        

    })

   

# Encrypt Message
def enc(publicKey,plainText):

    # Temp -Create "encrypted" text file
    # To do - connect to module
    # enc_text = f"🌍 Encrypted Stuff — public key: {publicKey} plain text: {plainText}"
    # private_text = f"🚀 PRIVATE — you sent: {bitEnc}"

    # file = jsonify({
    #     "encrypted_text": enc_text
    # })


    # return file

    # ===============================
    # Encrypt a message with the PUBLIC key
    # ===============================

    # Convert plainText to binary
    message = plainText.encode("utf-8")
    
    # Convert publicKey to binary
    pem_public_bytes = publicKey.encode("utf-8")

    # Load public_key
    public_key = serialization.load_pem_public_key(pem_public_bytes)

    # Encrypt
    ciphertext = public_key.encrypt(
        message,
        padding.OAEP(                                    # OAEP = Optimal Asymmetric Encryption Padding
            mgf=padding.MGF1(algorithm=hashes.SHA256()), # MGF1 = Mask Generation Function, using SHA-256 hash
            algorithm=hashes.SHA256(),                   # Hash used inside OAEP
            label=None                                   # Optional label (rarely used, keep None)
        )
    )

    # Decode binary to base 64 ( to enable serilization )
    # Return Base64-encoded ciphertext so it can be transmitted in JSON
    ciphertext_b64 = base64.b64encode(ciphertext).decode("utf-8")
   

    return jsonify({
        "encrypted_text": ciphertext_b64
        
    })

# Decrypt Message
def dec(privateKey,cypherText):

    

    # Convert cypherText to binary
    ciphertext = base64.b64decode(cypherText)

    # Convert privateKey to binary
    pem_private_bytes = privateKey.encode("utf-8")

    # Load private_key
    private_key = serialization.load_pem_private_key(
            pem_private_bytes,
            password=None,   # supply bytes here if key is encrypted with a password
        )
    
    # Decrypt
    plaintext_bytes = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    # Decode bytes to UTF-8 string
    plaintext = plaintext_bytes.decode("utf-8")

    return jsonify({"plaintext": plaintext}), 200

    # Temp -Create "decrypted" text file
    # To do - connect to module
    # dec_text = f"🌍 Decrypted Stuff — private key: {privateKey} cypher text: {cypherText}"
    # private_text = f"🚀 PRIVATE — you sent: {bitEnc}"

    # file = jsonify({
    #     "decrypted_text": dec_text
    # })

    # return file
    


#######################################################################




# ===============================
# 2️⃣ Serialize (Save) Keys to PEM format
# ===============================

# Save PRIVATE key to PEM file (unencrypted)
# pem_private = private_key.private_bytes(
#     encoding=serialization.Encoding.PEM,                   # Output format: PEM (Base64 + headers)
#     format=serialization.PrivateFormat.PKCS8,              # Standard private key format
#     encryption_algorithm=serialization.NoEncryption()      # Use BestAvailableEncryption(b"password") to encrypt
# )
# with open("private_key.pem", "wb") as f:
#     f.write(pem_private)

# # Save PUBLIC key to PEM file
# pem_public = public_key.public_bytes(
#     encoding=serialization.Encoding.PEM,                   # PEM format again
#     format=serialization.PublicFormat.SubjectPublicKeyInfo # Standard public key structure
# )
# with open("public_key.pem", "wb") as f:
#     f.write(pem_public)


# # ===============================
# # 3️⃣ Encrypt a message with the PUBLIC key
# # ===============================

# message = b"My top secret message"

# ciphertext = public_key.encrypt(
#     message,
#     padding.OAEP(                                    # OAEP = Optimal Asymmetric Encryption Padding
#         mgf=padding.MGF1(algorithm=hashes.SHA256()), # MGF1 = Mask Generation Function, using SHA-256 hash
#         algorithm=hashes.SHA256(),                   # Hash used inside OAEP
#         label=None                                   # Optional label (rarely used, keep None)
#     )
# )

# print("Ciphertext:", ciphertext)


# # ===============================
# # 4️⃣ Decrypt the message with the PRIVATE key
# # ===============================

# plaintext = private_key.decrypt(
#     ciphertext,
#     padding.OAEP(
#         mgf=padding.MGF1(algorithm=hashes.SHA256()), # Must match encryption settings
#         algorithm=hashes.SHA256(),
#         label=None
#     )
# )

# print("Decrypted:", plaintext.decode())

# Helper functions to compose contents of parameters
def wrap_text(text, width=64):
    """Wraps a long string into lines of given width."""
    return "\n".join(text[i:i+width] for i in range(0, len(text), width))

def format_rsa_components(p, q, n, e, d, width=64):
    """Formats RSA integers into labeled, wrapped strings."""
    components = {
        "p": str(p),
        "q": str(q),
        "n": str(n),
        "e": str(e),
        "d": str(d)
    }

    lines = []
    for label, value in components.items():
        wrapped = wrap_text(value, width)
        lines.append(f"{label} = {wrapped}")
    return "\n\n".join(lines)



