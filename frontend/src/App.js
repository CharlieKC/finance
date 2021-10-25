import React, { useEffect, useState } from "react";
// import logo from './logo.svg';
import './App.css';

function TickerSummary(props) {
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [summary, setSummary] = useState([]);

  // Note: the empty deps array [] means
  // this useEffect will run once
  // similar to componentDidMount()
  useEffect(() => {
    fetch("http://localhost:8000/ticker/" + props.selectedTicker + "/summary/")
      .then(res => res.json())
      .then(
        (result) => {
          setIsLoaded(true);
          setSummary(result);
        },
        // Note: it's important to handle errors here
        // instead of a catch() block so that we don't swallow
        // exceptions from actual bugs in components.
        (error) => {
          setIsLoaded(true);
          setError(error);
        }
      )
  }, [props.selectedTicker])

  if (error) {
    return <div>Error: {error.message}</div>;
  } else if (!isLoaded) {
    return <div>Loading...</div>;
  } else {
    return <div className="summary">
        <h1>Summary</h1>
        <div className="content" dangerouslySetInnerHTML={{__html: summary}}></div>
      </div>
  }

}

function TickerInsiderTrades(props) {
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [trades, setTrades] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/ticker/" + props.selectedTicker + "/insider_trades/")
      .then(res => res.json())
      .then(
        (result) => {
          setIsLoaded(true);
          setTrades(result);
        },
        (error) => {
          setIsLoaded(true);
          setError(error);
        }
      )
  }, [props.selectedTicker])

  if (error) {
    return <div>Error: {error.message}</div>;
  } else if (!isLoaded) {
    return <div>Loading...</div>;
  } else {
    return <div className="summary">
        <h1>InsiderTrades</h1>
        <div className="content" dangerouslySetInnerHTML={{__html: trades}}></div>
      </div>
  }

}

function Tickers(props) {
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [items, setItems] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/ticker/")
      .then(res => res.json())
      .then(
        (result) => {
          setIsLoaded(true);
          setItems(result);
        },
        (error) => {
          setIsLoaded(true);
          setError(error);
        }
      )
  }, [])

  if (error) {
    return <div>Error: {error.message}</div>;
  } else if (!isLoaded) {
    return <div>Loading...</div>;
  } else {
    return (
      <ul>
        {items.map(item => (
          <li key={item.id}>
            <button onClick={function() {props.setSelectedTicker(item.ticker)}}> {item.ticker} </button>
          </li>
        ))}
      </ul>
    );
  }
}

function Graph(props) {
    return <h1>The Graph! - {props.selectedTicker} </h1>
}



function App() {
  const [selectedTicker, setSelectedTicker] = useState("AAPL");


  return (
    <div className="App">
        <Graph selectedTicker={selectedTicker}></Graph>
        <TickerSummary selectedTicker={selectedTicker}></TickerSummary>
        <TickerInsiderTrades selectedTicker={selectedTicker}></TickerInsiderTrades>
        <Tickers setSelectedTicker={setSelectedTicker}></Tickers>
    </div>
  );
}

export default App;

