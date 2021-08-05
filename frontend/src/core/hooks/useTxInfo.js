import { useQuery } from "react-query";
import { TxInfoService } from "../services";
import { queryCacheProps } from "./hookCommon";
import { useToast } from ".";

const useTxInfo = (transaction) => {
  const toast = useToast();
  const getTxInfo = async () => {
    const response = await TxInfoService.getTxInfo(transaction);
    return response.data;
  };
  const { data, isLoading, isFetchedAfterMount, refetch, isError, error } =
    useQuery(["txinfo", transaction.tx.hash], getTxInfo, {
      ...queryCacheProps,
      enabled: !!transaction.tx,
      onError: (error) => toast(error, "error"),
    });

  return { data, isFetchedAfterMount, isLoading, refetch, isError, error };
};

export default useTxInfo;
