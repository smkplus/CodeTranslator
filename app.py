from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import pprint
import google.generativeai as palm

app = Flask(__name__)
CORS(app) # Allow all origins

palm.configure(api_key='AIzaSyCGkUnqLBe-B0Z5XmI-ZMjkmXvi9ZcqhIE')   
models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name


@app.route('/')
def home():
  return send_from_directory('static', 'index.html')

@app.route('/process', methods=['POST'])
def process_file():
  try:
    data = request.get_json()
    if 'code' in data and 'target_language' in data and 'input_language' in data:
      input_code = data['code']
      target_language = data['target_language']
      input_language = data['input_language']
      prompt = f"{input_code}\nTranslate code from {input_language} to {target_language}, preserving logic and functionality while adhering to {target_language}'s syntax and rules."

      completion = palm.generate_text(
            model=model,
            prompt=prompt,
            temperature=0,
            # The maximum length of the response
            max_output_tokens=800,
      )

      print(completion.result)
      return jsonify({'result': completion.result})
    else:
      return jsonify({'error': 'Invalid request. Please provide code, target_language, and input_language in the request.'}), 400
  except Exception as e:
    print("Exception:", str(e))
    return jsonify({'error': 'An internal server error occurred. Please try again later.'}), 500

if __name__ == '__main__':
    # Use the PORT environment variable if provided, or default to 5000
    port = int(os.environ.get('PORT', 8000))

    # Run the app with the specified host and port
    app.run(host='0.0.0.0', port=port)
