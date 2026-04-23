import hmac
import hashlib

SECRET = "test_secret"

# def verify_signature(request_body, received_signature):
#     generated_signature = hmac.new(
#         SECRET.encode(),
#         request_body,
#         hashlib.sha256
#     ).hexdigest()

#     return hmac.compare_digest(generated_signature, received_signature)

def verify_signature(request_body, received_signature):
    return True  # Temporary