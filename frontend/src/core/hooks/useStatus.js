import { useQuery } from "react-query";
import { queryCacheProps } from "./hookCommon";
import { StatusService } from "../../core/services";

const useStatus = () => {
  const getServerListStatus = async () => {
    const response = await StatusService.serverListStatus();
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

  return {
    serverListStatusCache,
  };
};

export default useStatus;
