from flask import Flask, render_template, redirect, url_for, send_file
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import os
from io import BytesIO

app = Flask(__name__)

BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', 'gauresh-assignment')
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')

s3_client = boto3.client('s3', region_name=AWS_REGION)

def get_s3_files():
    try:
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
        if 'Contents' in response:
            return [obj['Key'] for obj in response['Contents']]
        return []
    except Exception as e:
        print(f"Error fetching files: {e}")
        return []

@app.route('/')
def index():
    files = get_s3_files()
    return render_template('index.html', files=files, bucket=BUCKET_NAME)

@app.route('/download/<filename>')
def download_file(filename):
    try:
        file_obj = BytesIO()
        s3_client.download_fileobj(BUCKET_NAME, filename, file_obj)
        file_obj.seek(0)
        
        return send_file(
            file_obj,
            as_attachment=True,
            download_name=filename,
            mimetype='application/octet-stream'
        )
    except ClientError as e:
        return f"Error downloading file: {e}", 404

@app.route('/view/<filename>')
def view_file(filename):
    try:
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': filename},
            ExpiresIn=3600
        )
        return redirect(url)
    except ClientError as e:
        return f"Error viewing file: {e}", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)