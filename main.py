__author__ = "Leo Le Bleis"
__version__ = "0.1.0"

import requests
import operator
from datetime import datetime
import calendar
from gmail.email_service import *
from enum import Enum

separator = "\n------------------------\n"
heroku = "https://starling-insights-api.herokuapp.com"
accounts_path = "/accounts/c4602b9b-c955-4810-8d4c-f46772c0c88a"

headers = {
    "Authorization": open("starling_credentials.txt", "r").read()
}

today = datetime.today()
subject_line = "Spending breakdown | " + str(calendar.month_name[today.month])


def main():
    # Main entry point of the app
    print(separator)
    data = get_spending_category_insight_request()

    data.sort(key=operator.itemgetter("period"))

    spending_by_category = get_spending_by_category(data)

    data = {
        "net_spends": get_net_spends(data),
        "spends_by_category": spending_by_category,
        "highest_spend_category_per_period": get_highest_spend_category_per_period(spending_by_category),
        "balance": get_balance_request(),
        "spends_per_category_for_this_month": get_spends_per_category_for_period(spending_by_category,str(today.year) +
                                                                                 "-" + str(today.month).zfill(2))
    }

    html_message = create_html_body(data)

    message = create_message("me", "leo.lebleis@gmail.com", subject_line, html_message)
    send_email(get_service(), "me", message)


class Category(Enum):
    SHOPPING = "SHOPPING",
    EATING_OUT = "EATING_OUT",
    GROCERIES = "GROCERIES",
    PAYMENTS = "PAYMENTS",
    TRANSPORT = "TRANSPORT",
    BILLS_AND_SERVICES = "BILLS_AND_SERVICES",
    ENTERTAINMENT = "ENTERTAINMENT"
    INCOME = "INCOME"
    GENERAL = "GENERAL"
    CHARITY = "CHARITY"
    HOLIDAYS = "HOLIDAYS"


def get_category_spends(data):
    period_list = []

    for category_spend in data:
        if category_spend[2] not in period_list:
            period_list.append(category_spend[2])
    return period_list


def get_spends_per_category_for_period(data, period):
    return sorted([a for a in data if a[2] == period], key=operator.itemgetter(0), reverse=True)


def get_highest_spend_category_per_period(data):
    period_list = get_category_spends(data)

    min_spends = []

    for period in period_list:
        sorted_list = [a for a in data if a[2] == period]

        min_spend = min(i[0] for i in sorted_list)
        min_spends.append([i for i in sorted_list if i[0] == min_spend])

    return min_spends


def get_spending_by_category(data):
    spends_by_category = []

    for item in data:
        item_date = item["period"]
        for category_breakdown in item["breakdown"]:
            category_spend = category_breakdown["netSpend"] if \
                category_breakdown["netDirection"] == "IN" else \
                0 - category_breakdown["netSpend"]

            spend_category = category_breakdown["spendingCategory"]

            spends_by_category.append([category_spend, spend_category, item_date])

    return spends_by_category


def get_net_spends(data):
    net_spends = []

    for item in data:
        net_spends.append(
            {"net_spend": item['netSpend'], "period": item['period']} if
            item['direction'] == "IN" else
            {"net_spend": 0 - item['netSpend'], "period": item['period']})

    return net_spends


def get_balance_request():
    account_balance_path = "https://api.starlingbank.com/api/v2" + accounts_path + "/balance"

    print(str(today) + ": Making request to: " + account_balance_path)

    r = requests.get(account_balance_path, headers=headers)
    print("API Response status: " + str(r.status_code) + separator)

    return json.loads(r.text)


def get_spending_category_insight_request():
    category_insight_path = "/spending-insights/spending-category/between-two-dates"

    print(str(today) + ": Making request to: " + heroku + accounts_path + category_insight_path)

    datem = datetime(today.year, today.month, today.day)

    params = {
        "firstMonth": "November",
        "firstYear": 2019,
        "secondMonth": calendar.month_name[datem.month],
        "secondYear": datem.year
    }

    r = requests.get(heroku + accounts_path + category_insight_path, headers=headers, params=params)

    print("API Response status: " + str(r.status_code) + separator)
    return json.loads(r.text)


if __name__ == "__main__":
    # This is executed when run from the command line
    main()
