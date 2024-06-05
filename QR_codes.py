import qrcode
import json
import base64
import io


def generate_qr_code_from_json(data):
    try:
        # Convert JSON data to a string
        json_data = json.dumps(data)

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=20,
            border=4,
        )
        qr.add_data(json_data)
        qr.make(fit=True)

        # Create an in-memory file-like object
        img_stream = io.BytesIO()

        # Make and save the QR code image to the in-memory stream
        img = qr.make_image(fill="black", back_color="white")
        img.save(img_stream, format="PNG")

        img_base64 = base64.b64encode(img_stream.getvalue()).decode()

        print("QR code generated as base64")
        return img_base64
    except Exception as e:
        print(f"An error occurred: {e}")


