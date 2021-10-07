import { http } from "../utils";

const API_URL = process.env.NEXT_PUBLIC_MOONSTREAM_API_URL;
const DB_URL = process.env.NEXT_PUBLIC_MOONSTREAM_DB_URL;
const ETHEREUM_CLUSTER_URL =
  process.env.NEXT_PUBLIC_MOONSTREAM_ETHEREUM_CLUSTER_URL;

export const apiServerStatus = () => {
  return http({
    method: "GET",
    url: `${API_URL}/ping`,
  });
};

export const ethereumClusterServerStatus = () => {
  return http({
    method: "GET",
    url: `${ETHEREUM_CLUSTER_URL}/ping`,
  });
};

export const gethStatus = () => {
  return http({
    method: "GET",
    url: `${ETHEREUM_CLUSTER_URL}/status`,
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
