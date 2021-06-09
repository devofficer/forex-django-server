import loadable from "@loadable/component";
import pMinDelay from "p-min-delay";
import React, { useContext, useState, useEffect } from "react";
import { Dropdown, Nav, Tab } from "react-bootstrap";
import { Link } from "react-router-dom";
import { ThemeContext } from "../../../context/ThemeContext";
import QuickTransferSlider from "../kripton/Home/QuickTransferSlider";
import Widget1 from "../kripton/Home/WidgetChart1";
import Widget2 from "../kripton/Home/WidgetChart2";
import Widget3 from "../kripton/Home/WidgetChart3";
import Widget4 from "../kripton/Home/WidgetChart4";
import ReactApexChart from "react-apexcharts";
import axios from "axios";

const MarketOverview = loadable(() =>
  pMinDelay(import("../kripton/Home/MarketOverview"), 1000)
);
const MarketOverviewDark = loadable(() =>
  pMinDelay(import("../kripton/Home/MarketOverviewDark"), 1000)
);
const CryptoStatistics = loadable(() =>
  pMinDelay(import("../kripton/Home/CryptoStatistics"), 1000)
);
const CryptoStatisticsDark = loadable(() =>
  pMinDelay(import("../kripton/Home/CryptoStatisticsDark"), 1000)
);

const Home = () => {
  const { changeBackground, background } = useContext(ThemeContext);
  useEffect(() => {
    changeBackground({ value: "light", label: "Light" });
  }, []);
  // console.log(background.value === "dark");

  const [data, setData] = useState([]);

  axios
    .get("http://3.143.143.217:3306/api/predict", {
      // headers: {
      //   'Access-Control-Allow-Origin': '*'
      // }
    })
    .then(res => setData(res.data));

  console.log(data)

  const state = {
    series: [
      {
        name: "Estimation",
        data: [500, 230, 600, 360, 700, 890, 750, 420, 600, 300, 420, 220],
      },
      {
        name: "Real Currency",
        data: [250, 380, 200, 300, 200, 520, 380, 770, 250, 520, 300, 900],
      },
    ],
    options: {
      chart: {
        height: 600,
        type: "area",
        group: "social",
        toolbar: {
          show: false,
        },
        zoom: {
          enabled: false,
        },
      },
      dataLabels: {
        enabled: false,
      },
      stroke: {
        width: [2, 2],
        colors: ["#363062", "#2BC155"],
        curve: "straight",
      },
      legend: {
        tooltipHoverFormatter: function (val, opts) {
          return (
            val +
            " - " +
            opts.w.globals.series[opts.seriesIndex][opts.dataPointIndex] +
            ""
          );
        },
        markers: {
          fillColors: ["#363062", "#2BC155"],
          width: 19,
          height: 19,
          strokeWidth: 0,
          radius: 19,
        },
      },
      // markers: {
      //   size: 6,
      //   border: 0,
      //   colors: ["#363062", "#2BC155"],
      //   hover: {
      //     size: 6,
      //   },
      // },
      xaxis: {
        categories: [
          "January",
          "February",
          "March",
          "April",
          "May",
          "June",
          "July",
          "August",
          "September",
          "October",
          "November",
          "December",
          "10 Jan",
          "11 Jan",
          "12 Jan",
        ],
      },
      yaxis: {
        labels: {
          style: {
            colors: "#3e4954",
            fontSize: "14px",
            fontFamily: "Poppins",
            fontWeight: 100,
          },
        },
      },
      fill: {
        colors: ["#363062", "#2BC155"],
        type: "solid",
      },
      grid: {
        borderColor: "#f1f1f1",
      },
    },
  };

  return (
    <div id="chart" className="bar-chart">
      <ReactApexChart
        options={state.options}
        series={state.series}
        type="line"
        height={600}
      />
    </div>
  );
};

export default Home;
