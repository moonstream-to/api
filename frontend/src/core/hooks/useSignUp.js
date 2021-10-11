import { useContext } from "react";
import { useMutation } from "react-query";
import { AuthService } from "../services";
import { useUser, useToast, useInviteAccept, useRouter } from ".";
import UIContext from "../providers/UIProvider/context";
import mixpanel from "mixpanel-browser";
import { MIXPANEL_EVENTS } from "../providers/AnalyticsProvider/constants";

const useSignUp = (source) => {
  const ui = useContext(UIContext);

  const router = useRouter();
  const { getUser } = useUser();
  const toast = useToast();
  const { inviteAccept } = useInviteAccept();

  const {
    mutate: signUp,
    isLoading,
    error,
    data,
    isSuccess,
  } = useMutation(AuthService.register(), {
    onMutate: () => {
      ui.setLoggingIn(true);
    },
    onSuccess: (response) => {
      localStorage.setItem("MOONSTREAM_ACCESS_TOKEN", response.data.id);
      const invite_code = window.sessionStorage.getItem("invite_code");
      if (invite_code) {
        inviteAccept(invite_code);
      }

      if (mixpanel.get_distinct_id()) {
        mixpanel.track(`${MIXPANEL_EVENTS.CONVERT_TO_USER}`, {
          full_url: router.nextRouter.asPath,
          code: source,
        });
      }
      getUser();
      ui.setOnboardingComplete(false);
      router.push("/welcome", undefined, { shallow: false });
    },
    onError: (error) => {
      toast(error, "error");
    },
    onSettled: () => {
      ui.setLoggingIn(false);
    },
  });

  return {
    signUp,
    isLoading,
    data,
    error,
    isSuccess,
  };
};

export default useSignUp;
