import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  ChartCanvas,
  Chart,
  series,
  axes,
  helper,
  scale,
} from "react-financial-charts";

const { CandlestickSeries } = series;
const { XAxis, YAxis } = axes;
const { discontinuousTimeScaleProvider } = scale;
const { fitWidth } = helper;

const CandlestickChart = (props) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchData = async () => {
    setLoading(true);
    setError("");
    try {
      const response = await axios.get(
        "http://127.0.0.1:8000/charts/table/Bitcoin/" // Replace with your endpoint
      );
      // Map the data to the format required for candlestick charts
      const chartData = response.data.map((item) => ({
        date: new Date(item.datetime),
        open: item.open,
        high: item.high,
        low: item.low,
        close: item.close,
        volume: item.volume,
      }));
      setData(chartData);
    } catch (err) {
      setError("Failed to load data.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;

  const xScaleProvider = discontinuousTimeScaleProvider.inputDateAccessor(
    (d) => d.date
  );
  const { data: chartData, xScale, xAccessor, displayXAccessor } =
    xScaleProvider(data);

  const xExtents = [
    xAccessor(chartData[0]),
    xAccessor(chartData[chartData.length - 1]),
  ];

  return (
    <div>
      <h1>Candlestick Chart</h1>
      {data.length > 0 && (
        <ChartCanvas
          height={400}
          width={props.width}
          ratio={3}
          margin={{ left: 50, right: 50, top: 10, bottom: 30 }}
          type={"svg"}
          seriesName="Candlestick"
          data={chartData}
          xScale={xScale}
          xAccessor={xAccessor}
          displayXAccessor={displayXAccessor}
          xExtents={xExtents}
        >
          <Chart id={1} yExtents={(d) => [d.high, d.low]}>
            <XAxis />
            <YAxis />
            <CandlestickSeries />
          </Chart>
        </ChartCanvas>
      )}
    </div>
  );
};

export default fitWidth(CandlestickChart);
