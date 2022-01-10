import { useQuery } from "react-query";
import { queryCacheProps } from "./hookCommon";
import { useToast } from ".";
import axios from "axios";

const usePresignedURL = ({
  url,
  headers,
  cacheType,
  id,
  requestNewURLCallback,
  isEnabled,
  hideToastOn404,
}) => {
  const toast = useToast();

  const getFromPresignedURL = async () => {
    let request_parameters = {
      url: url,
      // You can uncomment this to use mockupsLibrary in development
      // url: `https://example.com/s3`,
      headers: {},
      method: "GET",
    };

    if (headers != undefined) {
      Object.keys(headers).map((key) => {
        request_parameters["headers"][key] = headers[key];
      });
    }

    const response = await axios(request_parameters);
    return response.data;
  };

  const { data, isLoading, error, failureCount, isFetching } = useQuery(
    ["presignedURL", cacheType, id, url],
    getFromPresignedURL,
    {
      ...queryCacheProps,
      refetchOnMount: false,
      refetchOnWindowFocus: false,
      refetchOnReconnect: false,
      staleTime: Infinity,
      enabled: isEnabled && url ? true : false,
      keepPreviousData: true,
      onSuccess: () => {},
      onError: (e) => {
        if (
          e?.response?.data?.includes("Request has expired") ||
          e?.response?.status === 403
        ) {
          requestNewURLCallback();
        } else if (e?.response?.status === 304) {
          // If not modified.
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
    isFetching,
  };
};

export default usePresignedURL;
