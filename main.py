from flask import Flask, jsonify, request
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app, support_credentials=True)

quantity_sub_account = 55

sub_accounts = [{
    "sub_account": "",
    "sub_account_index": x,
    "started_time": datetime.datetime.now(),
    "energy_pega_1": -1,
    "energy_pega_2": -1,
    "energy_pega_3": -1,
    "playing": False
} for x in range(quantity_sub_account)]

@app.route('/', methods=['GET'])
def get_data():
    return jsonify({'sub_accounts': sub_accounts})

@app.route('/pega_race_started', methods=['GET'])
def pega_race_started():

    sub_account = request.args.get('sub_account')
    energy_pega_1 = request.args.get('energy_pega_1')
    energy_pega_2 = request.args.get('energy_pega_2')
    energy_pega_3 = request.args.get('energy_pega_3')

    sub_account_object = [x for x in sub_accounts if x["sub_account"].startswith(sub_account[:5]) and x["sub_account"].endswith("..." + sub_account[-4:])]
    if sub_account_object:
        sub_account_object[0]["started_time" ] = datetime.datetime.now()
        sub_account_object[0]["energy_pega_1"] = energy_pega_1
        sub_account_object[0]["energy_pega_2"] = energy_pega_2
        sub_account_object[0]["energy_pega_3"] = energy_pega_3
        sub_account_object[0]["playing"] = True

    return jsonify({'result': "OK"})


@app.route('/metamask_get_next_sub_account', methods=['GET'])
def metamask_get_next_sub_account():

    actual_sub_account = request.args.get('actual_sub_account')

    sub_account_object = [x for x in sub_accounts if x["sub_account"] == actual_sub_account]
    if not sub_account_object:
        empty_sub_account = _get_empty_sub_account()
        empty_sub_account["sub_account"] = actual_sub_account
        empty_sub_account["started_time"] = datetime.datetime.now()

        return jsonify({'to_change': False})

    if sub_account_object[0]["playing"]:
        sub_account_object[0]["playing"] = False
        sub_account_object[0]["started_time"] = datetime.datetime.now()

        next_sub_account_index = _get_next_sub_account_index()
        sub_accounts[next_sub_account_index]["started_time"] = datetime.datetime.now()
        return jsonify({
            'to_change': True,
            "next_sub_account_index": next_sub_account_index
        })
    else:
        return jsonify({'to_change': False})


def _get_next_sub_account_index():
    empty_sub_account = _get_empty_sub_account()

    if empty_sub_account is not None:
        return empty_sub_account['sub_account_index']
    else:
        return min(sub_accounts, key=lambda x: x['started_time'])['sub_account_index']


def _get_empty_sub_account():
    try:
        return next(x for x in sub_accounts if x["sub_account"] is "")
    except:
        return None


if __name__ == '__main__':
    app.run(host= '0.0.0.0')



