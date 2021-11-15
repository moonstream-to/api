import React from "react";
import { ResponsiveLineCanvas } from "@nivo/line";

const Report = ({ data, metric }) => {
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

  console.log(`metric ${metric} \n xyCumulativeData: `, xyCumulativeData);

  const plotData = [{ id: "1", data: xyCumulativeData }];

  return (
    <ResponsiveLineCanvas
      {...commonProperties}
      data={plotData}
      margin={{ top: 50, right: 110, bottom: 70, left: 60 }}
      isInteractive={true}
      xScale={{
        type: "time",
        format: "%Y-%m-%d %H",
        useUTC: false,
        precision: "hour",
      }}
      xFormat="time:%Y-%m-%d %H"
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
        format: "%Y-%m-%d",
        tickValues: "every 1 day",
        legend: "time",
        tickRotation: 0,
        legendOffset: 35,
        legendPosition: "middle",
      }}
      curve={"basis"}
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

export default Report;
