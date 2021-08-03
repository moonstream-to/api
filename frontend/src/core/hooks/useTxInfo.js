import { useQuery } from "react-query";
import { TxInfoService } from "../services";
import { queryCacheProps } from "./hookCommon";
import { useToast } from ".";

const useTxInfo = (transaction) => {
    if (!transaction.tx) return {data: "undefined", isLoading: false, isFetchedAfterMount: true, refetch: false, isError: true, error: "undefined"}
    const toast = useToast();
    const getTxInfo = async () => {
        const response = await TxInfoService.getTxInfo(transaction);
        return response.data;
    }
    const { data, isLoading, isFetchedAfterMount, refetch, isError, error } =
    useQuery(["txinfo", transaction.tx.hash ], getTxInfo, {
      ...queryCacheProps,
      onError: (error) => toast(error, "error"),
    });

  return { data, isFetchedAfterMount, isLoading, refetch, isError, error };
};

export default useTxInfo;
