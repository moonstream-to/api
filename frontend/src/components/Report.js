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
      }}
      axisLeft={{
        orient: "left",
        tickSize: 5,
        tickPadding: 5,
        tickRotation: 0,
        legendOffset: -40,
        legendPosition: "middle",
      }}
      axisBottom={{
        format: "%b %d",
        tickValues: "every 7 day",
        tickRotation: 90,
      }}
      curve="linear"
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
