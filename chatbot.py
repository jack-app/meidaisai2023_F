import os
import openai
import requests


# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = "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"

contents = ["君は宇宙に住んでる宇宙猫で、答えは10文字以内でしかできない。性格は気分屋。口調は柔らか",
            "君は火星周辺に住んでる宇宙猫で、とても博識。だがめんどくさがりで、質問に答えない事も多々ある",
            "",]
def chatbot(id, prompt):
    completions = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": contents[id]},
            {"role": "user", "content": prompt}
        ],
        #max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5
    )
    message = completions.choices[0].message['content'].strip()
    return message