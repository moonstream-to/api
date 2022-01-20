import React from "react";
import { ResponsiveLineCanvas } from "@nivo/line";

const Report = ({ data, timeRange }) => {
  if (!data) return "there is no data to show";
  const commonProperties = {
    animate: false,
    enableSlices: "x",
  };

  const xyData = data.map((item) => {
    return { x: item.date, y: item.count };
  });

  xyData.reverse();

  // Cumulative sum calculation inspired by: https://stackoverflow.com/a/55261098
  function generateCumulativeSum(sum) {
    function cumulativeSum(item) {
      sum += item.y;
      return { x: item.x, y: sum };
    }
    return cumulativeSum;
  }

  const xyCumulativeData = xyData.map(generateCumulativeSum(0));

  const timeformat_scale = {
    month: "%Y-%m-%d %H",
    week: "%Y-%m-%d %H",
    day: "%Y-%m-%d %H %M",
  };

  const timeformat_xformat = {
    month: "time:%Y-%m-%d %H",
    week: "time:%Y-%m-%d %H",
    day: "time:%Y-%m-%d %H %M",
  };

  const axis_format = {
    month: "%m-%d",
    week: "%d",
    day: "%H:%M",
  };

  const tickValues_format = {
    month: "every 1 days",
    week: "every 1 days",
    day: "every 1 hours",
  };

  const plotData = [{ id: "1", data: xyCumulativeData }];

  return (
    <ResponsiveLineCanvas
      {...commonProperties}
      data={plotData}
      margin={{ top: 50, right: 5, bottom: 70, left: 60 }}
      isInteractive={true}
      xScale={{
        type: "time",
        format: timeformat_scale[timeRange],
        useUTC: false,
        precision: "minute",
      }}
      xFormat={timeformat_xformat[timeRange]}
      yScale={{
        type: "linear",
        max: "auto",
        min: 0,
      }}
      axisLeft={{
        orient: "left",
        tickSize: 5,
        tickPadding: 5,
        tickRotation: 0,
        legendOffset: -45,
        legendPosition: "middle",
        legend: "count",
      }}
      axisBottom={{
        format: axis_format[timeRange],
        tickValues: tickValues_format[timeRange],
        legend: "time",
        tickRotation: 65,
        legendOffset: 45,
        legendPosition: "middle",
      }}
      curve={"monotoneY"}
      enableArea={true}
      enablePointLabel={false}
      pointSize={0}
      colors="#fd671b"
      pointBorderWidth={1}
      pointBorderColor={{
        from: "color",
        modifiers: [["darker", 0.3]],
      }}
      useMesh={true}
      enableSlices={false}
      enableGridX={true}
      enableGridY={true}
    />
  );
};

export default React.memo(Report);
