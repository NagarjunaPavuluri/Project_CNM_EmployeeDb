
import boto3
import json
import os
# create S3 bucket instance
s3 = boto3.client('s3')
bucket_name = 'nag-pratap'
s3.create_bucket(Bucket=bucket_name)
# define the policy
bucket_policy = {
     'Version': '2012-10-17',
     'Statement': [{
         'Sid': 'permission_statement',
         'Effect': 'Allow',
         'Principal': '*',
         'Action': ['s3:GetObject'],
         'Resource': "arn:aws:s3:::%s/*" % bucket_name
      }]
 }
bucket_policy = json.dumps(bucket_policy)
s3.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)

#create a website
s3.put_bucket_website(
     Bucket=bucket_name,
     WebsiteConfiguration={
     'ErrorDocument': {'Key': 'index.html'},
     'IndexDocument': {'Suffix': 'app.py'},
    }
 )

'''filename = ['app.py']
# read the index and error files from the folder
for file in filename:
         s3.upload_file(file, bucket_name,file, ExtraArgs={'ContentType': 'text/html'}) '''  
local_directory = 'C:\\Users\\rajya\\Desktop\\CNM_Project_Employee_DB\\templates\\CNM_Project_Employee_DB\\'
bucket_directory = 'CNM_Project_Employee_DB/'

for root, dirs, files in os.walk(local_directory):
    for filename in files:
        # construct the full local path
        local_path = os.path.join(root, filename)
        # construct the full S3 path
        relative_path = os.path.relpath(local_path, local_directory)
        s3_path = os.path.join(bucket_directory, relative_path)
        # upload the file
        s3.upload_file(local_path, bucket_name, s3_path)

#http://typical-static-website.s3-website-us-east-1.amazonaws.com

endpoint = "http://"+bucket_name+".s3-website-"+s3.meta.region_name+".amazonaws.com" 
print(endpoint)    
         
         