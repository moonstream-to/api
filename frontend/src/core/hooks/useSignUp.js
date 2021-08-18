import { useContext } from "react";
import { useMutation } from "react-query";
import { AuthService } from "../services";
import { useUser, useToast, useInviteAccept, useRouter, useAnalytics } from ".";
import UIContext from "../providers/UIProvider/context";

const useSignUp = (source) => {
  const ui = useContext(UIContext);
  const router = useRouter();
  const { getUser } = useUser();
  const toast = useToast();
  const { inviteAccept } = useInviteAccept();
  const analytics = useAnalytics();

  const {
    mutate: signUp,
    isLoading,
    error,
    data,
    isSuccess,
  } = useMutation(AuthService.register(), {
    onSuccess: (response) => {
      localStorage.setItem("MOONSTREAM_ACCESS_TOKEN", response.data.id);
      const invite_code = window.sessionStorage.getItem("invite_code");
      if (invite_code) {
        inviteAccept(invite_code);
      }

      if (analytics.isLoaded) {
        analytics.mixpanel.track(
          `${analytics.MIXPANEL_EVENTS.CONVERT_TO_USER}`,
          { full_url: router.nextRouter.asPath, code: source }
        );
      }
      getUser();
      ui.setisOnboardingComplete(false);
      ui.setOnboardingState({ welcome: 0, subscriptions: 0, stream: 0 });
      router.push("/welcome", undefined, { shallow: false });
    },
    onError: (error) => {
      toast(error, "error");
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
