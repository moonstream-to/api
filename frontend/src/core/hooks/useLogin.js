import { useMutation } from "react-query";
import { useToast, useUser, useInviteAccept } from ".";
import { AuthService } from "../services";

const LOGIN_TYPES = {
  MANUAL: true,
  TOKEN: true,
};
const useLogin = (loginType) => {
  const { getUser } = useUser();
  const toast = useToast();
  const { inviteAccept } = useInviteAccept();
  const {
    mutate: login,
    isLoading,
    error,
    data,
  } = useMutation(AuthService.login, {
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
  });

  return {
    login,
    isLoading,
    data,
    error,
  };
};

export default useLogin;
