from .quickstart import *
from email.mime.text import MIMEText
import base64

from apiclient import errors
from string import Template
import json


def send_email(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        print("Message Id: %s" % message['id'])
        return message

    except errors.HttpError as error:
        print("An error occurred: %s" % error)


def get_service():
    if is_credentials():
        return build("gmail", "v1", credentials=return_credentials())
    else:
        return "No credentials found"


def create_message(sender, to, subject, html):
    """Create a message for an email.

    Args:
      sender: Email address of the sender.
      to: Email address of the receiver.
      subject: The subject of the email message.
      html: The text of the email message.

    Returns:
      An object containing a base64url encoded email object.
    """
    message = MIMEText(html, "html")
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}


def create_html_body(data):
    # Loop through net spend array to store values correctly
    net_spend_labels = []
    net_spend_data = []

    balance = "£" + str(int(data["balance"]["clearedBalance"]["minorUnits"])/100)

    for item in data["net_spends"]:
        net_spend_labels.append(item["period"])
        net_spend_data.append(item["net_spend"])

    first_date = net_spend_labels[0]

    sum_net_spend = 0

    for net_spend in net_spend_data:
        sum_net_spend += net_spend

    better_than_last_month = net_spend_data[-1] > net_spend_data[-2]

    title = "Good work :)" if better_than_last_month else "Not quite there :/"
    percent = "{:.2%}".format((net_spend_data[-1] - net_spend_data[-2])/net_spend_data[-2])
    current_month_savings = "{percent} {superlative}".format(percent=percent, superlative="more. Keep up the good work! :)" if better_than_last_month else "less. Keep trying! Things will work out :)")

    highest_spend_category_per_period_labels = []
    highest_spend_category_per_period_data = []

    for item in data["highest_spend_category_per_period"]:
        highest_spend_category_per_period_labels.append(str(item[0][2] + " - " + str(item[0][1])
                                                            .capitalize().replace("_", " ")))
        highest_spend_category_per_period_data.append(str(item[0][0]))

    spend_by_category_this_month_labels = []
    spend_by_category_this_month_data = []

    for item in data["spends_per_category_for_this_month"]:
        spend_by_category_this_month_labels.append(item[1].replace("_", " ").capitalize())
        spend_by_category_this_month_data.append(item[0])

    html_message_string = Template("""
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <style type="text/css">
          @import url("https://fonts.googleapis.com/css2?family=Catamaran:wght@400;800&display=swap");

          * {
            margin: 0;
            order: 0;
            padding: 0;
          }

          body {
            font-family: "Catamaran", sans-serif;
            background-color: #d8dbdb;
            font-size: 18px;
            max-width: 800px;
            margin: 0 auto;
            padding: 2%;
            color: #565859;
          }

          #wrapper {
            background: #f6faff;
          }

          img {
            max-width: 100%;
          }

          .one-col {
            padding: 2%;
          }

          h1 {
            letter-spacing: 1%;
          }

          p {
            text-align: justify;
          }

          .line {
            clear: both;
            height: 2px;
            background-color: #e3e9e9;
            margin: 4% auto;
            width: 96%;
          }

          .two-col {
            float: left;
            width: 46%;
            padding: 2%;
          }

          .contact {
            text-align: center;
            padding-bottom: 3%;
          }

          a {
            color: #607cc3;
            text-decoration: none;
          }

          @media (max-width: 600px) {
            .two-col {
              width: 97%;
            }
          }
          
          .header-col {
            float: right;
            width: 65%;
            padding: 2%;
          }

          .header-image {
            float: left;
            width: 25%;
            padding: 2%;
          }

        </style>
      </head>
      <body style="font-family: &quot;Catamaran&quot;, sans-serif;background-color: #d8dbdb;font-size: 18px;max-width: 800px;margin: 0 auto;padding: 2%;color: #565859;">
        <div id="wrapper" style="background: #f6faff;">
          <div id="banner">
            <img src="https://i.imgur.com/dxTPwJ1.png" alt="illuminati header" style="max-width: 100%;">
          </div>
          <div class="header-image" style="float: left;width: 25%;padding: 2%;">
            <img src="https://quickchart.io/chart?c=
                {type:'radialGauge',data:{datasets:[{data:[${percent}],backgroundColor:'rgba(96,124,195,1)'}]},
                options:{centerArea:{text:'${this_months_net_spend_percent}'}}}" alt="Net spend radial gauge" style="max-width: 100%;">
          </div>

          <div class="header-col" style="float: right;width: 65%;padding: 2%;">
            <h1 style="letter-spacing: 1%;">${title}</h1>
            <p style="text-align: justify;">
              Compared to last month, you saved ${current_month_savings}. You saved £${this_months_net_spend} this month,
              and £${sum_net_spend} since ${first_date}. 🤑
            </p>
            <p style="text-align: justify;">Your current balance is ${balance}. Don't spend it all at once!</p>
            <p>
              You're saving for ${savings_goal}: only £${savings_goal_amount_left}
              to go! :)
            </p>
          </div>
          <div class="line" style="clear: both;height: 2px;background-color: #e3e9e9;margin: 4% auto;width: 96%;"></div>
          <div class="two-col" style="float: left;width: 46%;padding: 2%;">
            <h2>Net spend over time</h2>
            <img src="https://quickchart.io/chart?width=500&height=300&c=
                {type:'line',data:{labels:${net_spend_labels}, 
                datasets:[{label:'Net Spend',data:${net_spend_data}, fill:false, borderColor:'rgba(96, 195, 170, 1)'}]}}" alt="Net spend over time" style="max-width: 100%;">
            <p style="text-align: justify;">Net spend is the net of any money going in or out of my current account. This includes everything: 
            bills, rent, deliveroos, video games purchases... Everything.</p>
          </div>
          <div class="two-col" style="float: left;width: 46%;padding: 2%;">
            <h2>Highest expense category over time</h2>
        <img
          src="https://quickchart.io/chart?width=500&height=300&c=
          {type:'bar', 
          data: { labels: ${highest_spend_category_per_period_labels}, 
          datasets: [{ label: 'Spending per category',
          backgroundColor:'rgba(62, 149, 205, 1)',
          data: ${highest_spend_category_per_period_data}, }] }}"
          alt="Highest spend category over time"
        />
            <p style="text-align: justify;">This is the category for which you've spent the most money. If you see this reducing over time, 
            then that's great! You're controlling yourself more. If not... well, it happens.</p>
          </div>
          <div class="two-col">
            <h2>Where you spent the most</h2>
            <img alt="counter party where I've spent the most this month" />
            <p>
              This is the places where you've spent the most money this month. Maybe
              try to go easy on the deliveroos if you can?
            </p>
          </div>
          <div class="two-col">
            <h2>Spend by category this month</h2>
            <img src="https://quickchart.io/chart?width=500&height=300&c=
              {type:'bar', 
              data: { labels: ${spend_by_category_this_month_labels}, 
              datasets: [{ label: 'Spending per category this month',
              backgroundColor:'rgba(62, 149, 205, 1)',
              data: ${spend_by_category_this_month_data}, }] }}" style="max-width: 100%;" alt="Spend by category this month" />
            <p>
              This is how much you've spent for every category this month. Try to
              see if you can save on those bigger categories!
            </p>
          </div>
          <div class="line" style="clear: both;height: 2px;background-color: #e3e9e9;margin: 4% auto;width: 96%;"></div>
          <p class="contact" style="text-align: center;padding-bottom: 3%;">
            <a href="https://leolebleis.com/" target="_blank" style="color: #607cc3;text-decoration: none;">Made by Leo Le Bleis.
            <br>
            </a><a href="https://github.com/Leolebleis/starling-insights-api" target="_blank" style="color: #607cc3;text-decoration: none;">Check out the repo!
          </a></p>
        </div>
        <!-- End of wrapper -->
      </body>
    </html>
    """).safe_substitute(this_months_net_spend=net_spend_data[-1],
                         percent=float(percent.replace("%", "")),
                         this_months_net_spend_percent=percent.replace("%", ""),
                         current_month_savings=current_month_savings,
                         title=title,
                         net_spend_labels=str(net_spend_labels).replace(" ", ""),
                         net_spend_data=str(net_spend_data).replace(" ", ""),
                         sum_net_spend=sum_net_spend,
                         first_date=first_date,
                         highest_spend_category_per_period_labels=highest_spend_category_per_period_labels,
                         highest_spend_category_per_period_data=highest_spend_category_per_period_data,
                         balance=balance,
                         spend_by_category_this_month_labels=spend_by_category_this_month_labels,
                         spend_by_category_this_month_data=spend_by_category_this_month_data,
                         savings_goal=savings_goal,
                         savings_goal_amount_left=savings_goal_amount_left
                         )

    # CSS in-liner: https://templates.mailchimp.com/resources/inline-css/

    return str(html_message_string).replace("\n", "")
