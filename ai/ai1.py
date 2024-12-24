from gpt4all import GPT4All

# Initialize the GPT4All model
model_name = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"  # Replace with the correct model file name if needed
model = GPT4All(model_name)

# Start a chat session
with model.chat_session() as session:
    # Generate a response to a prompt
    prompt = "Give me an article about the Indian CBSE maths class 2 syllabus"
    response = session.generate(prompt, max_tokens=1000)

    # Print the generated response
    print("GPT4All Response:", response)
