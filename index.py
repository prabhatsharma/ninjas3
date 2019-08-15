import json
import urllib.parse
import boto3
import re

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    file_begin = key.rfind('/')
    filename = key[file_begin + 1:]
    
    if verify_file_for_malware(filename):
      print("delete/quarantine file")
      quarantine_file(bucket, key, filename, bucket)
      # delete_file(bucket, key)
    else:
      print("All good. Doing nothing")
      

# verify of the file is a malware
def verify_file_for_malware(filename):
  x = re.search("malware", filename)
  if (x):
    return True
  else:
    return False

def quarantine_file(source_bucket, key, filename, quarantine_bucket):
  copy_source = {'Bucket': source_bucket, 'Key': key}
  
  # Copy the file to quarantine bucket
  s3.copy_object(CopySource = copy_source, Bucket = quarantine_bucket, Key = "testrmm/quarantine/" + filename)
  
  #delete the original uploaded file
  s3.delete_object(Bucket = source_bucket, Key = key)

  return 0

def delete_file(bucket, key):
  # Delete the file
  response = s3.delete_object(Bucket=bucket, Key=key)
  return response

