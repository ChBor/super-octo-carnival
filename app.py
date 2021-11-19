import json
from typing import Any
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/", methods = ["GET"])
def get_all_users():
    with open("data.json") as file:
        data = json.load(file)
    return jsonify([i["name"] for i in data])

@app.route("/", methods = ["POST"])
def create_new_user():
    new_user: dict[str, Any] = request.json
    with open("data.json") as file:
        data = json.load(file)
    data[new_user["login"]] = {"password": new_user["password"]}
    with open("data.json", "w") as file:
        json.dump(data, file)
    return jsonify({"info": "Success"})

@app.route("/", methods = ["VIEW"])
def verification():
    verification_data = request.json
    with open("data.json", "r") as file:
        data = json.load(file)
        for account in data:
            if account == verification_data:
                return "You were verified"
    return "Incorrect username or password"

@app.route("/", methods = ["PUT"])
def change_password():
    new_data: dict[str:str] = request.json
    with open("data.json", "r") as file:
        data = json.load(file)
        for account in data:
            if account["name"] == new_data["name"]:
                account["password"] = new_data["password"]
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)
    return "Password has been changed to %s" % new_data["password"]

@app.route("/",methods=["DELETE"])
def delete_account():
    deleted_account = request.json
    with open("data.json", "r") as file:
        data = json.load(file)
        for account in data:
            if account == deleted_account:
                data.remove(account)
    with open("data.json","w") as file:
        json.dump(data, file, indent=4)
    return "Account %s has been successfully deleted" % deleted_account["name"]

if __name__ ==' __main__':
    app.run(debug=True)
