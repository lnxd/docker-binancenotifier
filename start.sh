# This file is really only useful for testing code, but it will
# get you started. That said, you'll be much better off setting 
# up dockerMan or docker-compose

echo "-- Stopping --"
docker stop binancenotifier || true
echo "-- Cleaning --"
docker rm binancenotifier || true
echo "-- Building --"
docker build . -t lnxd/binancenotifier
echo "-- Running --"
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