import pandas as pd
import plotly.graph_objects as go
from .prices import get_daily_price_df
from ..dependencies import get_token_header

from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(dependencies=[Depends(get_token_header)])
# router = APIRouter()

def heishkin_ashi_df(df):
    #assigning existing columns to new variable HAdf
    HAdf = df[['OPEN', 'HIGH', 'LOW', 'CLOSE']]

    HAdf['CLOSE'] = round(((df['OPEN'] + df['HIGH'] + df['LOW'] + df['CLOSE'])/4),2)
    #round function to limit results to 2 decimal places

    for i in range(len(df)):
        if i == 0:
            HAdf.iat[0,0] = round(((df['OPEN'].iloc[0] + df['CLOSE'].iloc[0])/2),2)
        else:
            HAdf.iat[i,0] = round(((HAdf.iat[i-1,0] + HAdf.iat[i-1,3])/2),2)


    #Taking the Open and Close columns we worked on in Step 2 & 3
    #Joining this data with the existing HIGH/LOW data from df
    #Taking the max value in the new row with columns OPEN, CLOSE, HIGH
    #Assigning that value to the HIGH/LOW column in HAdf

    HAdf['HIGH'] = HAdf.loc[:,['OPEN', 'CLOSE']].join(df['HIGH']).max(axis=1)
    HAdf['LOW'] = HAdf.loc[:,['OPEN', 'CLOSE']].join(df['LOW']).min(axis=1)

    return HAdf

@router.get('/ticker/{ticker}/price/daily/graph')
def get_daily_price_graph(ticker: str):
    price_df = get_daily_price_df(ticker)
    ha_df = heishkin_ashi_df(price_df)

    fig = go.Figure(data=[go.Candlestick(x=ha_df.index,
                open=ha_df.OPEN,
                high=ha_df.HIGH,
                low=ha_df.LOW,
                close=ha_df.CLOSE)])


    fig.update_layout(
              title = 'Heikin Ashi Chart: RELIANCE',
              xaxis_title = 'Date',
              yaxis_title = 'Price')

    return fig



