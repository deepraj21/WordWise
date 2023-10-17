import google.generativeai as palm
from flask import Flask, render_template, request

app = Flask(__name__)

palm.configure(api_key='PALM API')

models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]

model = models[0].name #chat-bison-001

def generate_solution(prompt):
    completion = palm.generate_text(
        model=model,
        prompt="You are an expert at solving word problems."+prompt+"give a step by step analysis",
        temperature=0,  
        max_output_tokens=800,
    )
    
    result = completion.result
    
    return result

@app.route('/', methods=['GET', 'POST'])
def index():
 
    solution = None
    
    if request.method == 'POST':
        user_prompt = request.form.get('word_problem')
        solution = generate_solution(user_prompt)
    return render_template('index.html', solution=solution)

if __name__ == '__main__':
    app.run(debug=True)
