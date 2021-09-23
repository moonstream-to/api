import useToast from "./useToast";
import { useMutation } from "react-query";
import { AuthService } from "../services";

const useTokens = () => {
  const toast = useToast();
  const {
    mutate: list,
    isLoading,
    error,
    data,
  } = useMutation(AuthService.getTokenList);
  const { mutate: revoke } = useMutation(AuthService.revokeToken, {
    onSuccess: () => {
      toast("Token destroyed", "success");
      list();
    },
    onError: (error) => {
      toast(error, "error");
    },
  });

  const updateMutation = useMutation(AuthService.updateToken, {
    onSuccess: () => {
      list();
    },
    onError: (error) => {
      toast(error, "error");
    },
  });

  const createToken = useMutation(AuthService.login, {
    onSuccess: () => {
      list();
      toast("Created new token", "success");
    },
    onError: (error) => {
      toast(error, "error");
    },
  });

  return {
    createToken,
    list,
    updateMutation,
    revoke,
    isLoading,
    data,
    error,
  };
};

export default useTokens;
