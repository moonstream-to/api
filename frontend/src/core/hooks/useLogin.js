import { useContext } from "react";
import { useMutation } from "react-query";
import { useToast, useUser, useInviteAccept } from ".";
import UIContext from "../providers/UIProvider/context";
import { AuthService } from "../services";

const LOGIN_TYPES = {
  MANUAL: true,
  TOKEN: true,
};
const useLogin = (loginType) => {
  const { setLoggingIn } = useContext(UIContext);
  const { getUser } = useUser();
  const toast = useToast();
  const { inviteAccept } = useInviteAccept();
  const {
    mutate: login,
    isLoading,
    error,
    data,
  } = useMutation(AuthService.login, {
    onMutate: () => {
      setLoggingIn(true);
    },
    onSuccess: (data) => {
      // Default value for loginType is LOGIN_TYPES.MANUAL
      if (!loginType) {
        loginType = LOGIN_TYPES.MANUAL;
      }

      if (loginType === LOGIN_TYPES.MANUAL) {
        if (!data) {
          return;
        }
        localStorage.setItem("MOONSTREAM_ACCESS_TOKEN", data.data.id);
        const invite_code = window.sessionStorage.getItem("invite_code");
        if (invite_code) {
          inviteAccept(invite_code);
        }
        getUser();
      }
    },
    onError: (error) => {
      toast(error, "error");
    },
    onSettled: () => {
      setLoggingIn(false);
    },
  });

  return {
    login,
    isLoading,
    data,
    error,
  };
};

export default useLogin;
