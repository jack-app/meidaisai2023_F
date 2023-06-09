from flask import *   # Flaskのなかみを全部持ってくる
from chatbot import chatbot
import sqlite3  # sqliteつかいます
app = Flask(__name__)  # アプリの設定

app.secret_key = 'dskfjmvdngbsnmiovenajovneov'  # 秘密鍵の設定


@app.route("/")
def jump():
    conn = sqlite3.connect('chattest.db')
    c = conn.cursor()
    c.execute("select id from user")
    ids=c.fetchall()
    id = 1
    for n in ids:
        if n[0] > id:
            id = n[0]

    c.execute("insert into user values(?,?)",(id+1,'あなた'))
    conn.commit()
    conn.close()
    session['user_id'] = id+1

    return redirect("/start")

@app.route("/start")
def start():
    return render_template("start.html")


# ユーザーを全て表示
@app.route("/userlist")
def userlist():
    conn = sqlite3.connect('chattest.db')
    c = conn.cursor()
    c.execute("select id, name from user")
    user_info = c.fetchall()
    conn.close()
    print("----------------")
    print(user_info)
    return render_template("userlist.html", tpl_user_info=user_info)


# /userlistで「チャットする」ボタンを押したときに動くプログラム。チャットルームがなければ(まだチャットしたことのない相手であれば)新規作成。
@app.route("/chatroom/<int:other_id>", methods=["POST"])
def chatroom_post(other_id):
    print(session)
    if "user_id" in session:
        # まずはチャットルームがあるかchatidをとってくる
        my_id = session["user_id"]
        print(my_id)
        conn = sqlite3.connect('chattest.db')
        c = conn.cursor()
        c.execute(
            "select id from chat where (user_id1 = ? and user_id2 = ?) or (user_id1 = ? and user_id2 = ?)", (my_id, other_id, other_id, my_id))
        chat_id = c.fetchone()
        print(chat_id)
        # とってきたidの中身で判定。idがNoneであれば作成、それ以外(数字が入っていれば)スルー
        if chat_id == None:

            c.execute("select name from user where id = ?", (my_id,))
            myname = c.fetchone()[0]
            c.execute("select name from user where id = ?", (other_id,))
            othername = c.fetchone()[0]
            # ルーム名を作る
            room =othername + "のへや"
            c.execute("insert into chat values(null,?,?,?)",
                      (my_id, other_id, room))
            conn.commit()
            # 作ったチャットルームのidを取得
            c.execute(
                "select id from chat where (user_id1 = ? and user_id2 = ?) or (user_id1 = ? and user_id2 = ?)", (my_id, other_id, other_id, my_id))
            chat_id = c.fetchone()
        conn.close()
        print(chat_id)
        return redirect("/chat/{}".format(chat_id[0]))


# チャットルーム表示
@app.route("/chat/<int:chatid>")
def chat_get(chatid):
    if "user_id" in session:
        my_id = session["user_id"]
        # ここにチャットをDBからとって、表示するプログラム
        conn = sqlite3.connect('chattest.db')
        c = conn.cursor()
        c.execute(
            "select chatmess.to_user, chatmess.from_user, chatmess.message, user.name from chatmess inner join user on chatmess.from_user = user.id where chat_id = ?", (chatid,))
        chat_fetch = c.fetchall()
        chat_info = []
        for chat in chat_fetch:
            chat_info.append(
                {"to": chat[0], "from": chat[1], "message": chat[2], "fromname": chat[3]})
        c.execute("select room from chat where id = ?", (chatid,))
        room_name = c.fetchone()[0]
        c.close()
        return render_template("chat.html", chat_list=chat_info, link_chatid=chatid, tpl_room_name=room_name, tpl_my_id=my_id)


# チャット送信時のプログラム
@app.route("/chat/<int:chatid>", methods=["POST"])
def chat_post(chatid):
    if "user_id" in session:
        # ここにチャットの送信ボタンが押されたときにDBに格納するプログラム
        my_id = session["user_id"]
        chat_message = request.form.get("input_message")
        conn = sqlite3.connect('chattest.db')
        c = conn.cursor()
        c.execute(
            "select user_id1, user_id2 from chat where id = ?", (chatid,))
        chat_user = c.fetchone()
        print(chat_user)
        if my_id != chat_user[0]:
            to_id = chat_user[0]
        else:
            to_id = chat_user[1]
        print(to_id)
        c.execute("insert into chatmess values(null,?,?,?,?)",
                  (chatid, to_id, my_id, chat_message))
        conn.commit()
        c.close()
        # ChatGPTによる返答の格納
        c = conn.cursor()
        c.execute("insert into chatmess values(null,?,?,?,?)",
                  (chatid, my_id, to_id, chatbot(to_id, chat_message)))
        conn.commit()
        c.close()
        

        return redirect("/chat/{}".format(chatid))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
