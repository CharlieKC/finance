import pytest

def get_tickers():
    with open('./data/tickers.txt', 'r') as f:
        tickers = f.read()
    tickers =  tickers.split('\n')
    tickers = list(filter(lambda t: len(t) > 0, tickers))
    tickers = list(map(lambda t: t.rstrip(), tickers))
    return tickers

tickers = get_tickers()[:10]

def write_success(file, ticker):
    with open(file, 'a') as f:
        f.write(ticker + '\n')

def test_read_main(client):
    res = client.get('/')
    assert res.status_code == 200
    assert res.json() == {"Hello": "World"}

def test_read_tickers(client):
    res = client.get('/ticker/')
    tickers = res.json()
    assert isinstance(tickers, list)

@pytest.mark.parametrize("ticker", tickers)
def test_read_price_daily(client, ticker):
    res = client.get(f'/ticker/{ticker}/price/daily/')
    assert res.status_code == 200
    prices = res.json()
    assert isinstance(prices, list)
    assert isinstance(prices[0], dict)
    write_success('data/tickers_with_price.txt', ticker)

@pytest.mark.parametrize("ticker", tickers)
def test_read_ticker_summary(client, ticker):
    res = client.get(f'/ticker/{ticker}/summary')
    assert res.status_code == 200
    assert isinstance(res.text, str)
    write_success('data/tickers_with_summary.txt', ticker)


@pytest.mark.parametrize("ticker", tickers)
def test_read_ticker_insider_trades(client, ticker):
    res = client.get(f'/ticker/{ticker}/insider_trades')
    assert res.status_code == 200
    insider_trades = res.json()
    assert isinstance(insider_trades, list)
    write_success('data/tickers_with_insider_trades.txt', ticker)
