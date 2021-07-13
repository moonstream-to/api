import { HumbugService } from "../services";
import { useToast } from ".";
import { useQuery } from "react-query";
import { queryCacheProps } from "./hookCommon";

const useHumbug = (humbugId) => {
  const toast = useToast();

  const { data, isLoading, refetch } = useQuery(
    ["humbug", { humbugId }],
    HumbugService.getHumbug,
    {
      ...queryCacheProps,
      onError: (error) => {
        toast(error, "error");
      },
    }
  );

  return {
    data,
    isLoading,
    refetch,
  };
};
export default useHumbug;
