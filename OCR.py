import streamlit as st
import sqlite3
import easyocr
from PIL import Image

# Set up the database
conn = sqlite3.connect(r"D:\Data science\assignment 3\business_cards.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS cards
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              company_name TEXT,
              card_holder_name TEXT,
              designation TEXT,
              mobile_number TEXT,
              email_address TEXT,
              website_url TEXT,
              area TEXT,
              city TEXT,
              state TEXT,
              pin_code TEXT,
              image BLOB)''')
conn.commit()

# Set up the OCR reader
reader = easyocr.Reader(['en'])

# Define the Streamlit UI
st.title('Business Card Reader')

uploaded_file = st.file_uploader('Upload a business card image', type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    image = Image.open(r"C:\Users\Deepak\Downloads\2.png")
    st.image(image, caption='Uploaded business card image', use_column_width=True)

    # Extract information from the business card
    result = reader.readtext(image)
    extracted_info = {}
    for r in result:
        text = r[1].strip()
        if 'company' in text.lower():
            extracted_info['company_name'] = text
        elif 'name' in text.lower() and 'company' not in text.lower():
            extracted_info['card_holder_name'] = text
        elif 'designation' in text.lower():
            extracted_info['designation'] = text
        elif 'mobile' in text.lower():
            extracted_info['mobile_number'] = text
        elif 'email' in text.lower():
            extracted_info['email_address'] = text
        elif 'website' in text.lower():
            extracted_info['website_url'] = text
        elif 'area' in text.lower():
            extracted_info['area'] = text
        elif 'city' in text.lower():
            extracted_info['city'] = text
        elif 'state' in text.lower():
            extracted_info['state'] = text
        elif 'pin' in text.lower():
            extracted_info['pin_code'] = text

    # Display the extracted information
    st.subheader('Extracted Information')
    for k, v in extracted_info.items():
        st.write(f'{k}: {v}')

    # Save the extracted information and image to the database
    if st.button('Save'):
        image_data = uploaded_file.read()
        c.execute('''INSERT INTO cards
                     (company_name, card_holder_name, designation, mobile_number, email_address,
                      website_url, area, city, state, pin_code, image)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (extracted_info.get('company_name', ''),
                   extracted_info.get('card_holder_name', ''),
                   extracted_info.get('designation', ''),
                   extracted_info.get('mobile_number', ''),
                   extracted_info.get('email_address', ''),
                   extracted_info.get('website_url', ''),
                   extracted_info.get('area', ''),
                   extracted_info.get('city', ''),
                   extracted_info.get('state', ''),
                   extracted_info.get('pin_code', ''),
                   image_data))
        conn.commit()
        st.success('Business card information saved to the database.')