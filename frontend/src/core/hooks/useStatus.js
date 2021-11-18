import { useQuery } from "react-query";
import { queryCacheProps } from "./hookCommon";
import { StatusService } from "../../core/services";

const useStatus = () => {
  const getAPIServerStatus = async () => {
    const response = await StatusService.apiServerStatus();
    return response.data;
  };
  const getEthereumClusterServerStatus = async () => {
    const response = await StatusService.ethereumClusterServerStatus();
    return response.data;
  };
  const getGethStatus = async () => {
    const response = await StatusService.gethStatus();
    return response.data;
  };
  const getCrawlersStatus = async () => {
    const response = await StatusService.crawlersStatus();
    return response.data;
  };
  const getDBServerStatus = async () => {
    const response = await StatusService.dbServerStatus();
    return response.data;
  };
  const getLatestBlockDBStatus = async () => {
    const response = await StatusService.latestBlockDBStatus();
    return response.data;
  };

  const apiServerStatusCache = useQuery("apiServer", getAPIServerStatus, {
    ...queryCacheProps,
    retry: 0,
  });
  const ethereumClusterServerStatusCache = useQuery(
    "ethereumClusterServer",
    getEthereumClusterServerStatus,
    {
      ...queryCacheProps,
      retry: 0,
    }
  );
  const gethStatusCache = useQuery("geth", getGethStatus, {
    ...queryCacheProps,
    retry: 0,
  });
  const crawlersStatusCache = useQuery("crawlers", getCrawlersStatus, {
    ...queryCacheProps,
    retry: 0,
  });
  const dbServerStatusCache = useQuery("dbServer", getDBServerStatus, {
    ...queryCacheProps,
    retry: 0,
  });
  const latestBlockDBStatusCache = useQuery(
    "latestBlockDB",
    getLatestBlockDBStatus,
    {
      ...queryCacheProps,
      retry: 0,
    }
  );

  return {
    apiServerStatusCache,
    ethereumClusterServerStatusCache,
    gethStatusCache,
    crawlersStatusCache,
    dbServerStatusCache,
    latestBlockDBStatusCache,
  };
};

export default useStatus;
