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
    "try_to_refresh_with_empty_energy": 0,
    "try_to_refresh_with_no_pega": 0,
    "playing": False
} for x in range(quantity_sub_account)]


@app.route('/', methods=['GET'])
def get_all_data():
    return jsonify({'sub_accounts': sub_accounts})


@app.route('/data', methods=['GET'])
def get_data():

    sub_accounts_already_run = [x for x in sub_accounts if _already_run(x)]

    accounts_with_0_horses = list(map(lambda x: {"index" :x["sub_account_index"], "last_race_started_description" :x["last_race_started_description"], "subaccount": x["sub_account"]},
                                      [x for x in sub_accounts_already_run if
                                       (not _has_horses(x["energy_pega_1"])) and
                                       (not _has_horses(x["energy_pega_2"])) and
                                       (not _has_horses(x["energy_pega_3"]))
                                       ]))

    accounts_with_1_horses = list(map(lambda x: {"index" :x["sub_account_index"], "last_race_started_description" :x["last_race_started_description"], "subaccount": x["sub_account"], "pega_1": x["energy_pega_1"]},
                                      [x for x in sub_accounts_already_run if
                                       _has_horses(x["energy_pega_1"]) and
                                       (not _has_horses(x["energy_pega_2"])) and
                                       (not _has_horses(x["energy_pega_3"]))
                                       ]))
    accounts_with_2_horses = list(map(lambda x: {"index" :x["sub_account_index"], "last_race_started_description" :x["last_race_started_description"], "subaccount": x["sub_account"], "pega_1": x["energy_pega_1"], "pega_2": x["energy_pega_2"]},
                                      [x for x in sub_accounts_already_run if
                                       _has_horses(x["energy_pega_1"]) and
                                       _has_horses(x["energy_pega_2"]) and
                                       (not _has_horses(x["energy_pega_3"]))
                                       ]))
    accounts_with_3_horses = list(map(lambda x: {"index" :x["sub_account_index"], "last_race_started_description" :x["last_race_started_description"], "subaccount": x["sub_account"], "pega_1": x["energy_pega_1"], "pega_2": x["energy_pega_2"], "pega_3": x["energy_pega_3"]},
                                      [x for x in sub_accounts_already_run if
                                       _has_horses(x["energy_pega_1"]) and
                                       _has_horses(x["energy_pega_2"]) and
                                       _has_horses(x["energy_pega_3"])
                                       ]))

    sum_with_1_horses = sum(int(x['pega_1']) for x in accounts_with_1_horses)
    sum_with_2_horses = sum(int(x['pega_1']) + int(x['pega_2']) for x in accounts_with_2_horses)
    sum_with_3_horses = sum(int(x['pega_1']) + int(x['pega_2']) + int(x['pega_3']) for x in accounts_with_3_horses)
    energy_total = sum_with_1_horses + sum_with_2_horses + sum_with_3_horses

    json_to_return = {
        "_energy_total": energy_total,
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


@app.route('/account_empty_energy', methods=['GET'])
def account_empty_energy():
    sub_account = request.args.get('sub_account')
    sub_account_object = [x for x in sub_accounts if x["sub_account"].startswith(sub_account[:5]) and x["sub_account"].endswith( "..." + sub_account[-4:])][0]

    sub_account_object["try_to_refresh_with_empty_energy"] = sub_account_object["try_to_refresh_with_empty_energy"] + 1

    if sub_account_object["try_to_refresh_with_empty_energy"] > 3:
        return jsonify({'to_go_to_next_account': True})
    else:
        return jsonify({'to_go_to_next_account': False})


@app.route('/account_no_pega', methods=['GET'])
def account_no_pega():
    sub_account = request.args.get('sub_account')
    sub_account_object = [x for x in sub_accounts if x["sub_account"].startswith(sub_account[:5]) and x["sub_account"].endswith( "..." + sub_account[-4:])][0]

    sub_account_object["try_to_refresh_with_no_pega"] = sub_account_object["try_to_refresh_with_no_pega"] + 1

    if sub_account_object["try_to_refresh_with_no_pega"] > 3:
        return jsonify({'to_go_to_next_account': True})
    else:
        return jsonify({'to_go_to_next_account': False})


@app.route('/pega_race_started', methods=['GET'])
def pega_race_started():

    sub_account = request.args.get('sub_account')
    energy_pega_1 = request.args.get('energy_pega_1')
    energy_pega_2 = request.args.get('energy_pega_2')
    energy_pega_3 = request.args.get('energy_pega_3')
    last_race_started_description = request.args.get('last_race_started_description')

    sub_account_object = [x for x in sub_accounts if x["sub_account"].startswith(sub_account[:5]) and x["sub_account"].endswith("..." + sub_account[-4:])]
    if sub_account_object:
        sub_account_object[0]["started_time" ] = datetime.datetime.now()
        sub_account_object[0]["energy_pega_1"] = energy_pega_1
        sub_account_object[0]["energy_pega_2"] = energy_pega_2
        sub_account_object[0]["energy_pega_3"] = energy_pega_3
        sub_account_object[0]["last_race_started_description"] = last_race_started_description
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

        for sub_account in sub_accounts:
            sub_account["try_to_refresh_with_empty_energy"] = 0
            sub_account["try_to_refresh_with_no_pega"] = 0

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
        sorted_sub_accounts = sorted(sub_accounts, key=lambda x: x['started_time'], reverse=True)
        sorted_sub_accounts = sorted_sub_accounts[:4]
        sorted_sub_accounts = list(map(lambda x: x["sub_account"], sorted_sub_accounts))

        sub_account_object = max(filter(lambda f: f["sub_account"] != actual_sub_account and f["sub_account"]  not in sorted_sub_accounts, sub_accounts), key=lambda x: max({int(x['energy_pega_1'] if x['energy_pega_1'] != '' else 0), int(x['energy_pega_2']  if x['energy_pega_2'] != '' else 0), int(x['energy_pega_3'] if x['energy_pega_3'] != '' else 0)}, key=lambda y: y))

        max_energy = max({int(sub_account_object['energy_pega_1'] if sub_account_object['energy_pega_1'] != '' else 0), int(sub_account_object['energy_pega_2'] if sub_account_object['energy_pega_2'] != '' else 0), int(sub_account_object['energy_pega_3'] if sub_account_object['energy_pega_3'] != '' else 0)})

        if max_energy != "" and int(max_energy) > 3:
            return sub_account_object['sub_account_index']
        else:
            return min(sub_accounts, key=lambda x: x['started_time'])['sub_account_index']


def _get_empty_sub_account():
    try:
        return next(x for x in sub_accounts if x["sub_account"] is "")
    except:
        return None


if __name__ == '__main__':
    app.run(host= '0.0.0.0')



