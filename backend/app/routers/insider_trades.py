import pandas as pd

from fastapi import APIRouter
router = APIRouter()

@router.get("/ticker/{ticker}/insider_trades")
def get_ticker_insider_trades(ticker: str):
    url = f"http://openinsider.com/search?q={ticker}#results"
    dfs = pd.read_html(url)
    df = list(filter(lambda _df: "Value" in _df.columns, dfs))[0]
    df = df.dropna(axis=1)
    return df.to_dict(orient="records")
