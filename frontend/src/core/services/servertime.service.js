import { http } from "../utils";

import { MOONSTREAM_API_URL } from "../constants";

export const serverTimeNow = async () => {
  const response = await http({
    method: "GET",
    url: `${MOONSTREAM_API_URL}/now`,
  });

  const timestamp = response.data.epoch_time;
  // Javascript Date objects are loaded from Unix timestamps at the level of precision of milliseconds
  // since epoch start. The server returns microseconds since epoch, but the integer part of the response
  // time is at second-level precision.
  const jsTimestamp = Math.floor(timestamp * 1000);
  const jsDate = new Date(jsTimestamp);
  return jsDate;
};

// Returns the milliseconds of difference between the clocks of the client and the Moonstream API
// server. Since this involves a request to the server, it also includes the latency of making an HTTP
// request to the server's /now endpoint and getting a response.
export const clientServerOffsetMillis = async () => {
  // TODO(zomglings): Time the request and use a simple estimate for the latency based on:
  // 1. Size of request
  // 2. Size of resposne
  // 3. Profiling the body of the `/now` handler on the server.
  // At least a naive estimate would be something like:
  // const currentServerTime = serverTime + (responseAt - requestAt)*3/4
  //
  // This assumes that 3/4 of the latency was involved in sending the response back to the client.
  //
  // Unfortunately, it also assumes that the client clock and server clock are moving at the same
  // speed. Of course, we could check the speeds against each other by repeated calls to this method,
  // but I think we don't need that level of synchronizating yet.
  const serverTime = await serverTimeNow();
  const clientTime = new Date();
  return clientTime - serverTime;
};

// Returns a stream boundary representing the past 5 minutes.
export const defaultStreamBoundary = async () => {
  const endTime = await serverTimeNow();
  const startTimeMillis = endTime - 5 * 60 * 1000;
  const streamBoundary = {
    start_time: Math.floor(startTimeMillis / 1000),
    end_time: Math.floor(endTime / 1000),
    include_start: true,
    include_end: true,
  };
  return streamBoundary;
};
