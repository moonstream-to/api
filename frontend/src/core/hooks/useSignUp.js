import { useEffect } from "react";
import { useMutation } from "react-query";
import { AuthService } from "../services";
import { useUser, useToast, useInviteAccept, useRouter, useAnalytics } from ".";

const useSignUp = (source) => {
  const router = useRouter();
  const { getUser } = useUser();
  const toast = useToast();
  const { inviteAccept } = useInviteAccept();
  const analytics = useAnalytics();

  const [signUp, { isLoading, error, data }] = useMutation(
    AuthService.register(),
    {
      onSuccess: (response) => {
        localStorage.setItem("BUGOUT_ACCESS_TOKEN", response.data.access_token);
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
      },
      onError: (error) => {
        toast(error, "error");
      },
    }
  );

  useEffect(() => {
    if (!data) {
      return;
    }

    getUser();

    const requested_pricing = window.sessionStorage.getItem(
      "requested_pricing_plan"
    );
    const redirectURL = requested_pricing ? "/account/teams" : "/app";

    router.push(redirectURL);
    window.sessionStorage.clear("requested_pricing");
  }, [data, getUser, router]);

  return {
    signUp,
    isLoading,
    data,
    error,
  };
};

export default useSignUp;
