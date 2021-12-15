#!/usr/bin/env python3

from apprise import Apprise
from binance.client import Client
from os import environ    
from time import sleep
from my_class import BinanceAPI

def notify(message):
    # Sends notification via Apprise

    appriseClient.notify(
        body=message,
        title='BinanceNotifier',
    )
    print("Notification sent")

def get_currency_config():
     # Currency config
    try:
        currency = environ['CURRENCY']
    except KeyError:
        currency = ""
    supported_currencies = ["AUD", "EUR", "GBP", "USD"] 
    # At present, these are the only currencies the Binance API seems to support
    if currency not in supported_currencies:
        print("-- Warning: You did not give a supported currency, defaulting to AUD --")
        currency = "AUD"
    return currency

def get_balance_alert_config(request):
    # If balance_alert can be set to an integer, enable feature, otherwise disable it
    try:
        balance_alert_schedule = int(balance_alert)
        balance_alert_enabled  = True
    except ValueError:
        balance_alert_schedule = 0
        balance_alert_enabled  = False
    if request == "schedule":
        return balance_alert_schedule
    if request == "enabled":
        return balance_alert_enabled

def get_balance():
    # Returns total account balance in selected currency

    # Create an object using nedludd0's class and use it to get total balances
    nedludd0Client = BinanceAPI(p_api_pub_key = binance_api_key, p_api_secret_key = binance_api_secret, p_wallet = 'spot')
    balance_total = nedludd0Client.account_get_balance_total()

    if currency == "USD":
        # Ticker BTCUSD does not exist, and nedludd0's BinanceAPI class has its own way to calculate this
        total_converted = balance_total[1][0].get('totals').get('tot_usd')
    else:
        # If USD is not the currency, do the calculation manually
        # Calculate total balance in BTC
        total_btc = balance_total[1][0].get('totals').get('tot_btc')
        total_btc = float(total_btc)
        five_minute_average = binanceClient.get_avg_price(**{'symbol': 'BTC' + currency})["price"]
        five_minute_average = float(five_minute_average)
        total_converted = total_btc*five_minute_average
    
    print("Total balance in " + currency + ": " + str(format(total_converted, '.2f')))
    return total_converted

def check(orders):
    # Categorises orders into two groups
    # complete_orders: Orders that have been completed (filled or cancelled)
    # pending_orders: Orders that are currently in progress (unfilled)

    for order in all_orders:
        known = False
        # `known` variable allows function to remember whether it has seen an order before

        for pending in pending_orders:
            if order["orderId"] == pending["orderId"]:
                known = True

                if order["status"] == "FILLED":
                    # Notify if an order is filled
                    notify("Order filled! " + str(float(order["executedQty"])) + "@" + str(float(order["price"])))
                    print("Order " + str(order["orderId"]) + " filled")
                elif order["status"] == "CANCELED":
                    # Notify if an order is cancelled
                    notify("Order " + str(order["orderId"]) + " cancelled successfully")
                    print("Order " + str(order["orderId"]) + " cancelled")

                if order["status"] != "NEW":
                    # To be performed if an order's in the pending_orders array had a change in status
                    print("Categorised " + str(order["orderId"]) + " as completed")
                    complete_orders.append(order)
                    for i in range(len(pending_orders)):
                        # This needs some work, other options gave errors
                        if pending_orders[i]["orderId"] == order["orderId"]:
                            del pending_orders[i]
                            break

        for complete in complete_orders:
            if order["orderId"] == complete["orderId"]:
                # If an order is known, do nothing
                known = True
        if not known:
            if order["status"] != "NEW":
                # For orders that aren't pending, categorise as completed
                print("Categorised " + str(order["orderId"]) + " as completed")
                complete_orders.append(order)
            elif order["status"] == "NEW":
                # For orders that are't pending, categorise as such
                print("Categorised " + str(order["orderId"]) + " as pending")
                pending_orders.append(order)
                if not initial_run:
                    # If this isn't the first loop, notify about order creation
                    notify("Order " + str(order["orderId"]) + " created successfully")

if __name__ == "__main__":
    # Configuration variables
    binance_api_key        = environ['BINANCE_API_KEY']
    binance_api_secret     = environ['BINANCE_API_SECRET']
    binance_ticker         = environ['BINANCE_TICKER']
    notifier_api_app       = environ['NOTIFIER_API_APP']
    notifier_api_user      = environ['NOTIFIER_API_USER']
    notifier_protocol      = environ['NOTIFIER_PROTOCOL']
    balance_alert          = environ['BALANCE_ALERT']
    currency               = get_currency_config()
    balance_alert_schedule = get_balance_alert_config("schedule")
    balance_alert_enabled  = get_balance_alert_config("enabled")

    
    print("-- Preparing --")
    # Create objects
    binanceClient = Client(binance_api_key, binance_api_secret)
    appriseClient = Apprise()
    appriseClient.add(notifier_protocol + "://" + notifier_api_user + '@' + notifier_api_app)

    if balance_alert_enabled:
        print("Balance alert is enabled and set to run every " + str(balance_alert_schedule) + " seconds")
        print("Currency is set to " + currency)
    else:
        print("Balance alert is disabled")

    print("-- Monitoring trades --")
    # Start monitoring
    pending_orders  = []
    complete_orders = []
    initial_run = True
    loops = 0
    while True:
        all_orders = binanceClient.get_all_orders(symbol=binance_ticker)
        check(all_orders)
        initial_run = False
        sleep(1) # Can be changed if near instant notifications aren't necessary, and you're making too many API requests
        loops += 1
        if loops%1800 == 0:
            # Display "something" in the terminal so that users know it's still working
            print("-- Still monitoring --")
        if balance_alert_enabled:
            if loops%balance_alert_schedule == 0:
                # Send current wallet balance
                print("-- Performing balance check --")
                notify("Balance: " + str(format(get_balance(), '.2f')) + " " + currency)
                print("Balance notification sent")
