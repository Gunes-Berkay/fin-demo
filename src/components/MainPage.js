import React from 'react'
import AdvancedChart from './Charts/AdvancedChart'
import EconomicCalendar from './Charts/EconomicCalendar'
const MainPage = () => {
  const symbol = 'BTCUSDT'
  const watchlist = ['BINANCE:SOLUSDT' , 'BINANCE:INJUSDT', 'BINANCE:ETHUSDT']
  const indicators = ["STD;CCI", "STD;RSI"]

  return (
    <div style={{ width: '100%', height: '600px' }}>
      <AdvancedChart symbol={symbol} watchlist={watchlist} indicators={indicators}></AdvancedChart>
      <EconomicCalendar></EconomicCalendar>
    </div>
  )
}

export default MainPage