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
  });
  const ethereumClusterServerStatusCache = useQuery(
    "ethereumClusterServer",
    getEthereumClusterServerStatus,
    {
      ...queryCacheProps,
    }
  );
  const gethStatusCache = useQuery("geth", getGethStatus, {
    ...queryCacheProps,
  });
  const crawlersStatusCache = useQuery("crawlers", getCrawlersStatus, {
    ...queryCacheProps,
  });
  const dbServerStatusCache = useQuery("dbServer", getDBServerStatus, {
    ...queryCacheProps,
  });
  const latestBlockDBStatusCache = useQuery(
    "latestBlockDB",
    getLatestBlockDBStatus,
    {
      ...queryCacheProps,
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
