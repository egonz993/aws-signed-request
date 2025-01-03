import os
import datetime
import hashlib
import hmac
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
aws_region = os.getenv("AWS_REGION")
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_session_token = os.getenv("AWS_SESSION_TOKEN")

# Get current time in required formats
t = datetime.datetime.now(datetime.timezone.utc)
amz_date = t.strftime('%Y%m%dT%H%M%SZ')
date_stamp = t.strftime('%Y%m%d')


# Create a signed AWS API request
# Documentation: https://docs.aws.amazon.com/general/latest/gr/sigv4-create-canonical-request.html
def signed_request(method, aws_service, host, endpoint, request_parameters, payload=''):

    # 1. Canonical Request
    signed_headers = 'host;x-amz-date;x-amz-security-token'
    canonical_headers = f'host:{host}\n' + f'x-amz-date:{amz_date}\n' + f'x-amz-security-token:{aws_session_token}\n'
    payload_hash = hashlib.sha256((payload).encode('utf-8')).hexdigest()
    canonical_request = (
        f"{method}\n"               # HTTP Verb
        f"{endpoint}\n"             # Canonical URI
        f"{request_parameters}\n"   # Canonical Query String
        f"{canonical_headers}\n"    # Canonical Headers
        f"{signed_headers}\n"       # Signed Headers
        f"{payload_hash}"           # Hashed Payload
    )

    # 2. String to Sign
    credential_scope = f"{date_stamp}/{aws_region}/{aws_service}/aws4_request"
    algorithm = 'AWS4-HMAC-SHA256'
    string_to_sign = (
        f"{algorithm}\n"            # Algorithm
        f"{amz_date}\n"             # Timestamp
        f"{credential_scope}\n"     # Scope
        f"{hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()}"      # HEX(SHA256Hash(CanonicalRequest))
    )

    # 3. Signing Key
    def HMAC_SHA256(key, msg):
        return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

    date_key = HMAC_SHA256(('AWS4' + aws_secret_access_key).encode('utf-8'), date_stamp)
    date_region_key = HMAC_SHA256(date_key, aws_region)
    date_region_service_key = HMAC_SHA256(date_region_key, aws_service)
    signing_key = HMAC_SHA256(date_region_service_key, 'aws4_request')

    # 4. Signature
    signature = HMAC_SHA256(signing_key, string_to_sign).hex()

    # Build the request
    request_url = f"https://{host}{endpoint}?{request_parameters}"
    headers = {
        'x-amz-date': amz_date,
        'x-amz-security-token': aws_session_token,
        'x-amz-content-sha256': payload_hash,
        'Authorization': (
            f"{algorithm} "
            f"Credential={aws_access_key_id}/{credential_scope}, "
            f"SignedHeaders={signed_headers}, "
            f"Signature={signature}"
        )
    }

    print("\n\n***** AWS Signed Request *****")
    print(f"Request URL: {request_url}")
    print(f"Headers: {headers}")

    # Make the HTTP Signed Request to AWS and return the response
    response = requests.get(request_url, headers=headers)
    return response


# aws s3 ls
response = signed_request(
    method = 'GET',
    aws_service = 's3',
    host = 's3.amazonaws.com',
    endpoint = '/',
    request_parameters = ''
)

print("\n\n***** AWS Response *****")
print("statusCode", response.status_code)
print(response.text)