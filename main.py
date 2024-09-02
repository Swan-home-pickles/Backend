from flask import Flask, request, jsonify
import urllib.parse
import logging
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/submit-form', methods=['POST'])
def submit_form():
    try:
        data = request.json

        name = data.get('name')
        email = data.get('email')
        phone = data.get('Phonenum')
        subject = data.get('subject')
        message = data.get('message')

        # Construct the WhatsApp message for the form submission
        whatsapp_message = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nSubject: {subject}\nMessage: {message}"
        whatsapp_message_encoded = urllib.parse.quote(whatsapp_message)

        whatsapp_url = f"https://wa.me/9705050055?text={whatsapp_message_encoded}"  # Replace with your number

        logging.debug(f"WhatsApp URL: {whatsapp_url}")

        return jsonify({'whatsapp_url': whatsapp_url})
    except Exception as e:
        logging.error(f"Error submitting form: {e}")
        return jsonify({'error': 'Error submitting form'}), 500


@app.route('/checkout', methods=['POST'])
def checkout():
    try:
        data = request.json

        name = data.get('name')
        phonenum = data.get('phonenum')
        address = data.get('address')
        cart_items = data.get('cartItems')

        # Construct the message with proper formatting for the checkout
        message = f"Name: {name}\nPhone: {phonenum}\nAddress: {address}\n\nOrder Details:\n"
        
        total_amount = 0
        for item in cart_items:
            product_name = item['product']['name']
            price = item['product']['price'][item['selectedOption']]
            grams = item['selectedOption']
            quantity = item['quantity']
            subtotal = price * quantity

            message += f"{product_name} ({grams}): ₹{price} x {quantity} = ₹{subtotal}\n"
            total_amount += subtotal

        message += f"\nTotal Amount: ₹{total_amount}"
        
        # URL-encode the message to be sent via WhatsApp
        whatsapp_message_encoded = urllib.parse.quote(message)
        
        # Replace with your WhatsApp number
        whatsapp_link = f"https://wa.me/9705050055?text={whatsapp_message_encoded}"

        logging.debug(f"WhatsApp Link: {whatsapp_link}")

        return jsonify({'whatsappLink': whatsapp_link})
    except Exception as e:
        logging.error(f"Error during checkout: {e}")
        return jsonify({'error': 'Error processing checkout'}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
