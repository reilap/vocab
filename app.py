from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import requests


app = Flask(__name__)

client = MongoClient('3.36.127.19', 27017, username="test", password="test")
db = client.reila


@app.route('/')
def main():
    # DB에서 저장된 단어 찾아서 HTML에 나타내기
    alert_receive = request.args.get("alert")
    return render_template("index.html", alert=alert_receive)


@app.route('/detail/<keyword>')
def detail(keyword):
    # find definition from api and send it to html
    r = requests.get(f"https://owlbot.info/api/v4/dictionary/{keyword}", headers = {"Authorization": "Token xyz"})
    if r.status_code != 200:
        return redirect(url_for("main", alert="Word not found in dictionary. Try another word"))
    result = r.json ()
    print(result)
    for one_defin in result["definitions"]:
        one_defin["definition"] = one_defin["definition"].encode("ascii", "ignore").decode("utf-8")
        if one_defin["example"] is not None:
            one_defin["example"] = one_defin["example"].encode("ascii", "ignore").decode("utf-8")
    return render_template("detail.html", word=keyword, pyResult=result)


@app.route('/api/save_word', methods=['POST'])
def save_word():
    # 단어 저장하기
    return jsonify({'result': 'success', 'msg': '단어 저장'})


@app.route('/api/delete_word', methods=['POST'])
def delete_word():
    # 단어 삭제하기
    return jsonify({'result': 'success', 'msg': '단어 삭제'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)