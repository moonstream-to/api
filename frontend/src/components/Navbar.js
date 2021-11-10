import React, { Suspense, useContext } from "react";
import { Flex } from "@chakra-ui/react";
import UIContext from "../core/providers/UIProvider/context";

const LandingNavbar = React.lazy(() => import("./LandingNavbar"));
const AppNavbar = React.lazy(() => import("./AppNavbar"));

const Navbar = () => {
  const { isAppView, isLoggedIn } = useContext(UIContext);

  return (
    <Flex
      boxShadow={["sm", "md"]}
      alignItems="center"
      id="Navbar"
      minH="3rem"
      maxH="3rem"
      bgColor="blue.1200"
      direction="row"
      w="100%"
      overflow="hidden"
    >
      <Suspense fallback={""}>
        {(!isAppView || !isLoggedIn) && <LandingNavbar />}
        {isAppView && isLoggedIn && <AppNavbar />}
      </Suspense>
    </Flex>
  );
};

export default Navbar;
