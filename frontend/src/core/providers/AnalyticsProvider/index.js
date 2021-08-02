import React, { useEffect, useState } from "react";
import mixpanel from "mixpanel-browser";
import AnalyticsContext from "./context";
import { useClientID, useUser, useRouter } from "../../hooks";
import { MIXPANEL_EVENTS, MIXPANEL_PROPS } from "./constants";

const AnalyticsProvider = ({ children }) => {
  const clientID = useClientID();
  const analytics = process.env.NEXT_PUBLIC_MIXPANEL_TOKEN;
  const { user } = useUser();
  const [isLoaded, setIsLoaded] = useState(false);
  const router = useRouter();

  useEffect(() => {
    let durationSeconds = 0;

    const intervalId =
      isLoaded &&
      setInterval(() => {
        durationSeconds = durationSeconds + 1;
        mixpanel.track(
          MIXPANEL_EVENTS.LEFT_PAGE,
          {
            duration_seconds: durationSeconds,
            url: router.nextRouter.pathname,
            query: router.query,
            pathParams: router.params,
          },
          { transport: "sendBeacon" }
        );
      }, 1000);

    return () => clearInterval(intervalId);
    // eslint-disable-next-line
  }, [isLoaded]);

  useEffect(() => {
    if (isLoaded) {
      console.log(
        "track:",
        router.nextRouter.pathname,
        router.query,
        router.params
      );
    }
    isLoaded &&
      mixpanel.track(MIXPANEL_EVENTS.PAGEVIEW, {
        url: router.nextRouter.pathname,
        query: router.query,
        pathParams: router.params,
      });
  }, [router.nextRouter.pathname, router.query, router.params, isLoaded]);

  useEffect(() => {
    try {
      mixpanel.init(analytics, {
        api_host: "https://api.mixpanel.com",
        loaded: () => {
          setIsLoaded(true);
          mixpanel.identify(clientID);
        },
      });
    } catch (error) {
      console.warn("loading mixpanel failed:", error);
    }
  }, [analytics, clientID]);

  useEffect(() => {
    if (user) {
      try {
        if (isLoaded) {
          mixpanel.people.set({
            [`${MIXPANEL_EVENTS.LAST_VISITED}`]: new Date().toISOString(),
          });
          mixpanel.people.set({
            USER_ID: user.user_id,
            $name: user.username,
            $email: user.email,
          });
        }
      } catch (err) {
        console.error("could not set up people in mixpanel:", err);
      }
    }
  }, [user, isLoaded, clientID]);

  return (
    <AnalyticsContext.Provider
      value={{ mixpanel, isLoaded, MIXPANEL_EVENTS, MIXPANEL_PROPS }}
    >
      {children}
    </AnalyticsContext.Provider>
  );
};

export default AnalyticsProvider;
