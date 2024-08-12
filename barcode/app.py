from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import pyzbar.pyzbar as pyzbar
import io
import base64

app = Flask(__name__)

@app.route('/scan_barcode')
def scan_barcode():
    return render_template('upload_barcode.html')

@app.route('/upload_barcode', methods=['POST'])
def upload_barcode():
    # Handle image captured from the camera
    if request.form['barcode_image']:
        # Get the base64 image data from the form
        image_data = request.form['barcode_image']

        # Remove the data URL scheme from the base64 image data
        image_data = image_data.split(",")[1]

        # Decode the base64 image data
        image_bytes = base64.b64decode(image_data)

        # Open the image using PIL
        image = Image.open(io.BytesIO(image_bytes))
    
    # Handle image uploaded via file input
    elif 'fileUpload' in request.files:
        image_file = request.files['fileUpload']
        if image_file:
            image = Image.open(image_file)
        else:
            return 'No file uploaded or no barcode found in the image.'

    else:
        return 'No image data provided.'

    # Decode the barcode from the image
    barcodes = pyzbar.decode(image)
    
    if barcodes:
        barcode_data = barcodes[0].data.decode('utf-8')
        return f'Barcode data: {barcode_data}'
    else:
        return 'No barcode found in the image.'

if __name__ == '__main__':
    app.run(debug=True)
