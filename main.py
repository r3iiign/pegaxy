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
def get_all_data():
    return jsonify({'sub_accounts': sub_accounts})


@app.route('/data', methods=['GET'])
def get_data():

    sub_accounts_already_run = [x for x in sub_accounts if _already_run(x)]

    accounts_with_0_horses = list(map(lambda x: {"index" :x["sub_account_index"], "subaccount": x["sub_account"]},
                                      [x for x in sub_accounts_already_run if
                                       (not _has_horses(x["energy_pega_1"])) and
                                       (not _has_horses(x["energy_pega_2"])) and
                                       (not _has_horses(x["energy_pega_3"]))
                                       ]))

    accounts_with_1_horses = list(map(lambda x: {"index" :x["sub_account_index"], "subaccount": x["sub_account"], "pega_1": x["energy_pega_1"]},
                                      [x for x in sub_accounts_already_run if
                                       _has_horses(x["energy_pega_1"]) and
                                       (not _has_horses(x["energy_pega_2"])) and
                                       (not _has_horses(x["energy_pega_3"]))
                                       ]))
    accounts_with_2_horses = list(map(lambda x: {"index" :x["sub_account_index"], "subaccount": x["sub_account"], "pega_1": x["energy_pega_1"], "pega_2": x["energy_pega_2"]},
                                      [x for x in sub_accounts_already_run if
                                       _has_horses(x["energy_pega_1"]) and
                                       _has_horses(x["energy_pega_2"]) and
                                       (not _has_horses(x["energy_pega_3"]))
                                       ]))
    accounts_with_3_horses = list(map(lambda x: {"index" :x["sub_account_index"], "subaccount": x["sub_account"], "pega_1": x["energy_pega_1"], "pega_2": x["energy_pega_2"], "pega_3": x["energy_pega_3"]},
                                      [x for x in sub_accounts_already_run if
                                       _has_horses(x["energy_pega_1"]) and
                                       _has_horses(x["energy_pega_2"]) and
                                       _has_horses(x["energy_pega_3"])
                                       ]))

    json_to_return = {
        "horses_in_accounts": {
            "0": {
                "qtd": len(accounts_with_0_horses),
                "accounts": accounts_with_0_horses
            },
            "1": {
                "qtd": len(accounts_with_1_horses),
                "accounts": accounts_with_1_horses
            },
            "2": {
                "qtd": len(accounts_with_2_horses),
                "accounts": accounts_with_2_horses
            },
            "3": {
                "qtd": len(accounts_with_3_horses),
                "accounts": accounts_with_3_horses
            }

        }
    }

    return jsonify({'data': json_to_return})


def _already_run(account):
    return account["energy_pega_1"] != -1 and account["energy_pega_2"] != -1 and account["energy_pega_3"] != -1


def _has_horses(value):
    return value != ""


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

        next_sub_account_index = _get_next_sub_account_index(actual_sub_account)
        sub_accounts[next_sub_account_index]["started_time"] = datetime.datetime.now()
        return jsonify({
            'to_change': True,
            "next_sub_account_index": next_sub_account_index
        })
    else:
        return jsonify({'to_change': False})


def _get_next_sub_account_index(actual_sub_account):
    empty_sub_account = _get_empty_sub_account()

    if empty_sub_account is not None:
        return empty_sub_account['sub_account_index']
    else:
        sub_account_object = max(filter(lambda f: f["sub_account"] != actual_sub_account, sub_accounts), key=lambda x: max({x['energy_pega_1'], x['energy_pega_2'], x['energy_pega_3']}, key=lambda y: y))

        max_energy = max({sub_account_object['energy_pega_1'], sub_account_object['energy_pega_2'], sub_account_object['energy_pega_3']})

        if int(max_energy) > 10:
            return sub_account_object['sub_account_index']
        else:
            return max(sub_accounts, key=lambda x: x['started_time'])['sub_account_index']






def _get_empty_sub_account():
    try:
        return next(x for x in sub_accounts if x["sub_account"] is "")
    except:
        return None


if __name__ == '__main__':
    app.run(host= '0.0.0.0')



