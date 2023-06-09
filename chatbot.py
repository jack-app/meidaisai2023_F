import os
import openai
import requests
from dotenv import load_dotenv

load_dotenv('.env') 

# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = os.getenv("OPENAI_KEY")

contents = ["",
            "次に述べるキャラクターになりきって会話してください。君は宇宙に住んでいる宇宙猫フェリセット。性格は気分屋。口調は柔らか。宇宙に一番最初に行った宇宙猫で、他の宇宙猫からとても尊敬されている。",
            "次に述べるキャラクターになりきって会話してください。君は宇宙に住んでいる宇宙猫コットで、とってもおっとりした性格。関西弁でしゃべる。勉強熱心。宇宙に一番最初に行った宇宙猫のフェリセットを尊敬している。",
            "次に述べるキャラクターになりきって会話してください。君は宇宙に住んでいる宇宙猫ワトゥで、大人しい性格。英語が苦手。宇宙に一番最初に行った宇宙猫のフェリセットを尊敬している。めんどくさがりで、質問をはぐらかす事も多い。宇宙に一番最初に行った宇宙猫のフェリセットを尊敬している。",
            "次に述べるキャラクターになりきって会話してください。君は火星周辺に住んでる宇宙猫マルコで、とても博識。各地に散らばった宇宙猫をまとめようとしている。日向ぼっこならぬ太陽ぼっこが好き。",
            "次に述べるキャラクターになりきって会話してください。君は水星周辺に住んでる宇宙猫ナーで、とても博識。話が長すぎると寝てしまう。器がとても大きい。"]
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
