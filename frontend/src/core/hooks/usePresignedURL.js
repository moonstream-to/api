import { useQuery } from "react-query";
import { queryCacheProps } from "./hookCommon";
import { useToast } from ".";
import axios from "axios";
import { useEffect } from "react";

const usePresignedURL = ({
  url,
  cacheType,
  id,
  requestNewURLCallback,
  isEnabled,
}) => {
  const toast = useToast();

  const getFromPresignedURL = async () => {
    const queryState = queryClient.getQueryState([
      "presignedURL",
      cacheType,
      id,
      url,
    ]);

    const response = await axios({
      url: url,
      // You can uncomment this to use mockupsLibrary in development
      // url: `https://example.com/s3`,
      method: "GET",
      headers: {
        "If-Modified-Since": queryState?.dataUpdatedAt,
      },
    });
    return response.data;
  };

  const { data, isLoading, failureCount, refetch, dataUpdatedAt } = useQuery(
    [`${cacheType}`, id, url],
    getFromPresignedURL,
    {
      ...queryCacheProps,
      enabled: isEnabled && url ? true : false,
      onError: (e) => {
        if (
          e?.response?.data?.includes("Request has expired") ||
          e?.response?.status === 403
        ) {
          requestNewURLCallback();
        } else {
          toast(error, "error");
        }
      },
    }
  );

  useEffect(() => {
    if (url && isEnabled) {
      refetch();
    }
  }, [url, refetch, isEnabled]);

  return {
    data,
    isLoading,
    error,
    failureCount,
    dataUpdatedAt,
    refetch,
  };
};

export default usePresignedURL;
