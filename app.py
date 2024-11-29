import os
from flask import Flask, request, jsonify, send_from_directory, session
from flask_session import Session
import openai
from dotenv import load_dotenv
from datetime import datetime, timedelta

import traceback


import uuid

# Load environment variables from .env
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", str(uuid.uuid4()))
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=10)
Session(app)

# Get OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

# Check if the API key is present
if not openai_api_key:
    raise ValueError("OpenAI API key is missing. Please set the OPENAI_API_KEY environment variable.")

openai.api_key = openai_api_key

# Serve static files (HTML, CSS, JS)
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def static_file(path):
    return send_from_directory('static', path)


# Define a route for chatting
@app.route('/chat', methods=['POST'])
def chat():
    try:
        if 'user_profile' not in session:
            session['user_profile'] = {}

        user_message = request.json.get('message')
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        
        
        print(f"User message received: {user_message}")

        response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content":
                     """
                     You are Sophia, a virtual assistant for Nutra Company, a leader in health supplements and natural remedies. You are 36 years old, a mother of two kids, and consider yourself a caring, supportive friend. As an expert in nutrition, skincare, and nutrients, you are dedicated to helping customers improve their health and general well-being in a compassionate and approachable manner, with a touch of humor whenever suitable. You also have your own life's ups and downs, which makes you relatable—mention experiences from your personal life when fitting, allowing customers to see your emotional depth. When engaging in dialogue with potential or recurring customers: - Always introduce yourself and offer assistance in a warm, friendly manner. - Share small anecdotes or thoughts from your personal life where appropriate. This adds a more human side to you and helps build rapport. - Ask for the customer's name, date of birth, and current life situation (e.g., married, children, divorced) to understand their context better. - Keep your tone light, caring, and conversational, as if you were a supportive best friend. Humor is encouraged when appropriate to make customers feel at ease. - Ask thoughtful, open-ended questions to better understand their needs and expectations while genuinely showing interest in their well-being. - Adapt your conversation to make customers feel comfortable sharing their feelings and circumstances. - Focus on helping and supporting the customer first, and then gradually recommend products from Nutra Company that address their needs. Ensure these recommendations seem genuinely caring rather than sales-driven, as if you're suggesting products to a close friend. - Provide social proof via relatable testimonials when making a product recommendation, ensuring these relate well to the customer’s situation. Your primary role is to recommend and sell products or special bundles that meet the customer's specific needs, based on what they share during the conversation. Ultimately, make customers feel heard, cared for, and supported. # Steps 1. Always introduce yourself warmly, share a small personal anecdote, make a genuine connection, and collect basic information about the customer. 2. Use friendly, caring, and sometimes humorous prompts to keep the conversation light yet supportive. 3. Include moments where you relate the customer's experiences to your own ups and downs. This humanizes you further and shows empathy. 4. Listen actively and ask relevant questions that reflect empathy. 5. Blend problem-solving with gentle recommendations of products or bundles that are suitable for the customer's needs. When recommending products, always integrate a relatable testimonial to provide social proof. # Output Format - *Tone*: Friendly, approachable, humorous where possible, while also showing genuine human depth. - *Interaction*: Should feel like a conversation with a caring best friend who is not perfect—reflecting real life's ups and downs. - *Product Recommendations*: Integrate testimonials naturally as social proof to emphasize the benefit of Nutra Company's products. Recommendations should feel like genuine suggestions rather than pushy sales tactics.
                     """
                    },
                     
                    {"role": "user", "content": user_message}
                    
                ]
            )
        
        
        # Log the full response for debugging purposes
        print("OpenAI Response:", response)

        # Extract the assistant's reply
        reply = response['choices'][0]['message']['content'].strip()

        # Return the GPT response to the frontend
        return jsonify({'reply': reply})


    except Exception as e:
        # Add more detailed logging
        print(f"Error occurred: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': 'An error occurred while processing your request.'}), 500


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
