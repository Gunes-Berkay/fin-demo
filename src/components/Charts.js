// TradingViewWidget.jsx
import React, { useEffect, useRef, memo, useState } from 'react';


function TradingViewWidget() {
  const container = useRef();
  let isScriptAdded = useRef(false);
  const exchanges = ["BINANCE", "OKX", "BIST"];
  const [watchList, setWatchList] = useState([]);


  const coins = [
    "BINANCE:BTCUSDT", "BINANCE:ETHUSDT", "BINANCE:XRPUSDT", "BINANCE:SOLUSDT", "BINANCE:BNBUSDT", "BINANCE:DOGEUSDT", 
    "BINANCE:ADAUSDT", "BINANCE:TRXUSDT", "BINANCE:LINKUSDT", "BINANCE:AVAXUSDT", "BINANCE:XLMUSDT", "BINANCE:TONUSDT", 
    "BINANCE:HBARUSDT", "BINANCE:SUIUSDT", "BINANCE:SHIBUSDT", "BINANCE:DOTUSDT", "BINANCE:LEOUSDT", "BINANCE:LTCUSDT", 
    "BINANCE:BGBUSDT", "BINANCE:BCHUSDT", "BINANCE:HYPEUSDT", "BINANCE:UNIUSDT", "BINANCE:USDeUSDT", "BINANCE:TRUMPUSDT", 
    "BINANCE:DAIUSDT", "BINANCE:PEPEUSDT", "BINANCE:NEARUSDT", "BINANCE:AAVEUSDT", "BINANCE:ONDOUSDT", "BINANCE:OMUSDT", 
    "BINANCE:APTUSDT", "BINANCE:ICPUSDT", "BINANCE:XMRUSDT", "BINANCE:TAOUSDT", "BINANCE:ETCUSDT", "BINANCE:MNTUSDT", 
    "BINANCE:VETUSDT", "BINANCE:CROUSDT", "BINANCE:POLUSDT", "BINANCE:OKBUSDT", "BINANCE:KASUSDT", "BINANCE:ALGOUSDT", 
    "BINANCE:RENDERUSDT", "BINANCE:FILUSDT", "BINANCE:ARBUSDT", "BINANCE:FETUSDT", "BINANCE:ATOMUSDT", "BINANCE:GTUSDT"
  ];
  
  //const [watchList, setWatchList] = useState([]);
  //const [indicators, setIndicators] = useState([]);

  //const new_coin_list = coin_list.map((coin)=>)
    const coin = "BINANCE:XAIUSDT";

 
  



    useEffect(
      () => {
        const script = document.createElement("script");
        script.src = "https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js";
        script.type = "text/javascript";
        script.async = true;
        script.innerHTML = JSON.stringify({
          width: "1980",
          height: "810",
          symbol: "BINANCE:BTCUSDT",
          interval: "240",
          timezone: "Europe/Istanbul",
          theme: "dark",
          style: "1",
          locale: "tr",
          withdateranges: true,
          hide_side_toolbar: false,
          allow_symbol_change: true,
          watchlist: coins,
          details: true,
          hotlist: true,
          calendar: false,
          studies: [
            "STD;24h%Volume",
            "STD;2030"
          ],
          support_host: "https://www.tradingview.com"
        });
        
        container.current.appendChild(script);
      },
      []
    );

  return (
    <div className="tradingview-widget-container" ref={container} >
      <div>
        <button id='add_to_watchlist'></button>
      </div>
      <div className="tradingview-widget-container__widget" ></div>
      
    </div>
  );
}

export default memo(TradingViewWidget);
