def get_highest_spend_category_per_period(data):
    highest_spend_category_per_period_labels = []
    highest_spend_category_per_period_data = []

    for item in data:
        highest_spend_category_per_period_labels.append(str(item[2] + " - " + str(item[1])
                                                            .capitalize().replace("_", " ")))
        highest_spend_category_per_period_data.append(str(item[0]))

    return[highest_spend_category_per_period_labels, highest_spend_category_per_period_data]


def get_net_spends(data):
    net_spend_labels = []
    net_spend_data = []

    for item in data:
        net_spend_labels.append(item["period"])
        net_spend_data.append(item["net_spend"])

    return [net_spend_labels, net_spend_data]


def get_balance(data):
    return "£" + str(int(data["clearedBalance"]["minorUnits"])/100)


def get_spend_by_category_this_month(data):
    spend_by_category_this_month_labels = []
    spend_by_category_this_month_data = []

    for item in data:
        spend_by_category_this_month_labels.append(item[1].replace("_", " ").capitalize())
        spend_by_category_this_month_data.append(item[0])

    return [spend_by_category_this_month_labels, spend_by_category_this_month_data]


def get_spend_per_party_this_month(data):
    spend_per_party_this_month_labels = []
    spend_per_party_this_month_data = []

    for item in data:
        spend_per_party_this_month_labels.append(item["counterPartyName"])
        spend_per_party_this_month_data.append(item["netSpend"])

    return [spend_per_party_this_month_labels, spend_per_party_this_month_data]