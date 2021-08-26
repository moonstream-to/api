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
const HubspotForm = React.lazy(() => import("./HubspotForm"));

const Navbar = () => {
  const { modal, toggleModal, isAppView, isLoggedIn } = useContext(UIContext);

  return (
    <Flex
      boxShadow={["sm", "md"]}
      alignItems="center"
      id="Navbar"
      minH="3rem"
      maxH="3rem"
      bgColor="primary.1200"
      direction="row"
      w="100%"
      overflow="hidden"
    >
      <Suspense fallback={""}>
        {modal === "register" && <SignUp toggleModal={toggleModal} />}
        {modal === "login" && <SignIn toggleModal={toggleModal} />}
        {modal === "forgot" && <ForgotPassword toggleModal={toggleModal} />}
        {modal === "hubspot-trader" && (
          <HubspotForm
            toggleModal={toggleModal}
            title={"Join the waitlist"}
            formId={"29a17405-819b-405d-9563-f75bfb3774e0"}
          />
        )}
        {modal === "hubspot-fund" && (
          <HubspotForm
            toggleModal={toggleModal}
            title={"Join the waitlist"}
            formId={"04f0b8df-6b8f-4cd0-871f-4e872523b6f5"}
          />
        )}
        {modal === "hubspot-developer" && (
          <HubspotForm
            toggleModal={toggleModal}
            title={"Join the waitlist"}
            formId={"1897f4a1-3a00-475b-9bd5-5ca2725bd720"}
          />
        )}
        {(!isAppView || !isLoggedIn) && <LandingNavbar />}
        {isAppView && isLoggedIn && <AppNavbar />}
      </Suspense>
    </Flex>
  );
};

export default Navbar;
