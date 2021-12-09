import { useQuery } from "react-query";
import { queryCacheProps } from "./hookCommon";
import { StatusService } from "../../core/services";

const useStatus = () => {
  const getServerListStatus = async () => {
    const response = await StatusService.serverListStatus();
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

  const serverListStatusCache = useQuery(
    "serverListStatus",
    getServerListStatus,
    {
      ...queryCacheProps,
      retry: 0,
    }
  );
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
    serverListStatusCache,
    crawlersStatusCache,
    dbServerStatusCache,
    latestBlockDBStatusCache,
  };
};

export default useStatus;
