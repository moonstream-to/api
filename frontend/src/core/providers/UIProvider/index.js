import React, {
  useState,
  useContext,
  useEffect,
  useCallback,
  useLayoutEffect,
} from "react";
import { useBreakpointValue } from "@chakra-ui/react";
import { useStorage, useQuery, useRouter } from "../../hooks";
import UIContext from "./context";
import UserContext from "../UserProvider/context";
import ModalContext from "../ModalProvider/context";
import { v4 as uuid4 } from "uuid";
import { PreferencesService } from "../../services";

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
  const [isLoggingIn, setLoggingIn] = useState(false);
  const [isAppReady, setAppReady] = useState(false);
  const [isAppView, setAppView] = useState(false);

  useLayoutEffect(() => {
    if (
      isAppView &&
      isInit &&
      !user?.username &&
      !isLoggingOut &&
      !isLoggingIn &&
      !modal
    ) {
      toggleModal("login");
    } else if (user || isLoggingOut) {
      toggleModal(false);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isAppView, isAppReady, user, isLoggingOut, modal]);

  useEffect(() => {
    if (isLoggingOut && !isAppView && user) {
      setLoggingOut(false);
    }
  }, [isAppView, user, isLoggingOut]);

  useEffect(() => {
    if (user && user.username) {
      setLoggedIn(true);
    } else {
      setLoggedIn(false);
    }
  }, [user]);

  useLayoutEffect(() => {
    if (
      isLoggingOut &&
      router.nextRouter.pathname === "/" &&
      !user &&
      !localStorage.getItem("MOONSTREAM_ACCESS_TOKEN")
    ) {
      setLoggingOut(false);
    }
  }, [isLoggingOut, router.nextRouter.pathname, user]);

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

  const [onboardingState, setOnboardingState] = useState(false);
  const [onboardingStep, setOnboardingStep] = useState();
  const [onboardingStateInit, setOnboardingStateInit] = useState(false);
  const [onboardingRedirectCheckPassed, setOnboardingRedirectCheckPassed] =
    useState(false);

  const setOnboardingComplete = useCallback(
    (newState) => {
      setOnboardingState({ ...onboardingState, is_complete: newState });
    },
    [onboardingState]
  );

  useEffect(() => {
    //If onboarding state not exists - fetch it from backend
    //If it exists but init is not set - set init true
    //If it exists and is init -> post update to backend
    if (!onboardingState && user && !isLoggingOut) {
      const currentOnboardingState = async () =>
        PreferencesService.getOnboardingState().then((response) => {
          return response.data;
        });

      currentOnboardingState().then((response) => {
        setOnboardingState(response);
      });
    } else if (user && onboardingState && !onboardingStateInit) {
      setOnboardingStateInit(true);
    } else if (user && onboardingStateInit) {
      PreferencesService.setOnboardingState(onboardingState);
    }
    // eslint-disable-next-line
  }, [onboardingState, user]);

  useEffect(() => {
    //This will set step after state is fetched from backend
    if (!Number.isInteger(onboardingStep) && onboardingState) {
      const step = onboardingSteps.findIndex(
        (event) => onboardingState[event.step] === 0
      );
      if (step === -1 && onboardingState["is_complete"])
        setOnboardingStep(onboardingSteps.length - 1);
      else if (step === -1 && !onboardingState["is_complete"])
        return setOnboardingStep(0);
      else setOnboardingStep(step);
    }
  }, [onboardingState, onboardingStep]);

  useEffect(() => {
    //redirect to welcome page if yet not completed onboarding
    if (isLoggedIn && onboardingState && !onboardingState?.is_complete) {
      router.replace("/welcome", undefined, { shallow: true });
    }
    if (isLoggedIn) {
      setOnboardingRedirectCheckPassed(true);
    } else {
      setOnboardingRedirectCheckPassed(false);
    }
    // eslint-disable-next-line
  }, [isLoggedIn, onboardingState?.is_complete]);

  useEffect(() => {
    //This will set up onboarding complete once user finishes each view at least once
    if (onboardingState?.steps && user && isAppReady) {
      if (
        onboardingSteps.findIndex(
          (event) => onboardingState.steps[event.step] === 0
        ) === -1
      ) {
        !onboardingState.is_complete && setOnboardingComplete(true);
      }
    }
  }, [onboardingState, user, isAppReady, setOnboardingComplete]);

  useEffect(() => {
    //This will update onboardingState when step changes
    if (
      router.nextRouter.pathname === "/welcome" &&
      isAppReady &&
      user &&
      Number.isInteger(onboardingStep) &&
      onboardingState?.steps
    ) {
      setOnboardingState({
        ...onboardingState,
        steps: {
          ...onboardingState.steps,
          [`${onboardingSteps[onboardingStep].step}`]:
            onboardingState.steps[onboardingSteps[onboardingStep].step] + 1,
        },
      });
    }
    // eslint-disable-next-line
  }, [onboardingStep, router.nextRouter.pathname, user, isAppReady]);

  // ********************************************************

  useEffect(() => {
    if (
      isInit &&
      router.nextRouter.isReady &&
      onboardingState &&
      !isLoggingOut &&
      !isLoggingIn &&
      onboardingRedirectCheckPassed
    ) {
      setAppReady(true);
    } else {
      setAppReady(false);
    }
  }, [
    isInit,
    router,
    onboardingState,
    isLoggingOut,
    isLoggingIn,
    onboardingRedirectCheckPassed,
  ]);

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
        setOnboardingComplete,
        onboardingSteps,
        setOnboardingState,
        onboardingState,
        isLoggingOut,
        isLoggingIn,
        setLoggingIn,
      }}
    >
      {children}
    </UIContext.Provider>
  );
};

export default UIProvider;
