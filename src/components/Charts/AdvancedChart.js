// TradingViewWidget.jsx
import React, { useEffect, useRef, memo } from 'react';

function TradingViewWidget( { symbol, watchlist, indicators } ) {
  const container = useRef(null);

//   const studiesas= [
//     "STD;24h%Volume",
//     "STD;Accumulation_Distribution",
//     "STD;Advance%1Decline%1Line",
//     "STD;Advance%1Decline%1Ratio",
//     "STD;Advance_Decline_Ratio_Bars",
//     "STD;Arnaud%1Legoux%1Moving%1Average",
//     "STD;Aroon",
//     "STD;Average%Day%Range",
//     "STD;Average%1Directional%1Index",
//     "STD;Average_True_Range",
//     "STD;Awesome_Oscillator",
//     "STD;Balance%1of%1Power",
//     "STD;BBTrend",
//     "STD;Bollinger_Bands",
//     "STD;Bollinger_Bands_B",
//     "STD;Bollinger_Bands_Width",
//     "STD;Bollinger%1Bars",
//     "STD;Bull%Bear%Power",
//     "STD;Chaikin_Money_Flow",
//     "STD;Chaikin_Oscillator",
//     "STD;Chande%1Kroll%1Stop",
//     "STD;Chande_Momentum_Oscillator",
//     "STD;Chop%1Zone",
//     "STD;Choppiness_Index",
//     "STD;CCI",
//     "STD;Connors_RSI",
//     "STD;Coppock%1Curve",
//     "CorrelationCoefficient@tv-basicstudies",
//     "STD;Correlation_Coeff",
//     "STD;Cumulative%1Volume%1Delta",
//     "STD;Cumulative%1Volume%1Index",
//     "STD;DPO",
//     "STD;DMI",
//     "STD;Donchian_Channels",
//     "STD;DEMA",
//     "STD;EOM",
//     "STD;EFI",
//     "STD;ENV",
//     "STD;Fisher_Transform",
//     "STD;Gaps",
//     "STD;Historical_Volatility",
//     "STD;Hull%1MA",
//     "STD;Ichimoku%1Cloud",
//     "STD;Keltner_Channels",
//     "STD;Klinger%1Oscillator",
//     "STD;Know_Sure_Thing",
//     "STD;Least%1Squares%1Moving%1Average",
//     "STD;Linear_Regression",
//     "STD;MA%1Cross",
//     "STD;Mass%1Index",
//     "STD;McGinley%1Dynamic",
//     "STD;Median",
//     "STD;Momentum",
//     "STD;Money_Flow",
//     "MoonPhases@tv-basicstudies",
//     "STD;Moon%1Phases",
//     "STD;MACD",
//     "STD;EMA",
//     "STD;MA%Ribbon",
//     "STD;SMA",
//     "STD;WMA",
//     "STD;Multi-Time%Period%Charts",
//     "STD;Net%1Volume",
//     "STD;On_Balance_Volume",
//     "STD;Open%Interest",
//     "STD;PSAR",
//     "STD;Performance",
//     "STD;Pivot%1Points%1High%1Low",
//     "STD;Pivot%1Points%1Standard",
//     "STD;Price_Oscillator",
//     "STD;Price%1Target",
//     "PriceVolumeTrend@tv-basicstudies",
//     "STD;Price_Volume_Trend",
//     "STD;Rank_Correlation_Index",
//     "STD;ROC",
//     "STD;RCI_Ribbon",
//     "STD;RSI",
//     "STD;Relative_Vigor_Index",
//     "STD;Relative_Volatility_Index",
//     "STD;Relative%1Volume%1at%1Time",
//     "BookerIntradayPivots@tv-basicstudies",
//     "BookerKnoxvilleDivergence@tv-basicstudies",
//     "BookerMissedPivots@tv-basicstudies",
//     "BookerReversal@tv-basicstudies",
//     "STD;Rob%1Booker%1Ghost%1Pivots%1v2",
//     "STD;Divergence%1Indicator",
//     "STD;Seasonality",
//     "STD;SMI_Ergodic_Indicator_Oscillator",
//     "STD;SMI_Ergodic_Oscillator",
//     "STD;Smoothed%1Moving%1Average",
//     "STD;Stochastic",
//     "STD;SMI",
//     "STD;Stochastic_RSI",
//     "STD;Supertrend",
//     "STD;Technical%1Ratings",
//     "STD;Time%1Weighted%1Average%1Price",
//     "STD;Trading%1Sessions",
//     "STD;Trend%1Strength%1Index",
//     "STD;TEMA",
//     "STD;TRIX",
//     "STD;True%1Strength%1Indicator",
//     "STD;Ultimate_Oscillator",
//     "STD;UP_DOWN_Volume",
//     "STD;Visible%1Average%1Price",
//     "STD;Volatility_Stop",
//     "Volume@tv-basicstudies",
//     "STD;Volume%1Delta",
//     "STD;Volume%1Oscillator",
//     "STD;VWAP",
//     "STD;VWMA",
//     "STD;Vortex%1Indicator",
//     "STD;Williams_Alligator",
//     "STD;Whilliams_Fractals",
//     "STD;Willams_R",
//     "STD;Woodies%1CCI",
//     "STD;Zig_Zag"
//   ]

  useEffect(
    () => {
      const script = document.createElement("script");
      script.src = "https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js";
      script.type = "text/javascript";
      script.async = true;
      script.innerHTML =JSON.stringify({
        symbol: "BINANCE:"+symbol ,
        interval: "240",
        timezone: "Europe/Istanbul",
        theme: "dark",
        style: "1",
        locale: "tr",
        withdateranges: true,
        hide_side_toolbar: false,
        allow_symbol_change: true,
        watchlist: watchlist,
        studies : indicators,
        details: true,
        hotlist: true,
        calendar: false,
        show_popup_button: true,
        popup_width: "1700",
        popup_height: "800",
        support_host: "https://www.tradingview.com"
      });
      container.current.innerHTML = '';
      container.current.appendChild(script);
    },
    [symbol, watchlist, indicators]
  );

  return (
    <div className="tradingview-widget-container" ref={container} style={{ height: "600px" , width:"80%" }}>
      {/* Bu div'e height: "600px" gibi bir değer ekleyerek boyutu kontrol edebilirsiniz */}
      <div className="tradingview-widget-container__widget" style={{ height: "600px", width: "100%" }}></div>
      <div className="tradingview-widget-copyright">
        <a href="https://tr.tradingview.com/" rel="noopener nofollow" target="_blank">
          <span className="blue-text">Tüm piyasaları TradingView üzerinden takip edin</span>
        </a>
      </div>
    </div>
  );
}

export default memo(TradingViewWidget);
