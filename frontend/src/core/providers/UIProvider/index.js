import React, {
  useState,
  useContext,
  useEffect,
  useCallback,
  useLayoutEffect,
  useReducer,
} from "react";
import { useBreakpointValue } from "@chakra-ui/react";
import { useStorage, useQuery, useRouter, useDashboard } from "../../hooks";
import UIContext from "./context";
import UserContext from "../UserProvider/context";
import { v4 as uuid4 } from "uuid";
import { PreferencesService } from "../../services";
import {
  DASHBOARD_CONFIGURE_SETTING_SCOPES,
  DASHBOARD_UPDATE_ACTIONS,
} from "../../constants";

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
  const { dashboardId } = router.params;
  const { dashboardCache } = useDashboard(dashboardId);
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

  useEffect(() => {
    if (isInit && router.nextRouter.isReady && !isLoggingOut && !isLoggingIn) {
      setAppReady(true);
    } else {
      setAppReady(false);
    }
  }, [isInit, router, isLoggingOut, isLoggingIn]);

  //***************New chart item 's state  ************************/
  const dashboardUpdateReducer = useCallback(
    (state, command) => {
      let newState = undefined;
      let index = -1;
      switch (command.type) {
        case DASHBOARD_UPDATE_ACTIONS.RESET_TO_DEFAULT:
          newState = { ...state };
          if (!dashboardCache.isLoading && dashboardCache.data?.resource_data) {
            newState = { ...dashboardCache.data.resource_data };
          }
          return newState;
        case DASHBOARD_UPDATE_ACTIONS.RENAME_DASHBOARD:
          return { ...state, name: command.payload };
        case DASHBOARD_UPDATE_ACTIONS.OVERRIDE_DASHBOARD:
          return { ...command.payload };
        case DASHBOARD_UPDATE_ACTIONS.APPEND_SUBSCRIPTION:
          newState = { ...state };

          if (
            state.subscription_settings.every(
              (subscriptionSetting) =>
                subscriptionSetting.subscription_id !==
                command.payload.subscriptionId
            )
          ) {
            newState.subscription_settings.push({
              subscription_id: command.payload.subscriptionId,
              all_methods: false,
              all_events: false,
              generic: [],
              methods: [],
              events: [],
            });
          }
          return newState;
        case DASHBOARD_UPDATE_ACTIONS.OVERRIDE_SUBSCRIPTION:
          newState = { ...state };
          index =
            dashboardCache.data?.resource_data?.subscription_settings?.findIndex(
              (subscriptionSetting) =>
                subscriptionSetting.subscription_id ===
                command.payload.subscriptionId
            );

          newState.subscription_settings[command.payload.index] =
            index !== -1
              ? JSON.parse(
                  JSON.stringify(
                    dashboardCache.data?.resource_data?.subscription_settings[
                      index
                    ]
                  )
                )
              : {
                  subscription_id: command.payload.subscriptionId,
                  all_methods: false,
                  all_events: false,
                  generic: [],
                  methods: [],
                  events: [],
                };
          return newState;
        case DASHBOARD_UPDATE_ACTIONS.DROP_SUBSCRIPTION:
          newState = { ...state };
          newState.subscription_settings =
            newState.subscription_settings.filter(
              (subscriptionSetting) =>
                subscriptionSetting.subscription_id !==
                command.payload.subscriptionId
            );
          return newState;
        case DASHBOARD_UPDATE_ACTIONS.APPEND_METRIC:
          switch (command.scope) {
            case DASHBOARD_CONFIGURE_SETTING_SCOPES.METRICS_ARRAY:
              newState = { ...state };
              index = state.subscription_settings.findIndex(
                (subscriptionSetting) =>
                  subscriptionSetting.subscription_id ===
                  command.payload.subscriptionId
              );
              if (index !== -1) {
                newState.subscription_settings[index][
                  command.payload.propertyName
                ] = [...command.payload.data];
              }
              return newState;

            case DASHBOARD_CONFIGURE_SETTING_SCOPES.METRIC_NAME:
              newState = { ...state };
              index = state.subscription_settings.findIndex(
                (subscriptionSetting) =>
                  subscriptionSetting.subscription_id ===
                  command.payload.subscriptionId
              );
              if (index !== -1) {
                if (
                  !newState.subscription_settings[index][
                    command.payload.propertyName
                  ].some((method) => method.name === command.payload.data.name)
                ) {
                  newState.subscription_settings[index][
                    command.payload.propertyName
                  ].push({
                    name: command.payload.data,
                  });
                }
              }
              return newState;

            default:
              throw new Error();
          }
        case DASHBOARD_UPDATE_ACTIONS.DROP_METRIC:
          switch (command.scope) {
            case DASHBOARD_CONFIGURE_SETTING_SCOPES.METRICS_ARRAY:
              newState = { ...state };
              index = state.subscription_settings.findIndex(
                (subscriptionSetting) =>
                  subscriptionSetting.subscription_id ===
                  command.payload.subscriptionId
              );
              newState.subscription_settings[index][
                command.payload.propertyName
              ] = [];
              return newState;

            case DASHBOARD_CONFIGURE_SETTING_SCOPES.METRIC_NAME:
              newState = { ...state };
              index = state.subscription_settings.findIndex(
                (subscriptionSetting) =>
                  subscriptionSetting.subscription_id ===
                  command.payload.subscriptionId
              );
              newState.subscription_settings[index][
                command.payload.propertyName
              ] = newState.subscription_settings[index][
                command.payload.propertyName
              ].filter((metric) => metric.name !== command.payload.data);
              return newState;

            default:
              throw new Error(`unhandled case command.scope: ${command.scope}`);
          }
        default:
          throw new Error(`unhandled case command.type: ${command.type}`);
      }
    },
    [dashboardCache.data, dashboardCache.isLoading]
  );
  const [dashboardUpdate, dispatchDashboardUpdate] = useReducer(
    dashboardUpdateReducer,
    {
      name: undefined,
      subscription_settings: [
        {
          subscription_id: undefined,
          all_methods: false,
          all_events: false,
          generic: [],
          methods: [],
          events: [],
        },
      ],
    }
  );

  useEffect(() => {
    if (!dashboardCache.isLoading && dashboardCache.data?.resource_data) {
      const dashboardCachedData = JSON.parse(
        JSON.stringify({ ...dashboardCache.data.resource_data })
      );
      dispatchDashboardUpdate({
        type: DASHBOARD_UPDATE_ACTIONS.OVERRIDE_DASHBOARD,
        payload: dashboardCachedData,
      });
    }
  }, [dashboardId, dashboardCache.isLoading, dashboardCache.data]);

  //***************New dashboard state  ************************/

  const [newDashboardForm, setNewDashboardForm] = useState();

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
        newDashboardForm,
        setNewDashboardForm,
        dashboardUpdate,
        dispatchDashboardUpdate,
      }}
    >
      {children}
    </UIContext.Provider>
  );
};

export default UIProvider;
