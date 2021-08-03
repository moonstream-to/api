import { useQuery } from "react-query";
import { TxInfoService } from "../services";
import { queryCacheProps } from "./hookCommon";
import { useToast } from ".";

const useTxInfo = (transaction) => {
    if (!transaction.tx) return {data: "undefined", isLoading: false, isFetchedAfterMount: true, refetch: false, isError: true, error: "undefined"}
    const toast = useToast();
    const getTxInfo = async () => {
        const response = await TxInfoService.getTxInfo(transaction);
        // const responce_transaction = response.data;
        // console.log(responce_transaction)
        // responce_transaction.tags = [];
        // responce_transaction.tags.append("hello", "test")
        // if (responce_transaction.is_smart_contract_deployment) {
        //   responce_transaction.tags.append("smart contract deployment")
        // }
        // if (responce_transaction.is_smart_contract_call) {
        //   responce_transaction.tags.append("smart contract call")
        // }
        // if (responce_transaction.smart_contract_address) {
        //   responce_transaction.tx.smart_contract_address = responce_transaction.smart_contract_address
        // }
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
