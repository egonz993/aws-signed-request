# AWS Documentation: https://docs.aws.amazon.com/
signed_request = "function to be implemented"

# aws s3 ls
response = signed_request(
    method = 'GET',
    aws_service = 's3',
    host = 's3.amazonaws.com',
    endpoint = '/',
    request_parameters = ''
)

# aws ec2 describe-instances
response = signed_request(
    method = 'GET',
    service = 'ec2',
    host = 'ec2.amazonaws.com',
    endpoint = '/',
    request_parameters = 'Action=DescribeInstances&Version=2016-11-15'
)

# # aws ec2 describe-vpcs
response = signed_request(
    method = 'GET',
    service = 'ec2',
    host = 'ec2.amazonaws.com',
    endpoint = '/',
    request_parameters = 'Action=DescribeVpcs&Version=2016-11-15'
)

# aws cloudfront list-distributions
response = signed_request(
    method = 'GET',
    service = 'cloudfront',
    host = 'cloudfront.amazonaws.com',
    endpoint = '/2020-05-31/distribution',
    request_parameters = ''
)

# aws lambda list-functions
response = signed_request(
    method = 'GET',
    service = 'lambda',
    host = 'lambda.us-east-1.amazonaws.com',
    endpoint = '/2015-03-31/functions',
    request_parameters = ''
)