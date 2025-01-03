#### Readme writed by: ChatGPT-4o

___


# AWS Signed Request for S3 API

This Python project demonstrates how to make an authenticated AWS request using the AWS Signature Version 4 (SigV4) method. The script interacts with the AWS S3 service to list the contents of a bucket.

## Prerequisites

Before running the script, ensure you have the following:

- **Python 3.x** installed on your system.
- **AWS Access Key ID** and **AWS Secret Access Key**.
- **AWS Session Token** if you're using temporary credentials.
- **AWS Region** where your resources are hosted.

## Setup

1. **Install Dependencies**:
   You need to install the required Python packages. You can do so by running the following command:

   ```bash
   pip install requests python-dotenv
   ```

2. **Create a `.env` File**:
   In the project directory, create a `.env` file and populate it with the following AWS credentials:

   ```env
   AWS_REGION=your-aws-region
   AWS_ACCESS_KEY_ID=your-access-key-id
   AWS_SECRET_ACCESS_KEY=your-secret-access-key
   AWS_SESSION_TOKEN=your-session-token
   ```

   Replace `your-aws-region`, `your-access-key-id`, `your-secret-access-key`, and `your-session-token` with your actual AWS credentials. The session token is required if you're using temporary credentials, such as from an IAM role.

## Script Overview

The script performs the following tasks:

1. **Environment Variable Loading**:
   The script uses the `python-dotenv` library to load AWS credentials and region information from a `.env` file.

2. **Generating the AWS SigV4 Signature**:
   It constructs the AWS Signature Version 4 by performing the following steps:
   - Creating a canonical request
   - Creating a string to sign
   - Signing the string using HMAC with your secret access key
   - Building the final request with the signature

3. **Making the Request**:
   The script then constructs an HTTP request to AWS S3, including the necessary headers and signed URL, and sends a GET request to list the contents of an S3 bucket.

## Running the Script

To run the script, simply execute it in your terminal:

```bash
python main.py
```

The script will output the signed request URL and headers, and display the response from AWS, including the status code and body of the response.

### Example Output

```text
***** AWS Signed Request *****
Request URL: https://s3.amazonaws.com/? 
Headers: {
    'x-amz-date': '20250102T100000Z',
    'x-amz-security-token': 'your-session-token',
    'x-amz-content-sha256': 'hashed-payload',
    'Authorization': 'AWS4-HMAC-SHA256 Credential=your-access-key-id/20250102/your-region/s3/aws4_request, SignedHeaders=host;x-amz-date;x-amz-security-token, Signature=calculated-signature'
}

***** AWS Response *****
statusCode 200
{"Contents": [...] }
```

## Notes

- Ensure your AWS credentials have sufficient permissions to list the contents of S3 buckets.
- The script uses a temporary AWS session token, so if your session expires, you will need to refresh the credentials.

## Troubleshooting

- **Invalid credentials**: If you encounter issues with authentication, ensure your AWS credentials are correctly set in the `.env` file and are valid.
- **Permissions issues**: Verify your AWS IAM user or role has the necessary permissions to access the resources you're querying.
- **Connection issues**: Ensure your network connection is stable, and AWS endpoints are accessible from your environment.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
