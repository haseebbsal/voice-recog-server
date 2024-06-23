import os
from openai import OpenAI

os.environ["NVIDIA_API_KEY"] = "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"

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)

system_prompt = """
You are an expert assistant in task management. Classify the given tasks based on the Eisenhower Matrix, which categorizes tasks as follows:
- Quadrant 1: Urgent and Important
- Quadrant 2: Not Urgent but Important
- Quadrant 3: Urgent but Not Important
- Quadrant 4: Not Urgent and Not Important

For each task provided, return a array of JSON objects in the following format:
{'task_name': task, 'priority': [Important or Not Important, Urgent or Not Urgent]}

In the response i just want an array of json objects with the categorization of the tasks as i mentioned and nothing else.
Here are the tasks to classify:
"""

def classify_tasks(user_input):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]
    completion = client.chat.completions.create(
        model="upstage/solar-10.7b-instruct",
        messages=messages,
        temperature=0.1,
        top_p=0.9,
        max_tokens=3500 
    )
    response = completion.choices[0].message.content
    return response

# Example task input
user_input = """
1. Completing the assignment whose deadline is tomorrow.
2. Finishing a project that will reward me with a bonus if I finish it by tomorrow but the deadline is in one week.
3. Running an errand so that mom can cook dinner for us.
4. Doing my friend's homework.
5. Taking my girlfriend for a dinner date.
"""


def llm_task_categorization(user_input):
    response = classify_tasks(user_input)
    return response

# print(response)
# print(eval(response))
# print()
