from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import requests


app = Flask(__name__)

client = MongoClient('3.36.127.19', 27017, username="test", password="test")
db = client.reila


@app.route("/")
def main():
    # show saved word in DB and display in HTML
    alert_receive = request.args.get("alert")
    words = list(db.vocabs.find({}, {"_id":False}))
    return render_template("index.html", pyAlert=alert_receive, pyWords=words, alert=alert_receive)


@app.route("/detail/<keyword>")
def detail(keyword):
    # find definition from api and send it to html
    condition_receive = request.args.get("condition_give")
    r = requests.get(f"https://owlbot.info/api/v4/dictionary/{keyword}", headers = {"Authorization": "Token PutYourTokenHere"})
    if r.status_code != 200:
        return redirect(url_for("main", alert="Word not found in dictionary"))
    result = r.json()
    print(result)
    for one_defin in result["definitions"]:
        one_defin["definition"] = one_defin["definition"].encode("ascii", "ignore").decode("utf-8")
        if one_defin["example"] is not None:
            one_defin["example"] = one_defin["example"].encode("ascii", "ignore").decode("utf-8")
    return render_template("detail.html", keyword=keyword, pyResult=result, condition=condition_receive)


@app.route("/api/save_word", methods=["POST"])
def save_word():
    word_receive = request.form["word_give"]
    defin_receive = request.form["defin_give"]
    doc = {"word":word_receive,"defin":defin_receive }
    db.vocabs.insert_one(doc)
    return jsonify({"result": "success", "msg": "Saved"})


@app.route('/api/delete_word', methods=['POST'])
def delete_word():
    word_receive = request.form["word_give"]
    db.vocabs.delete_one({"word":word_receive})
    return jsonify({'result': 'success', 'msg': 'Deleted'})


@app.route('/api/save_ex', methods=['POST'])
def save_ex():
    ex_receive = request.form["ex_give"]
    word_receive = request.form['word_give']
    db.vocabs.update({"word":word_receive}, {"$set":{"example":ex_receive}})
    return jsonify({'result': 'success', 'msg':f'example "{ex_receive}" saved'})

@app.route('/api/display_ex', methods = ['GET'])
def display_ex():
    word_receive = request.args.get("word_give")
    display_word = list(db.vocabs.find({"word":word_receive},{'_id':False}))
    print(display_word)
    return jsonify({'display':display_word})

@app.route('/api/delete_ex', methods = ['POST'])
def delete_ex():
    word_receive = request.form['word_give']
    example = list(db.vocabs.find_one({"word": word_receive}))
    db.vocabs.update({'word':word_receive}, {'$unset': {'example':1}}, multi=True)
    print(word_receive, example)
    return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
