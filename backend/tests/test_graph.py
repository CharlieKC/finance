import pytest


@pytest.mark.parametrize("ticker", ["GME"])
def test_graph(client, ticker):
    res = client.get(f"/ticker/{ticker}/price/daily/graph")
    assert res.status_code == 200
    

