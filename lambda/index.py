import os 
import json
import openai
import boto3
import base64
import requests
import uuid
from datetime import datetime
from datetime import timedelta
import time
import urllib.parse

s3 = boto3.client('s3')
session = boto3.session.Session()
secret = session.client(service_name = 'secretsmanager')
dynamo = boto3.resource('dynamodb')

SM_DALLE = os.environ['SM_DALLE']
SM_ULTRAMSG = os.environ['SM_ULTRAMSG']
BUCKET_NAME = os.environ['BUCKET_NAME']
DYNAMO_TABLE = os.environ["DYNAMO_TABLE"]

sm_dalle = secret.get_secret_value(SecretId = SM_DALLE)
data = json.loads(sm_dalle['SecretString'])
api_key = data['api_key']

sm_ultramsg = secret.get_secret_value(SecretId = SM_ULTRAMSG)
data = json.loads(sm_ultramsg['SecretString'])
ultramsg_instancia = data["instance"]
ultramsg_token = data["token"]

openai.api_key = api_key

def lambda_handler(event, context):
    
    s3r = boto3.resource('s3')
    decoded_record_data = [base64.b64decode(record['kinesis']['data']) for record in event['Records']]
    deserialized_data = [json.loads(decoded_record) for decoded_record in decoded_record_data]

    table_dynamo_execution = dynamo.Table(DYNAMO_TABLE)
    with table_dynamo_execution.batch_writer() as batch_writer:
      
        for item in deserialized_data:
    
            p_name = item['name']
            p_cel = item['cel']
            p_msg = item['msg']
            
            print("Kinesis data:")
            print(item)
            
            response = openai.Image.create(
                prompt = p_msg,
                n = 1,
                size = "256x256"
            )
            
            image_url = response['data'][0]['url']
    
            print(image_url)
    
            IMAGE_URL = image_url
            FILE_NAME = str(uuid.uuid4()) + ".jpg"
            
            response = requests.get(image_url)
            s3.put_object(Bucket = BUCKET_NAME, Key = FILE_NAME, Body = response.content, ContentType = 'image/png')
    
            d = datetime.today() - timedelta(hours = 5, minutes = 0) #hora Lima
            date_reg = str(d.strftime("%Y-%m-%d %H:%M:%S"))  

            s3_object = s3r.Object(BUCKET_NAME, FILE_NAME)
            image_content = s3_object.get()['Body'].read()
            
            base64_image = base64.b64encode(image_content)
            img_bas64 = urllib.parse.quote_plus(base64_image)
            
            output_wsp = p_name + ", the image generated from this text is sent to you (" + p_msg + ")."
            
            #replace cel
            p_cel = p_cel.replace("+","")
            
            payload = "token=" + ultramsg_token + "&to=%2B" + p_cel + "&image=" + img_bas64 + "&caption=" + output_wsp
            payload = payload.encode('utf8').decode('iso-8859-1')
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            url = "https://api.ultramsg.com/" + ultramsg_instancia + "/messages/image"
            response = requests.request("POST", url, data = payload, headers = headers)
            
            print(response)
            
            batch_writer.put_item(
              Item = {
                  "id" : str(int(time.time())),
                  "text_input" : p_msg,
                  "cel" : p_cel,
                  "name" : p_name,
                  "url_img" : "s3://" + BUCKET_NAME + "/" + FILE_NAME,
                  "freg" : date_reg
                }
            )

        return {
            'statusCode': 200
        }