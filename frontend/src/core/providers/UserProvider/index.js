import React, { useState, useEffect, useCallback } from "react";
import http from "axios";
import { AUTH_URL } from "./constants";
import UserContext from "./context";

const UserProvider = ({ children }) => {
  const [user, setUser] = useState();
  const [isInit, setInit] = useState(false);

  const getUser = useCallback(() => {
    const token = localStorage.getItem("MOONSTREAM_ACCESS_TOKEN");
    if (!token) {
      setInit(true);
      return setUser(null);
    }

    const headers = { Authorization: `Bearer ${token}` };
    http
      .get(`${AUTH_URL}/user`, { headers })
      .then((response) => {
        setUser(response.data);
      })
      .catch(() => setUser(null))
      .finally(() => setInit(true));
  }, []);

  useEffect(() => {
    let isMounted = true;
    if (isMounted) {
      getUser();
    }
    return () => {
      isMounted = false;
    };
  }, [getUser]);

  return (
    <UserContext.Provider value={{ isInit, user, setUser, getUser }}>
      {children}
    </UserContext.Provider>
  );
};

export default UserProvider;
