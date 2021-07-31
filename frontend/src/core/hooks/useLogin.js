import { useMutation } from "react-query";
import { useToast, useUser, useInviteAccept } from ".";
import { AuthService } from "../services";
import { useAnalytics } from ".";

const LOGIN_TYPES = {
  MANUAL: true,
  TOKEN: true,
};
const useLogin = (loginType) => {
  const { getUser } = useUser();
  const toast = useToast();
  const analytics = useAnalytics();
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
        localStorage.setItem("MOONSTREAM_ACCESS_TOKEN", data.data.access_token);
        const invite_code = window.sessionStorage.getItem("invite_code");
        if (invite_code) {
          inviteAccept(invite_code);
        }
        getUser();
        if (analytics.isLoaded) {
          analytics.mixpanel.people.set_once({
            [`${analytics.MIXPANEL_EVENTS.FIRST_LOGIN_DATE}`]: new Date().toISOString(),
          });
          analytics.mixpanel.people.set({
            [`${analytics.MIXPANEL_EVENTS.LAST_LOGIN_DATE}`]: new Date().toISOString(),
          });
          analytics.mixpanel.track(
            `${analytics.MIXPANEL_EVENTS.USER_LOGS_IN}`,
            {}
          );
        }
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
