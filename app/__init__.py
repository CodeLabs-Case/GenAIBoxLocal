from flask import Flask, request, jsonify, render_template
from flask_restful import Api
import urllib.request
import openai
import os
from datetime import datetime, timedelta

genaibox = Flask(__name__,static_url_path='/static')

### MODEL AND FUNCTIONS
class ChatGPT3(object):
    def __init__(self, model, temp, max_tokens, top_p, frequency_penalty, presence_penalty, context=''):
        self.openai_api_key = os.environ['OPENAI_API_KEY']
        # (7) chosen parameters for example
        self.model = model
        self.context = context
        self.temp = temp
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty

    def get_response(self, text):
        openai.api_key = self.openai_api_key
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{'role':'user','content':text}],
            temperature=self.temp,
            max_tokens=self.max_tokens,
            top_p=self.top_p,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty
        )
        return response.choices[0].message['content'].strip()

    def chat(self, text):
        # Tell the model what the Context/History is so that it won't respond to past questions
        response = self.get_response("Context:" + self.context + "Prompt:" + text)

        # Add to the conversation history
        self.context += text + '\n'

        #print('\n\nContext:\n{}'.format(self.context))
        return response

    def clearContext(self):
        self.context = ''



### Parameter Tunning
# Summarizer Box(1):
    # Low Temperature
    # Large Frequency Penalty (Avoid Redundant Summaries)
# Examiner Box(2):
    # Medium Temperature (More relaxed, Unpredicable)
    # Higher Top-P (Wordiness)
    # No Frequency Penalty (Redundancy Acceptable)
# Instructor Box(3):
    # Low Temperature (Predictable)
    # Small Frequency Penalty (Small Repetition Acceptable)
# gpt-3.5-turbo-16k
    # 16,384 tokens
    # Same capabilities as the standard gpt-3.5-turbo model but with 4 times the context.
# MODEL, TEMP, MAX_TOKENS, TOP-P, FREQ_PEN, PRES_PEN, STOP
Box1 = ChatGPT3('gpt-3.5-turbo-16k', 0.1, 1000, 0.1, 0.5, 0.0)
Box2 = ChatGPT3('gpt-3.5-turbo-16k', 0.5, 1000, 0.3, 0.0, 0.0)
Box3 = ChatGPT3('gpt-3.5-turbo-16k', 0.1, 1000, 0.2, 0.2, 0.0)

# Internal state to hold current box selected
state = {
    "current_box" : "0"
}



### ENDPOINTS
@genaibox.route("/")
def index():
    return render_template("index.html")

@genaibox.route('/chat', methods=['POST'])
def process():
    prompt = request.form['user_input']
    
    #print("API KEY: {}".format(Box1.getAPIKey()))
    if state['current_box'] == '1':
        generated_text = Box1.chat(prompt)
    elif state['current_box'] == '2':
        generated_text = Box2.chat(prompt)
    elif state['current_box'] == '3':
        generated_text = Box3.chat(prompt)
    else:
        # Default to Box1
        generated_text = Box1.chat(prompt)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify(data=generated_text)  # Return JSON response for AJAX request
    
    # if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
    #     return jsonify(data=generated_text)  # Return JSON response for AJAX request

    return render_template('index.html')  # Render the template for regular form submission

@genaibox.route('/box1', methods=['GET'])
def box1():
    state['current_box'] = '1'
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    context_path = os.path.join(current_dir, 'data', 'context_box1.txt')

    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_dir, 'data', 'template_box1.txt')
    
    with open(context_path, 'r') as file:
        context = file.read()
    with open(template_path, 'r') as file:
        template = file.read()
    


    # Hosted version code
    '''
    with urllib.request.urlopen('https://genaiazurestore.blob.core.windows.net/container0/context_box1.txt') as response:
        context = response.read().decode('utf-8')

    with urllib.request.urlopen('https://genaiazurestore.blob.core.windows.net/container0/template_box1.txt') as response:
        template = response.read().decode('utf-8')
    '''



    # When the box is loaded clear contex
    Box1.clearContext()
    # Load the box with content and examples
    Box1.chat("Context: " + context + "\n" + "Few-Examples Section: " + template)

    response = 'Summarizer Loaded!'

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify(data=response)  # Return JSON response for AJAX request
    
    return None

@genaibox.route('/box2', methods=['GET'])
def box2():
    state['current_box'] = '2'

    current_dir = os.path.dirname(os.path.abspath(__file__))
    context_path = os.path.join(current_dir, 'data', 'context_box2.txt')

    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_dir, 'data', 'template_box2.txt')
   
    with open(context_path, 'r') as file:
        context = file.read()
    with open(template_path, 'r') as file:
        template = file.read()
 


    # Hosted version code
    '''
    with urllib.request.urlopen('https://genaiazurestore.blob.core.windows.net/container0/context_box2.txt') as response:
        context = response.read().decode('utf-8')

    with urllib.request.urlopen('https://genaiazurestore.blob.core.windows.net/container0/template_box2.txt') as response:
        template = response.read().decode('utf-8')
    '''



    # When the box is loaded clear contex
    Box2.clearContext()
    # Load the box with content and examples
    Box2.chat("Context: " + context + "\n" + "Few-Examples Section: " + template)

    response = 'Examiner Loaded!'

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify(data=response)  # Return JSON response for AJAX request
    
    return None

@genaibox.route('/box3', methods=['GET'])
def box3():
    state['current_box'] = '3'

    current_dir = os.path.dirname(os.path.abspath(__file__))
    context_path = os.path.join(current_dir, 'data', 'context_box3.txt')

    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_dir, 'data', 'template_box3.txt')
   
    with open(context_path, 'r') as file:
        context = file.read()
    with open(template_path, 'r') as file:
        template = file.read()
    

    # Hosted version code
    '''
    with urllib.request.urlopen('https://genaiazurestore.blob.core.windows.net/container0/context_box3.txt') as response:
        context = response.read().decode('utf-8')

    with urllib.request.urlopen('https://genaiazurestore.blob.core.windows.net/container0/template_box3.txt') as response:
        template = response.read().decode('utf-8')
    '''



    # When the box is loaded clear contex
    Box3.clearContext()
    # Load the box with content and examples
    Box3.chat("Context: " + context + "\n" + "Few-Examples Section: " + template)

    response = 'Instructor Loaded!'

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify(data=response)  # Return JSON response for AJAX request

    return None