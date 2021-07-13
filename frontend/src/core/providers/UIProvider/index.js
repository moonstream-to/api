import React, { useState, useContext, useEffect } from "react";
import { useBreakpointValue } from "@chakra-ui/react";
import { useStorage, useQuery, useRouter } from "../../hooks";
import UIContext from "./context";
import UserContext from "../UserProvider/context";
import ModalContext from "../ModalProvider/context";

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

  const { modal, toggleModal } = useContext(ModalContext);
  const [searchTerm, setSearchTerm] = useQuery("q", " ", true, false);
  const [searchBarActive, setSearchBarActive] = useState(false);

  // ******* APP state ********
  const [isLoggedIn, setLoggedIn] = useState(user && user.username);
  const [isLoggingOut, setLoggingOut] = useState(false);
  const [isAppReady, setAppReady] = useState(false);
  const [isAppView, setAppView] = useState(
    router.nextRouter.asPath.includes("/app") ||
      router.nextRouter.asPath.includes("/account")
  );

  useEffect(() => {
    if (isAppView && isAppReady && !user?.username && !isLoggingOut) {
      toggleModal("login");
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isAppView, isAppReady, user, isLoggingOut]);

  useEffect(() => {
    if (isLoggingOut && !isAppView && !user) {
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
      router.nextRouter.asPath.includes("/app") ||
        router.nextRouter.asPath.includes("/account")
    );
  }, [router.nextRouter.asPath, user]);

  // *********** Sidebar states **********************

  // Whether sidebar should be visible at all or hidden
  const [sidebarVisible, setSidebarVisible] = useStorage(
    window.sessionStorage,
    "sidebarVisible",
    false
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
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isMobileView]);

  // //When entrering appView - start with showing sidebar at all times
  useEffect(() => {
    if (isAppView) {
      setSidebarVisible(true);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isAppView]);

  // *********** Entries layout states **********************

  /**
   * States that entries list box should be expanded
   * Default true in mobile mode and false in desktop mode
   */
  const [entriesViewMode, setEntriesViewMode] = useState(
    isMobileView ? (router.params?.entryId ? "entry" : "list") : "split"
  );

  useEffect(() => {
    setEntriesViewMode(
      isMobileView ? (router.params?.entryId ? "entry" : "list") : "split"
    );
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isMobileView]);

  useEffect(() => {
    setEntriesViewMode(isMobileView ? "list" : "split");
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [router.params?.id]);

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
        setEntriesViewMode,
        modal,
        toggleModal,
      }}
    >
      {children}
    </UIContext.Provider>
  );
};

export default UIProvider;
