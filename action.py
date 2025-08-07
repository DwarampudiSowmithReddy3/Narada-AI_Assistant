from gpt4all import GPT4All

def fetch_general_answer(query):
    """Fetch answer using GPT4All instead of OpenAI"""
    model = GPT4All("mistral-7b-instruct-v0.1.Q4_0.gguf")  # Change model if needed
    response = model.generate(query, max_tokens=100)
    return response

def respond_to_user():
    """Process user query and return AI response"""
    query = input("Ask something: ")  # Replace this with GUI input
    return fetch_general_answer(query)
