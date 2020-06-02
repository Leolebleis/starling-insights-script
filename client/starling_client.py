from datetime import datetime
import calendar
import requests
import json

separator = "\n------------------------\n"
starling_root = "https://api.starlingbank.com/api/v2"
heroku = "https://starling-insights-api.herokuapp.com"
accounts_path = "/accounts/c4602b9b-c955-4810-8d4c-f46772c0c88a"
account_path = "/account/c4602b9b-c955-4810-8d4c-f46772c0c88a"

headers = {
    "Authorization": open("starling_credentials.txt", "r").read()
}

today = datetime.today()


def get_spending_category_insight_request_between():
    category_insight_path = "/spending-insights/spending-category/between-two-dates"

    print_request(heroku + accounts_path + category_insight_path)

    datem = datetime(today.year, today.month, today.day)

    params = {
        "firstMonth": "November",
        "firstYear": 2019,
        "secondMonth": calendar.month_name[datem.month],
        "secondYear": datem.year
    }

    r = requests.get(heroku + accounts_path + category_insight_path, headers=headers, params=params)

    print_request_response(r)
    return json.loads(r.text)


def get_balance_request():
    account_balance_path = "https://api.starlingbank.com/api/v2" + accounts_path + "/balance"

    print_request(account_balance_path)

    r = requests.get(account_balance_path, headers=headers)
    print_request_response(r)

    return json.loads(r.text)


def get_statement_since_start_of_month():
    start = str(today.year) + "-" + str(today.month).zfill(2) + "-01"
    end = str(today.year) + "-" + str(today.month).zfill(2) + "-" + str(today.day).zfill(2)

    statement_path = starling_root + accounts_path + "/statement/downloadForDateRange?start={start}&end={end}"\
        .format(start=start, end=end)

    print_request(statement_path)

    r = requests.get(statement_path, headers=headers)

    print_request_response(r)
    return r.content


def get_spending_counter_party_insight_request():
    counter_party_insights_path = starling_root + accounts_path + \
                                  "/spending-insights/counter-party?month={month}&year={year}"\
                                  .format(month=calendar.month_name[today.month].upper(), year=today.year)

    print_request(counter_party_insights_path)

    r = requests.get(counter_party_insights_path, headers=headers)

    print_request_response(r)
    return json.loads(r.text)


def get_savings_goals():
    savings_goal_path = starling_root + account_path + "/savings-goals"
    print_request(savings_goal_path)

    r = requests.get(savings_goal_path, headers=headers)

    print_request_response(r)
    return json.loads(r.text)


def print_request(path):
    print(str(today) + ": Making request to: " + path)


def print_request_response(request):
    print("API Response status: " + str(request.status_code) + separator)
