import React, { Suspense, useContext } from "react";
import { Flex } from "@chakra-ui/react";
import UIContext from "../core/providers/UIProvider/context";

import LandingNavbar from "./LandingNavbar";
const AppNavbar = React.lazy(() => import("./AppNavbar"));

const Navbar = () => {
  const { isAppView, isLoggedIn } = useContext(UIContext);

  return (
    <Flex
      boxShadow={["sm", "md"]}
      zIndex={1}
      alignItems="center"
      id="Navbar"
      minH="3rem"
      maxH="3rem"
      bgColor="blue.1200"
      direction="row"
      w="100%"
      overflow="hidden"
      position={"fixed"}
      transition={"0.3s"}
      top={"0"}
    >
      {(!isAppView || !isLoggedIn) && <LandingNavbar />}
      <Suspense fallback={""}>
        {isAppView && isLoggedIn && <AppNavbar />}
      </Suspense>
    </Flex>
  );
};

export default Navbar;
