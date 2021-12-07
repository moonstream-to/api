import { http } from "../utils";

const BUGOUT_STATUS_URL = process.env.NEXT_PUBLIC_BUGOUT_STATUS_URL;
const API_URL = process.env.NEXT_PUBLIC_MOONSTREAM_API_URL;
const DB_URL = process.env.NEXT_PUBLIC_MOONSTREAM_DB_URL;

export const serverListStatus = () => {
  return http({
    method: "GET",
    url: `${BUGOUT_STATUS_URL}`,
  });
};

export const crawlersStatus = () => {
  return http({
    method: "GET",
    url: `${API_URL}/status`,
  });
};

export const dbServerStatus = () => {
  return http({
    method: "GET",
    url: `${DB_URL}/ping`,
  });
};

export const latestBlockDBStatus = () => {
  return http({
    method: "GET",
    url: `${DB_URL}/block/latest`,
  });
};
