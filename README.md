# BinanceNotifier
BinanceNotifier is an optionally containerised python script that watches your [Binance](https://accounts.binance.com/en/register?ref=158612165) orders and notifies you if there's a change via [Apprise](https://github.com/caronc/apprise) to just about any notification service, such as Pushover, Pushbullet, Discord, Gotify, etc.

It can also send you a notification with your current estimated account balance. Please note that it might deviate slightly from the view in [Binance](https://accounts.binance.com/en/register?ref=158612165)  but is arguably a more realistic figure. 

## Setup
By far the easiest way to run this is via [Docker](https://docker.com), an example `docker run` statement is provided below. 

Most of the environment variables are self explanatory, the only serious limitation is that the [Binance API](https://binance-docs.github.io/apidocs/#general-info) only allows you to pull orders for one* ticker at a time (eg. `ETHUSD`). You can currently get around this by creating multiple containers, but I'd recommend only enabling balance alerts for one of them. Also please note that order info requests are made one every second at a [weight](https://www.binance.com/en/support/faq/360004492232#:~:text=Hard-Limits:) of `5`.

There is one slightly confusing environment variable: `NOTIFIER_PROTOCOL`. An example value, and the one used throughout this readme, is `pover` which corresponds to [Pushover](https://pushover.net/). Other example values can be found on the [Apprise readme](https://github.com/caronc/apprise#popular-notification-services). This project is currently untested with services other than Pushover, but most other services should work with minimal changes to `start.py`.

To enable balance alerts, simply set the `CURRENCY` variable to a currency supported by Binance (AUD, EUR, USD, GBP) and the `BALANCE_ALERT` variable to an interval in seconds (eg. setting `3600` would send a notification once per hour.)

<sub> *To be specific, the Binance API *does* allow you to request all open orders, but with a `weight` of `40`, which is basically unusable for a near instantaneous API monitor and would make this the only project you could use that relied on the Binance API. The total `weight` limit is `1200` per minute, this project makes 1 request per second & several for the balance check, which would mean a `weight` likely in excess of `2400` per minute.</sub>

### Docker
Here is an example `docker run` command, make sure you fill in the blank API variables before running it otherwise it will error out.
```
docker run -ti --name binancenotifier \
       --env BINANCE_API_KEY=x \
       --env BINANCE_API_SECRET=x \
       --env BINANCE_TICKER=VOXELUSDT \
       --env NOTIFIER_API_APP=x \
       --env NOTIFIER_API_USER=x \
       --env NOTIFIER_PROTOCOL=pover \
       --env BINANCE_TICKER=VOXELUSDT \
       --env CURRENCY=AUD \
       --env BALANCE_ALERT=3600 \
       lnxd/binancenotifier
```

### Local Installation
I wouldn't recommend taking this path unless you really can't use Docker and there's no alternatives, but only because it's messy. I also haven't tested it, but there's little to no reason it shouldn't work.

1. Make sure you have [Python](https://www.python.org/) (versions other than 3.8 are untested), and a recent version of [pip](https://pypi.org/project/pip/) installed 
2. Clone this git somewhere `git clone https://github.com/lnxd/docker-binancenotifier`, or download and extract the master zip
3. Install the dependencies `pip install --prefix=/install -r requirements.txt`
4. Set the environment variables manually:
```
BINANCE_API_KEY=x
BINANCE_API_SECRET=x
BINANCE_TICKER=VOXELUSDT
NOTIFIER_API_APP=x
NOTIFIER_API_USER=x
NOTIFIER_PROTOCOL=pover
BINANCE_TICKER=VOXELUSDT
CURRENCY=AUD
BALANCE_ALERT=3600
```
5. Start the monitor with `python start.py`

## Donations
If this project helps you in some way, please consider making a donation to support my future work. Instructions can be found by clicking [here](https://github.com/lnxd#donations). Additionally, if you don't have a Binance account, [this](https://accounts.binance.com/en/register?ref=158612165) is my referral link which doesn't cost you anything to use, but would give me a commission on your trade fees.

Thank you