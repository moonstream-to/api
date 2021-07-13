import { useMutation } from "react-query";
import { AuthService } from "../services";

const useTokens = () => {
  const [list, { isLoading, error, data }] = useMutation(
    AuthService.getTokenList
  );
  const [revoke] = useMutation(AuthService.revokeToken, {
    onSuccess: () => {
      list();
    },
  });

  const [update] = useMutation(AuthService.updateToken, {
    onSuccess: () => {
      list();
    },
  });

  return {
    list,
    update,
    revoke,
    isLoading,
    data,
    error,
  };
};

export default useTokens;
