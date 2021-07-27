/** @jsxRuntime classic */
/** @jsx jsx */
import { jsx } from "@emotion/react";
import React, { Suspense, useContext } from "react";
import { Flex } from "@chakra-ui/react";
import UIContext from "../core/providers/UIProvider/context";
const ForgotPassword = React.lazy(() => import("./ForgotPassword"));
const SignIn = React.lazy(() => import("./SignIn"));
const SignUp = React.lazy(() => import("./SignUp"));
const LandingNavbar = React.lazy(() => import("./LandingNavbar"));
const AppNavbar = React.lazy(() => import("./AppNavbar"));

const Navbar = () => {
  const { modal, toggleModal, isAppView, isLoggedIn } = useContext(UIContext);


  return (
    <Flex
      boxShadow={["sm", "md"]}
      alignItems="center"
      id="Navbar"
      minH={["3rem", "3rem", "3rem", "3rem", "3rem", "3rem"]}
      // overflow="initial"
      bgColor="primary.1200"
      // flexWrap="wrap"
      direction={["column", "row", "row", null, "row"]}
      // zIndex={100}
      w="100%"
      minW="100%"
      m={0}
      p={0}
      overflow="hidden"
    >
      <Suspense fallback={""}>
        {modal === "register" && <SignUp toggleModal={toggleModal} />}

        {modal === "login" && <SignIn toggleModal={toggleModal} />}

        {modal === "forgot" && <ForgotPassword toggleModal={toggleModal} />}

        {(!isAppView || !isLoggedIn) && <LandingNavbar />}
        {isAppView && isLoggedIn && <AppNavbar />}
      </Suspense>
    </Flex>
  );
};

export default Navbar;
