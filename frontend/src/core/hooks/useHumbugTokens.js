import { HumbugService } from "../services";
import { useToast } from ".";
import { useMutation, useQuery, useQueryCache } from "react-query";
import { queryCacheProps } from "./hookCommon";

const useHumbugTokens = (humbugId) => {
  const toast = useToast();
  const cache = useQueryCache();

  const getTokens = async (key, { humbugId }) => {
    var data;
    data = await HumbugService.getTokens(humbugId);
    const newHumbugTokens = data.data.tokens;
    return [...newHumbugTokens];
  };

  const humbugTokensCache = useQuery(
    [`Humbug-Tokens`, { humbugId }],
    getTokens,
    queryCacheProps
  );

  const [
    createRestrictedToken,
    {
      isLoading: isLoadingRestrictedToken,
      error: errorRestrictedToken,
      data: dataRestrictedToken,
    },
  ] = useMutation(HumbugService.createRestrictedToken(humbugId), {
    onMutate: () => {},
    onError: (error) => {
      toast(error, "error");
    },

    onSuccess: (response) => {
      const oldData = cache.getQueryData([`Humbug-Tokens`, { humbugId }]);
      const newData = [...oldData, ...response.data.tokens];
      cache.setQueryData([`Humbug-Tokens`, { humbugId }], newData);
    },
  });

  const createRestrictedTokenMutation = {
    createRestrictedToken,
    isLoading: isLoadingRestrictedToken,
    error: errorRestrictedToken,
    data: dataRestrictedToken,
  };

  const [
    deleteRestrictedToken,
    {
      isLoading: isLoadingDeleteRestrictedToken,
      error: errorDeleteRestrictedToken,
      data: dataDeleteRestrictedToken,
    },
  ] = useMutation(HumbugService.deleteRestrictedToken(humbugId), {
    onMutate: (tokenId) => {
      var newTokens = cache.getQueryData([`Humbug-Tokens`, { humbugId }]);
      const previousTokens = [...newTokens];

      newTokens = newTokens.filter(
        (token) => token.restricted_token_id !== tokenId
      );

      cache.setQueryData([`Humbug-Tokens`, { humbugId }], newTokens);

      return previousTokens;
    },
    onError: (error, variables, context) => {
      cache.setQueryData([`Humbug-Tokens`, { humbugId }], context);
      toast(error, "error");
    },
  });

  const deleteRestrictedTokenMutation = {
    deleteRestrictedToken,
    isLoading: isLoadingDeleteRestrictedToken,
    error: errorDeleteRestrictedToken,
    data: dataDeleteRestrictedToken,
  };

  return {
    humbugTokensCache,
    createRestrictedTokenMutation,
    deleteRestrictedTokenMutation,
  };
};

export default useHumbugTokens;
