import { useQuery } from "react-query";
import { JournalService } from "../services";
import { queryCacheProps } from "./hookCommon";

const useJournals = () => {
  const getJournalsScopes = async () => {
    var data;

    data = await JournalService.getJournalsScopes();
    const scopes = data.data.scopes;

    return [...scopes];
  };

  const scopesCache = useQuery("journals-scopes", getJournalsScopes, {
    ...queryCacheProps,
    enabled: true,
  });

  return {
    scopesCache,
  };
};

export default useJournals;
