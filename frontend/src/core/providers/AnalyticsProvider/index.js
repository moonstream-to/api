import React, { useContext, useEffect, useState } from "react";
import mixpanel from "mixpanel-browser";
import AnalyticsContext from "./context";
import { useClientID, useUser, useRouter } from "../../hooks";
import { MIXPANEL_EVENTS, MIXPANEL_PROPS } from "./constants";
import UIContext from "../UIProvider/context";

const TELEMETRY_SCHEMA_VERSION = 1.2;

const AnalyticsProvider = ({ children }) => {
  const clientID = useClientID();
  const analytics = process.env.NEXT_PUBLIC_MIXPANEL_TOKEN;
  const { user, isInit } = useUser();
  const [isMixpanelReady, setIsLoaded] = useState(false);
  const router = useRouter();
  const ui = useContext(UIContext);

  // ********** OBOARDING STATE **************
  useEffect(() => {
    if (ui.onboardingState && isMixpanelReady) {
      mixpanel.people.set(MIXPANEL_EVENTS.ONBOARDING_STATE, {
        state: { ...ui.onboardingState },
      });
    }
  }, [ui.onboardingState, isMixpanelReady]);

  useEffect(() => {
    if (ui.isOnboardingComplete && isMixpanelReady && user) {
      mixpanel.people.set(MIXPANEL_EVENTS.ONBOARDING_COMPLETED, true);
    }
  }, [ui.isOnboardingComplete, isMixpanelReady, user]);

  // ********** ONBOARDING STEP and TIMING **************
  const [previousOnboardingStep, setPreviousOnboardingStep] = useState(false);

  useEffect(() => {
    if (isMixpanelReady && router.nextRouter.pathname === "/welcome") {
      if (!previousOnboardingStep) {
        mixpanel.time_event(MIXPANEL_EVENTS.ONBOARDING_STEP);
        setPreviousOnboardingStep(ui.onboardingStep);
      }
      if (
        previousOnboardingStep &&
        previousOnboardingStep !== ui.onboardingStep
      ) {
        mixpanel.track(MIXPANEL_EVENTS.ONBOARDING_STEP, {
          step: previousOnboardingStep,
          isBeforeUnload: false,
        });
        setPreviousOnboardingStep(false);
      }
    } else if (previousOnboardingStep) {
      mixpanel.track(MIXPANEL_EVENTS.ONBOARDING_STEP, {
        step: previousOnboardingStep,
        isBeforeUnload: false,
      });
      setPreviousOnboardingStep(false);
    }
  }, [
    previousOnboardingStep,
    ui.onboardingStep,
    isMixpanelReady,
    router.nextRouter.pathname,
  ]);

  // ********** PING_PONG **************
  useEffect(() => {
    let durationSeconds = 0;

    const intervalId =
      isMixpanelReady &&
      setInterval(() => {
        durationSeconds = durationSeconds + 30;
        mixpanel.track(
          MIXPANEL_EVENTS.BEACON,
          {
            duration_seconds: durationSeconds,
            url: router.nextRouter.pathname,
          },
          { transport: "sendBeacon" }
        );
      }, 30000);

    return () => clearInterval(intervalId);
  }, [isMixpanelReady, router.nextRouter.pathname]);

  // ********** TIME SPENT ON PATH**************

  const [previousPathname, setPreviousPathname] = useState(false);

  useEffect(() => {
    if (isMixpanelReady) {
      if (!previousPathname) {
        mixpanel.time_event(MIXPANEL_EVENTS.PAGEVIEW_DURATION);
        setPreviousPathname(router.nextRouter.pathname);
      }
      if (previousPathname && previousPathname !== router.nextRouter.pathname) {
        mixpanel.track(MIXPANEL_EVENTS.PAGEVIEW_DURATION, {
          url: previousPathname,
          isBeforeUnload: false,
        });
        setPreviousPathname(false);
      }
    }
  }, [router.nextRouter.pathname, previousPathname, isMixpanelReady]);

  // ********** PAGES VIEW  **************
  useEffect(() => {
    if (isMixpanelReady && ui.sessionId && router.nextRouter.pathname) {
      mixpanel.track(MIXPANEL_EVENTS.PAGEVIEW, {
        url: router.nextRouter.pathname,
        sessionID: ui.sessionId,
      });

      mixpanel.people.increment([
        `${MIXPANEL_EVENTS.TIMES_VISITED} ${router.nextRouter.pathname}`,
      ]);
    }
    const urlForUnmount = router.nextRouter.pathname;
    const closeListener = () => {
      mixpanel.track(MIXPANEL_EVENTS.PAGEVIEW_DURATION, {
        url: urlForUnmount,
        isBeforeUnload: true,
      });
    };
    window.addEventListener("beforeunload", closeListener);
    //cleanup function fires on useEffect unmount
    //https://reactjs.org/docs/hooks-effect.html
    return () => {
      window.removeEventListener("beforeunload", closeListener);
    };
  }, [router.nextRouter.pathname, isMixpanelReady, ui.sessionId]);

  // ********** SESSION STATE **************
  useEffect(() => {
    if (clientID) {
      try {
        mixpanel.init(analytics, {
          api_host: "https://api.mixpanel.com",
          loaded: () => {
            setIsLoaded(true);
            mixpanel.identify(clientID);
            mixpanel.register({ schema_version: TELEMETRY_SCHEMA_VERSION });
          },
        });
      } catch (error) {
        console.warn("loading mixpanel failed:", error);
      }
    }
  }, [analytics, clientID]);

  useEffect(() => {
    isMixpanelReady && mixpanel.register("sessionId", ui.sessionId);
  }, [ui.sessionId, isMixpanelReady]);

  // ********** USER STATE **************

  useEffect(() => {
    if (user) {
      try {
        if (isMixpanelReady) {
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
  }, [user, isMixpanelReady, clientID]);

  useEffect(() => {
    if (isMixpanelReady && user) {
      mixpanel.people.set_once({
        [`${MIXPANEL_EVENTS.FIRST_LOGIN_DATE}`]: new Date().toISOString(),
      });
      mixpanel.people.set({
        [`${MIXPANEL_EVENTS.LAST_LOGIN_DATE}`]: new Date().toISOString(),
      });
      mixpanel.track(`${MIXPANEL_EVENTS.USER_LOGS_IN}`, {});
    }
  }, [user, isMixpanelReady]);

  useEffect(() => {
    if (isMixpanelReady && ui.isLoggingOut) {
      mixpanel.track(`${MIXPANEL_EVENTS.USER_LOGS_OUT}`, {});
    }
  }, [ui.isLoggingOut, isMixpanelReady]);

  // ********** USER BOUNCE TIME **************
  useEffect(() => {
    if (!user && isInit && isMixpanelReady) {
      mixpanel.time_event(MIXPANEL_EVENTS.CONVERT_TO_USER);
    }
  }, [user, isInit, isMixpanelReady]);

  const buttonReport = React.useCallback(
    (name, section, pageName) => {
      pageName = pageName || router.nextRouter.pathname.slice(1);
      console.log(`Reporting on name ${name} and section ${section}`);
      if (mixpanel?.get_distinct_id()) {
        mixpanel.track(`${MIXPANEL_EVENTS.BUTTON_CLICKED}`, {
          full_url: router.nextRouter.asPath,
          buttonName: name,
          page: pageName,
          section: section,
        });
      }
    },
    [router.nextRouter.asPath, router.nextRouter.pathname]
  );

  return (
    <AnalyticsContext.Provider
      value={{
        mixpanel,
        buttonReport,
        isMixpanelReady,
        MIXPANEL_EVENTS,
        MIXPANEL_PROPS,
      }}
    >
      {children}
    </AnalyticsContext.Provider>
  );
};

export default AnalyticsProvider;
