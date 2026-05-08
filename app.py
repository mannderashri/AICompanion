from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
          return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
          data = request.json
          message = data.get('message', '')

    # Placeholder for AI logic
          response = f"I received your message: '{message}'. This is a simulated response from the AI Companion backend."

    return jsonify({
                  'status': 'success',
                  'response': response
    })

if __name__ == '__main__':
          app.run(debug=True)
