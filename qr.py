import streamlit as st
from PIL import Image
import qrcode
import requests
from io import BytesIO
import base64

# Function to generate QR code and return the path
def generate_qr_code(url, qr_color, logo_image):
    if logo_image is not None:
        logo = Image.open(logo_image)
    else:
        # Download the default logo from GitHub
        default_logo_url = 'https://raw.githubusercontent.com/zendaokaofficial/QRcodeGeneratorBPS/main/logoBPS-01.png'
        default_logo_response = requests.get(default_logo_url)

        if default_logo_response.ok:
            logo = Image.open(BytesIO(default_logo_response.content))
        else:
            st.error("Failed to retrieve the default logo. Please upload a custom logo.")
            return None

    basewidth = 100
    wpercent = (basewidth / float(logo.size[0]))
    hsize = int((float(logo.size[1]) * float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)

    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(url)
    qr.make()

    qr_img = qr.make_image(fill_color=qr_color, back_color="white").convert('RGB')
    pos = ((qr_img.size[0] - logo.size[0]) // 2, (qr_img.size[1] - logo.size[1]) // 2)
    qr_img.paste(logo, pos)

    # Save the QR code image
    qr_image_path = 'QR.png'
    qr_img.save(qr_image_path)

    return qr_image_path

# Streamlit App
st.markdown(
    """
    <style>
        body {
            background-color: #f1f1f1;
            color: #000000;
            font-family: sans-serif;
        }
        .st-bj {
            box-shadow: none;
        }
        .css-2trqyj {
            margin-top: 0;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title('QR Code Generator')
st.markdown("---")

# Input URL and QR code color
url = st.text_input('Enter URL:', 'https://example.com')
qr_color = st.color_picker('Choose QR Code Color:', '#0000FF')

# Upload logo image
logo_image = st.file_uploader('Upload Logo Image (optional):', type=['jpg', 'png', 'jpeg'])

# Generate QR code on button click
if st.button('Generate QR Code'):
    generated_qr_path = generate_qr_code(url, qr_color, logo_image)

    if generated_qr_path is not None:
        # Display the QR code image
        st.image(generated_qr_path, use_column_width=True, caption='Generated QR Code')

        # Download button
        with open(generated_qr_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
            st.markdown(f'<a href="data:application/octet-stream;base64,{data}" download="QR.png"><button>Download QR Code</button></a>', unsafe_allow_html=True)

# Copyright notice
st.markdown("---")
st.markdown("© 2024 Badan Pusat Statistik Kabupaten Tabanan. All rights reserved.")
