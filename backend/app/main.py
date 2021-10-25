from typing import Optional

from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from pydantic import BaseModel

import pandas as pd
import requests
from bs4 import BeautifulSoup
from .routers import insider_trades, prices, graph

app = FastAPI()

app.include_router(insider_trades.router)
app.include_router(prices.router)
app.include_router(graph.router)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = False


fake_users_db = {
        "charlie": {
            "username": "charlie",
            "fullname": "charlie kruczko",
            "hashed_password": "fakehashedsecret",
        }
    }


class UserInDB(User):
    hashed_password: str


def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user



@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/ticker/{ticker}")
def get_cik(ticker: str, q: Optional[str] = None):
    cik = '0000'
    return {"ticker": ticker, "q": q, "cik": cik}

@app.get("/ticker/")
def get_ticker_list():
    with open('./backend/data/tickers.txt', 'r') as f:
        tickers = f.read()
    tickers =  tickers.split('\n')
    tickers = list(filter(lambda t: len(t) > 0, tickers))
    tickers = list(map(lambda t: t.rstrip(), tickers))

    tickers = [{"id": i, "ticker": ticker} for i, ticker in enumerate(tickers)]

    return tickers


@app.get("/ticker/{ticker}/summary")
def get_ticker_summary(ticker: str):
    sec_info_url = f"https://sec.report/Ticker/{ticker}"

    header = {
      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
      "X-Requested-With": "XMLHttpRequest"
    }

    r = requests.get(sec_info_url, headers=header)
    soup = BeautifulSoup(r.text, features="lxml")
    return str(soup.find_all("div", "panel-body")[0])

