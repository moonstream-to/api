import { useQuery } from "react-query";
import { TxInfoService } from "../services";
import { queryCacheProps } from "./hookCommon";
import { useToast } from ".";

const useTxInfo = (wrappedEvent) => {
  const toast = useToast();

  let event = {};
  if (wrappedEvent?.tx) {
    event = wrappedEvent.tx;
  }
  let transaction = null;
  if (event.event_type === "ethereum_blockchain") {
    transaction = event.event_data;
  } else if (event.event_type === "ethereum_txpool") {
    transaction = {
      from: event.event_data.from,
      nonce: event.event_data.nonce,
      ...event.event_data.transaction,
    };
  }

  const getTxInfo = async () => {
    const response = await TxInfoService.getTxInfo({ tx: { ...transaction } });
    return response.data;
  };
  const { data, isLoading, isFetchedAfterMount, refetch, isError, error } =
    useQuery(
      ["txinfo", transaction ? transaction.hash : "unknown"],
      getTxInfo,
      {
        ...queryCacheProps,
        enabled: !!transaction,
        onError: (error) => toast(error, "error"),
      }
    );
  const isFetching = !!transaction;
  return {
    data,
    isFetchedAfterMount,
    isLoading,
    refetch,
    isFetching,
    isError,
    error,
  };
};

export default useTxInfo;
