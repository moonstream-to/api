import React, { useState, useContext, useEffect } from "react";
import { useBreakpointValue } from "@chakra-ui/react";
import { useStorage, useQuery, useRouter } from "../../hooks";
import UIContext from "./context";
import UserContext from "../UserProvider/context";
import ModalContext from "../ModalProvider/context";
import { v4 as uuid4 } from "uuid";

const UIProvider = ({ children }) => {
  const router = useRouter();
  const { user, isInit } = useContext(UserContext);
  const isMobileView = useBreakpointValue({
    base: true,
    sm: true,
    md: false,
    lg: false,
    xl: false,
    "2xl": false,
  });
  // const isMobileView = true;

  const { modal, toggleModal } = useContext(ModalContext);
  const [searchTerm, setSearchTerm] = useQuery("q", "", true, false);

  const [searchBarActive, setSearchBarActive] = useState(false);

  // ****** Session state *****
  // Whether sidebar should be toggled in mobile view
  const [sessionId] = useStorage(window.sessionStorage, "sessionID", uuid4());

  // ******* APP state ********
  const [isLoggedIn, setLoggedIn] = useState(user && user.username);
  const [isLoggingOut, setLoggingOut] = useState(false);
  const [isAppReady, setAppReady] = useState(false);
  const [isAppView, setAppView] = useState(
    router.nextRouter.asPath.includes("/stream") ||
      router.nextRouter.asPath.includes("/account") ||
      router.nextRouter.asPath.includes("/subscriptions") ||
      router.nextRouter.asPath.includes("/analytics") ||
      router.nextRouter.asPath.includes("/welcome")
  );

  useEffect(() => {
    if (isAppView && isAppReady && !user?.username && !isLoggingOut) {
      // toggleModal("login");
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isAppView, isAppReady, user, isLoggingOut]);

  useEffect(() => {
    if (isLoggingOut && !isAppView && user) {
      setLoggingOut(false);
    }
  }, [isAppView, user, isLoggingOut]);

  useEffect(() => {
    if (isInit && router.nextRouter.isReady) {
      setAppReady(true);
    } else {
      setAppReady(false);
    }
  }, [isInit, router]);

  useEffect(() => {
    if (user && user.username) {
      setLoggedIn(true);
    } else {
      setLoggedIn(false);
    }
  }, [user]);

  useEffect(() => {
    setAppView(
      router.nextRouter.asPath.includes("/stream") ||
        router.nextRouter.asPath.includes("/account") ||
        router.nextRouter.asPath.includes("/subscriptions") ||
        router.nextRouter.asPath.includes("/analytics") ||
        router.nextRouter.asPath.includes("/welcome")
    );
  }, [router.nextRouter.asPath, user]);

  // *********** Sidebar states **********************

  // Whether sidebar should be visible at all or hidden
  const [sidebarVisible, setSidebarVisible] = useStorage(
    window.sessionStorage,
    "sidebarVisible",
    true
  );
  // Whether sidebar should be smaller state
  const [sidebarCollapsed, setSidebarCollapsed] = useStorage(
    window.sessionStorage,
    "sidebarCollapsed",
    false
  );

  // Whether sidebar should be toggled in mobile view
  const [sidebarToggled, setSidebarToggled] = useStorage(
    window.sessionStorage,
    "sidebarToggled",
    false
  );

  //Sidebar is visible at all times in mobile view
  useEffect(() => {
    if (isMobileView) {
      setSidebarVisible(true);
      setSidebarCollapsed(false);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isMobileView]);

  //Sidebar is visible at at breakpoint value less then 2
  //Sidebar is visible always in appView
  useEffect(() => {
    if (isMobileView) {
      setSidebarVisible(true);
      setSidebarCollapsed(false);
    } else {
      if (!isAppView) {
        setSidebarVisible(false);
      } else {
        setSidebarVisible(true);
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isMobileView, isAppView]);

  // *********** Entries layout states **********************

  //
  // const [entryId, setEntryId] = useState();
  // Current transaction to show in sideview
  const [currentTransaction, _setCurrentTransaction] = useState(undefined);
  const [isEntryDetailView, setEntryDetailView] = useState(false);

  const setCurrentTransaction = (tx) => {
    _setCurrentTransaction(tx);
    setEntryDetailView(!!tx);
  };

  /**
   * States that entries list box should be expanded
   * Default true in mobile mode and false in desktop mode
   */
  const [entriesViewMode, setEntriesViewMode] = useState(
    isMobileView ? "list" : "split"
  );

  useEffect(() => {
    setEntriesViewMode(
      isMobileView ? (isEntryDetailView ? "entry" : "list") : "split"
    );
  }, [isEntryDetailView, isMobileView]);

  // *********** Onboarding state **********************

  const onboardingSteps = [
    {
      step: "welcome",
      description: "Basics of how Moonstream works",
    },
    {
      step: "subscriptions",
      description: "Learn how to subscribe to blockchain events",
    },
    {
      step: "stream",
      description: "Learn how to use your Moonstream to analyze blah blah blah",
    },
  ];

  const [onboardingState, setOnboardingState] = useStorage(
    window.localStorage,
    "onboardingState",
    {
      welcome: 0,
      subscriptions: 0,
      stream: 0,
    }
  );

  const [onboardingStep, setOnboardingStep] = useState(() => {
    //First find onboarding step that was viewed once (resume where left)
    // If none - find step that was never viewed
    // if none - set onboarding to zero
    let step = onboardingSteps.findIndex(
      (event) => onboardingState[event.step] === 1
    );
    step =
      step === -1
        ? onboardingSteps.findIndex(
            (event) => onboardingState[event.step] === 0
          )
        : step;
    if (step === -1 && isOnboardingComplete) return 0;
    else if (step === -1 && !isOnboardingComplete) return 0;
    else return step;
  });

  const [isOnboardingComplete, setisOnboardingComplete] = useStorage(
    window.localStorage,
    "isOnboardingComplete",
    isLoggedIn ? true : false
  );

  useEffect(() => {
    if (isLoggedIn && !isOnboardingComplete) {
      router.replace("/welcome");
    }
    // eslint-disable-next-line
  }, [isLoggedIn, isOnboardingComplete]);

  useEffect(() => {
    if (
      onboardingSteps.findIndex(
        (event) => onboardingState[event.step] === 0
      ) === -1
    ) {
      setisOnboardingComplete(true);
    }
    //eslint-disable-next-line
  }, [onboardingState]);

  useEffect(() => {
    if (router.nextRouter.pathname === "/welcome") {
      const newOnboardingState = {
        ...onboardingState,
        [`${onboardingSteps[onboardingStep].step}`]:
          onboardingState[onboardingSteps[onboardingStep].step] + 1,
      };

      setOnboardingState(newOnboardingState);
    }
    // eslint-disable-next-line
  }, [onboardingStep, router.nextRouter.pathname]);

  // const ONBOARDING_STEP_NUM = steps.length;

  // ********************************************************

  return (
    <UIContext.Provider
      value={{
        sidebarVisible,
        setSidebarVisible,
        searchBarActive,
        setSearchBarActive,
        isMobileView,
        sidebarCollapsed,
        setSidebarCollapsed,
        sidebarToggled,
        setSidebarToggled,
        searchTerm,
        setSearchTerm,
        isAppView,
        setAppView,
        setLoggingOut,
        isLoggedIn,
        isAppReady,
        entriesViewMode,
        setEntryDetailView,
        modal,
        toggleModal,
        sessionId,
        currentTransaction,
        setCurrentTransaction,
        isEntryDetailView,
        onboardingStep,
        setOnboardingStep,
        isOnboardingComplete,
        setisOnboardingComplete,
        onboardingSteps,
        setOnboardingState,
      }}
    >
      {children}
    </UIContext.Provider>
  );
};

export default UIProvider;
