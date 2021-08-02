import { useEffect, useCallback, useContext } from "react";
import { useMutation, useQueryClient } from "react-query";
import { useUser, useRouter, useAnalytics } from ".";
import UIContext from "../providers/UIProvider/context";
import { AuthService } from "../services";

const useLogout = () => {
  const { setLoggingOut } = useContext(UIContext);
  const router = useRouter();
  const analytics = useAnalytics();
  const { mutate: revoke, data } = useMutation(AuthService.revoke, {
    onSuccess: () => {
      if (analytics.isLoaded) {
        analytics.mixpanel.track(
          `${analytics.MIXPANEL_EVENTS.USER_LOGS_OUT}`,
          {}
        );
      }
    },
  });
  const { setUser } = useUser();
  const cache = useQueryClient();

  const logout = useCallback(() => {
    setLoggingOut(true);
    router.replace("/");
    revoke();
    setUser(null);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [revoke, setUser, router]);

  useEffect(() => {
    if (!data) {
      return;
    }

    localStorage.removeItem("BUGOUT_ACCESS_TOKEN");
    cache.clear();
  }, [data, cache]);

  return {
    logout,
  };
};

export default useLogout;
