from flask import Flask , render_template, request
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)

client = Groq()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return "Welcome to the about page"

@app.route('/generate',methods=['POST'])
def generate():
    user_prompt = request.form.get('prompt','').strip()
    if not user_prompt:
        return render_template('index.html',error='Please enter a prompt')   

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=1,
        max_completion_tokens=2048,
        top_p=1,
        reasoning_effort="medium"
    )

    ai_response = response.choices[0].message.content or "The model returned an empty response."

    return render_template(
        'index.html',
        ai_response=ai_response,
        user_prompt=user_prompt
    )

    print(user_prompt)

if __name__=='__main__':
    app.run(debug=True)