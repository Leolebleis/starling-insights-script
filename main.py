__author__ = "Leo Le Bleis"
__version__ = "0.1.0"

import operator
from gmail.email_service import *
from enum import Enum
from client.starling_client import *

subject_line = "Spending breakdown | " + str(calendar.month_name[today.month])


def main():
    # Main entry point of the app
    print(separator)
    data = get_spending_category_insight_request_between()

    data.sort(key=operator.itemgetter("period"))

    spending_by_category = get_spending_by_category(data)

    data = {
        "net_spends": get_net_spends(data),
        "spends_by_category": spending_by_category,
        "highest_spend_category_per_period": get_highest_spend_category_per_period(spending_by_category),
        "balance": get_balance_request(),
        "spends_per_category_for_this_month": get_spends_per_category_for_period(spending_by_category, str(today.year) +
                                                                                 "-" + str(today.month).zfill(2)),
        "counter_party_current_month": get_spending_counter_party_insight_request(),
        "savings_goals": get_savings_goals()
    }

    html_message = create_html_body(data)

    message = create_message("me", "leo.lebleis@gmail.com", subject_line, html_message, attachment=get_statement_since_start_of_month())
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
    data = [i for i in data if i[1] != "HOME"]

    min_spends = []

    for period in period_list:
        sorted_list = [a for a in data if a[2] == period]
        min_spend = min(i[0] for i in sorted_list)
        min_spends.append([i for i in sorted_list if i[0] == min_spend][0])

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


if __name__ == "__main__":
    # This is executed when run from the command line
    main()
