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
  console.log("usePresignedURL:", url, id, isEnabled);
  const toast = useToast();

  const getFromPresignedURL = async () => {
    const response = await axios({
      url: url,
      // You can uncomment this to use mockupsLibrary in development
      // url: `https://example.com/s3`,
      method: "GET",
    });
    console.log("getFromPresignedURL", response);
    return response.data;
  };

  const { data, isLoading, error, refetch } = useQuery(
    ["presignedURL", cacheType, id],
    getFromPresignedURL,
    {
      ...queryCacheProps,
      enabled: isEnabled && url ? true : false,
      keepPreviousData: true,
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
      console.log("useeffect:", url, isEnabled);
      refetch();
    }
  }, [url, isEnabled, refetch]);

  return {
    data,
    isLoading,
    error,
  };
};

export default usePresignedURL;
