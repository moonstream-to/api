import React, { Suspense, useContext } from "react";
import { Flex } from "@chakra-ui/react";
import UIContext from "../core/providers/UIProvider/context";
import { BACKGROUND_COLOR } from "../core/constants";

import LandingNavbar from "./LandingNavbar";
const AppNavbar = React.lazy(() => import("./AppNavbar"));

const Navbar = () => {
  const { isAppView, isLoggedIn, isMobileView } = useContext(UIContext);

  return (
    <Flex
      boxShadow={["sm", "md"]}
      zIndex={1}
      alignItems="center"
      id="Navbar"
      minH={isMobileView && !isAppView ? "89px" : "62px"}
      maxH={isMobileView && !isAppView ? "89px" : "62px"}
      bgColor={BACKGROUND_COLOR}
      borderBottom="1px solid white"
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
