import React, { useCallback } from "react";
import { Spinner } from "@chakra-ui/react";
import useNFTs from "../core/hooks/useNFTs";
import { ResponsiveBarCanvas } from "@nivo/bar";
import moment from "moment";

const HOUR_KEY = "Hourly";
const DAY_KEY = "Daily";
const WEEK_KEY = "Weekly";
let timeMap = {};
timeMap[HOUR_KEY] = "hour";
timeMap[DAY_KEY] = "day";
timeMap[WEEK_KEY] = "week";

const NFTChart = ({ timeRange, keyPosition, keyTotal }) => {
  const { nftCache } = useNFTs();

  const getHourlyData = useCallback(
    (keyPosition, keyTotal) => {
      const retval = [];
      nftCache?.data?.forEach((block, idx) => {
        let diff =
          keyTotal && Number(block[keyTotal]) - Number(block[keyPosition]);

        let date = moment(block.crawled_at).format(`HH`);
        //group by days if not hour key
        if (idx < 23) {
          retval.push({
            date: date,
            NFTs: Number(block[keyPosition]),
            Other: keyTotal && diff,
          });
        }
      });

      return retval;
    },
    [nftCache.data]
  );

  const getDailyData = useCallback(
    (keyPosition, keyTotal) => {
      const retval = [];
      nftCache?.data?.forEach((block, idx) => {
        if (idx < 7 * 24) {
          let diff =
            keyTotal && Number(block[keyTotal]) - Number(block[keyPosition]);

          let date = moment(block.crawled_at).format(`l`);
          let existingIdx = retval.findIndex(
            (element) => element.date === date
          );
          if (existingIdx !== -1) {
            const prevValue = retval[existingIdx];
            const newValue = {
              date: prevValue.date,
              NFTs: prevValue.NFTs + Number(block[keyPosition]),
              Other: prevValue.Other + Number(block[keyPosition]),
            };
            retval[existingIdx] = { ...newValue };
          } else {
            retval.push({
              date: date,

              NFTs: Number(block[keyPosition]),
              Other: keyTotal && diff,
            });
          }
        }
      });

      return retval;
    },
    [nftCache.data]
  );

  const getWeeklyData = useCallback(
    (keyPosition, keyTotal) => {
      const retval = [];
      nftCache?.data?.forEach((block, idx) => {
        if (idx < 28 * 24) {
          let diff =
            keyTotal && Number(block[keyTotal]) - Number(block[keyPosition]);

          let date = moment(block.crawled_at).format(`l`);
          let existingIdx = retval.findIndex(
            (element) => element.date === date
          );
          if (existingIdx !== -1) {
            const prevValue = retval[existingIdx];
            const newValue = {
              date: prevValue.date,
              NFTs: prevValue.NFTs + Number(block[keyPosition]),
              Other: prevValue.Other + Number(block[keyPosition]),
            };
            retval[existingIdx] = { ...newValue };
          } else {
            retval.push({
              date: date,
              NFTs: Number(block[keyPosition]),
              Other: keyTotal && diff,
            });
          }
        }
      });

      return retval;
    },
    [nftCache.data]
  );

  const plotData =
    timeRange === HOUR_KEY
      ? getHourlyData(keyPosition, keyTotal)
      : timeRange === DAY_KEY
      ? getDailyData(keyPosition, keyTotal)
      : getWeeklyData(keyPosition, keyTotal);

  keyPosition === "nft_transfer_value" &&
    plotData.forEach((item, index) => {
      plotData[index].NFTs = plotData[index].NFTs / 1e18;
      plotData[index].Other = plotData[index].Other / 1e18;
    });
  if (nftCache.isLoading) return <Spinner />;
  console.log("plotData is", plotData);
  return (
    <ResponsiveBarCanvas
      colors={["#fe9a67", "#7a7fbc"]}
      animate={true}
      data={plotData}
      valueScale={{
        type: "linear",
      }}
      enableLabel={false}
      keys={keyTotal ? ["NFTs", "Other"] : ["NFTs"]}
      padding={0}
      axisBottom={
        timeRange === WEEK_KEY
          ? null
          : {
              tickSize: 5,
              tickPadding: 5,
              tickRotation: 45,
              // legend: "Time",
              legendPosition: "middle",
              legendOffset: 62,
            }
      }
      indexBy="date"
      offsetType="expand"
      margin={{ top: 50, right: 110, bottom: 50, left: 60 }}
      // legendLabel={(d) => labelLookup[d.id]}
      // tooltipLabel={(d) => labelLookup[d.id]}
      legends={[
        {
          anchor: "bottom-right",
          direction: "column",
          translateX: 100,
          itemWidth: 80,
          itemHeight: 20,
          itemTextColor: "#999999",
          symbolSize: 12,
          symbolShape: "circle",
          effects: [
            {
              on: "hover",
              style: {
                itemTextColor: "#000000",
              },
            },
          ],
        },
      ]}
    />
  );
};

export default NFTChart;
