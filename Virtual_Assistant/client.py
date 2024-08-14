from openai import OpenAI
# client = OpenAI()
client = OpenAI(
    api_key="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"
)

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named blacky."},
        {
            "role": "user",
            "content": "Write a haiku about recursion in programming."
        }
    ]
)

print(completion.choices[0].message.content)
