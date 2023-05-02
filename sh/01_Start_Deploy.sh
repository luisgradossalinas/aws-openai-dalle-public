#!/bin/bash

ACCOUNT_ID=`aws sts get-caller-identity --query Account --output text`
PROJECT="dalle"

aws s3 mb s3://${PROJECT}-code-${ACCOUNT_ID}

sleep 5

aws s3 cp lambda/awsdalle.zip s3://${PROJECT}-code-${ACCOUNT_ID}/lambda/

pip3 install -r web/requirements.txt

aws cloudformation create-stack --stack-name StackDalle --template-body file://dalle.yaml --capabilities CAPABILITY_NAMED_IAM
