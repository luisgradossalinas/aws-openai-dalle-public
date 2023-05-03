from flask import Flask, render_template, request
import boto3
import json
import uuid

app = Flask(__name__)

kinesis = boto3.client("kinesis", region_name = "us-east-1")
stream_name = "StreamDalle"

@app.route('/')
def index():
   return render_template("index.html")

@app.route('/submit', methods = ['POST'])
def submit():

    name = request.form['name']
    cel = request.form['cel']
    msg = request.form['msg']

    data = {
        'name': name,
        'cel': cel,
        'msg': msg
    }
    
    list_param = [name, cel, msg]
    
    kinesis.put_record(
        StreamName = stream_name,
        Data = json.dumps(data),
        PartitionKey = str(uuid.uuid4())
    )

    return render_template('success.html', data = list_param)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8081)
