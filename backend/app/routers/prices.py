import yfinance as yf
from datetime import date

from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_token_header

router = APIRouter(dependencies=[Depends(get_token_header)])

def get_daily_price_df(ticker: str):
    # Set the start and end date
    start_date = '1990-01-01'
    today = str(date.today())
    # Set the ticker
    end_date = today

    # Get the data
    data = yf.download(ticker, start_date, end_date)
    assert len(data) > 0
    return data

@router.get("/ticker/{ticker}/price/daily")
def get_price_daily(ticker: str):
    data = get_daily_price_df(ticker)
    return data.reset_index().to_dict(orient="records")
