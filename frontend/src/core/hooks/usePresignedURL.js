import { useQuery, useQueryClient } from "react-query";
import { queryCacheProps } from "./hookCommon";
import { useToast } from ".";
import axios from "axios";

const usePresignedURL = ({
  presignedRequest,
  cacheType,
  id,
  requestNewURLCallback,
  isEnabled,
  hideToastOn404,
  refreshingStatus,
  setRefreshingStatus,
}) => {
  const toast = useToast();

  const getFromPresignedURL = async () => {
    let request_parameters = {
      url: presignedRequest.url,
      // You can uncomment this to use mockupsLibrary in development
      // url: `https://example.com/s3`,
      headers: {},
      method: "GET",
    };

    if ("headers" in presignedRequest) {
      Object.keys(presignedRequest.headers).map((key) => {
        request_parameters["headers"][key] = presignedRequest.headers[key];
      });
    }

    const response = await axios(request_parameters);
    return response.data;
  };

  const { data, isLoading, error, failureCount, refetch } = useQuery(
    ["presignedURL", cacheType, id, presignedRequest.url],
    getFromPresignedURL,
    {
      ...queryCacheProps,
      refetchOnMount: false,
      refetchOnWindowFocus: false,
      refetchOnReconnect: false,
      staleTime: Infinity,
      enabled: isEnabled && presignedRequest.url ? true : false,
      keepPreviousData: true,
      onSuccess: (e) => {
        setRefreshingStatus(false);
      },
      onError: (e) => {
        if (
          e?.response?.data?.includes("Request has expired") ||
          e?.response?.status === 403
        ) {
          requestNewURLCallback();
        } else if (e?.response?.status === 304) {
        } else {
          !hideToastOn404 && toast(error, "error");
        }
      },
    }
  );

  return {
    data,
    isLoading,
    error,
    failureCount,
    refetch,
  };
};

export default usePresignedURL;
