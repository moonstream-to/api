import { HumbugService } from "../services";
import { useToast } from ".";
import { useMutation, useQuery, useQueryCache } from "react-query";
import { queryCacheProps } from "./hookCommon";

const useHumbugs = (query) => {
  const toast = useToast();
  const cache = useQueryCache();

  const getHumbugItegrations = async (key, { query }) => {
    var data;
    if (!query) {
      data = await HumbugService.getHumbugItegrations();
    } else {
      data = await HumbugService.getHumbugItegrations(query);
    }
    const newHumbugIntegrations = data.data.integrations;

    return [...newHumbugIntegrations];
  };

  const { data: humbugList } = useQuery(
    ["humbugs", { query }],
    getHumbugItegrations,
    queryCacheProps
  );

  const [
    createHumbug,
    {
      isLoading: isLoadingCreateHumbug,
      error: errorCreateHumbug,
      data: dataCreateHumbug,
    },
  ] = useMutation(HumbugService.createHumbug, {
    onSuccess: (response) => {
      var oldData = cache.getQueryData(["humbugs", { query }]);
      var newData = oldData ? [...oldData, response.data] : [response.data];
      cache.setQueryData(["humbugs", { query }], newData);
      cache.refetchQueries(["journals-list"]);

      cache.refetchQueries(["humbugs"], newData);
    },
    onError: (error) => {
      toast(error, "error");
    },
  });

  const [
    deleteHumbug,
    {
      isLoading: isLoadingDeleteHumbug,
      error: errorDeleteHumbug,
      data: dataDeleteHumbug,
    },
  ] = useMutation(HumbugService.deleteHumbug, {
    onMutate: (humbugId) => {
      var newHumbugs = cache.getQueryData(["humbugs", { query }]);
      const previousHumbugs = [...newHumbugs];
      newHumbugs = newHumbugs.filter((humbug) => humbug.id !== humbugId);

      cache.setQueryData(["humbugs", { query }], newHumbugs);

      var newHumbugsAll = cache.getQueryData(["humbugs", {}]);
      const prevHumbugsAll = [...newHumbugsAll];
      newHumbugsAll = newHumbugs.filter((humbug) => humbug.id !== humbugId);

      cache.setQueryData(["humbugs", {}], newHumbugsAll);

      return { previousHumbugs, prevHumbugsAll };
    },
    onError: (error, variables, context) => {
      cache.setQueryData(["humbugs", { query }], context.previousHumbugs);
      cache.setQueryData(["humbugs"], context.prevHumbugsAll);
      toast(error, "error");
    },
  });

  const createHumbugMutation = {
    createHumbug,
    isLoading: isLoadingCreateHumbug,
    errorCreateHumbug,
    dataCreateHumbug,
  };

  const deleteHumbugMutation = {
    deleteHumbug,
    isLoading: isLoadingDeleteHumbug,
    errorDeleteHumbug,
    dataDeleteHumbug,
  };

  return {
    humbugList,
    createHumbugMutation,
    deleteHumbugMutation,
  };
};
export default useHumbugs;
