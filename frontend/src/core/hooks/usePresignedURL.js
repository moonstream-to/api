import { useQuery } from "react-query";
import { queryCacheProps } from "./hookCommon";
import { useToast } from ".";
import axios from "axios";

const usePresignedURL = ({
  url,
  cacheType,
  id,
  requestNewURLCallback,
  isEnabled,
  hideToastOn404,
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

<<<<<<< HEAD
  const { data, isLoading, failureCount, refetch, dataUpdatedAt } = useQuery(
    [`${cacheType}`, id, url],
=======
  const { data, isLoading, error, failureCount } = useQuery(
    ["presignedURL", cacheType, id, url],
>>>>>>> main
    getFromPresignedURL,
    {
      ...queryCacheProps,
      refetchOnMount: false,
      refetchOnWindowFocus: false,
      refetchOnReconnect: false,
      staleTime: Infinity,
      enabled: isEnabled && url ? true : false,
      keepPreviousData: true,
      onError: (e) => {
        if (
          e?.response?.data?.includes("Request has expired") ||
          e?.response?.status === 403
        ) {
          requestNewURLCallback();
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
<<<<<<< HEAD
    dataUpdatedAt,
    refetch,
=======
>>>>>>> main
  };
};

export default usePresignedURL;
