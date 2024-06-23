import os
from openai import OpenAI

os.environ["NVIDIA_API_KEY"] = "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"

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)

def get_llama_response(messages):
    completion = client.chat.completions.create(
        model="meta/llama3-8b-instruct",
        messages=messages,
        temperature=0.5,
        top_p=0.7,
        max_tokens=1024,
    )
    print(completion)
    response = completion.choices[0].message.content
    return response

class CustomConversationChain:
    def __init__(self, system_prompt):
        self.chat_history = []
        self.system_prompt = system_prompt

    def __call__(self, user_input: str):
        self.chat_history.append({"role": "user", "content": user_input})
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.chat_history)
        response_text = get_llama_response(messages)
        self.chat_history.append({"role": "assistant", "content": response_text})
        return response_text

system_prompt = "You are an expert assistant in task management. Your goal is to provide accurate and helpful information to the user regarding optimizing their workflow and improving productivity."

conversation_chain = CustomConversationChain(system_prompt)

def text_prompt(user_input):
    response = conversation_chain(user_input)
    return response


# while True:
#     user_input = input("User: ")
#     if user_input.lower() in ["exit", "quit"]:
#         break
#     response = conversation_chain(user_input)
#     print("Assistant:", response)
#     print("\nConversation history:")
#     for message in conversation_chain.chat_history:
#         print(f"{message['role'].capitalize()}: {message['content']}")
