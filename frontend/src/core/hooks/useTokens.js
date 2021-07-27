import { useMutation } from "react-query";
import { AuthService } from "../services";

const useTokens = () => {
  const {
    mutate: list,
    isLoading,
    error,
    data,
  } = useMutation(AuthService.getTokenList);
  const { mutate: revoke } = useMutation(AuthService.revokeToken, {
    onSuccess: () => {
      list();
    },
  });

  const { mutate: update } = useMutation(AuthService.updateToken, {
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
