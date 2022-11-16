import { Flex, Spinner, Box } from "@chakra-ui/react";
import { getLayout as getSiteLayout } from "./RootLayout";
import React, { Suspense, useContext, useEffect } from "react";
import UIContext from "../core/providers/UIProvider/context";
import AppNavbar from "../components/AppNavbar";
import { BACKGROUND_COLOR } from "../core/constants";
import Sidebar from "../components/Sidebar";

const AppLayout = ({ children }) => {
  const ui = useContext(UIContext);

  useEffect(() => {
    ui.setAppView(true);
    return () => {
      ui.setAppView(false);
    };
    // eslint-disable-next-line
  }, []);

  return (
    <Flex
      id="JournalsWrapper"
      bgColor={BACKGROUND_COLOR}
      flexGrow={1}
      maxH="100%"
      w="100%"
      overflow="hidden"
      direction="column"
      pb="85px"
    >
      {(!ui.isAppReady || !ui.isLoggedIn) && (
        <Spinner
          position="absolute"
          top="50%"
          left="50%"
          size="xl"
          speed="1s"
          zIndex={1011}
        />
      )}
      {(!ui.isAppReady || !ui.isLoggedIn) && (
        <Box
          position="absolute"
          top="0"
          bottom={0}
          left={0}
          right={0}
          bg="rgba(0,0,0,0.7)"
          zIndex={1010}
        />
      )}
      <Flex
        direction={"column"}
        bgColor={BACKGROUND_COLOR}
        borderBottom="1px solid white"
        id="Navbar"
      >
        <AppNavbar />
      </Flex>
      <Flex
        direction="row"
        // id="Bugout"
        className="Main"
        w="100%"
        h="100%"
        maxH="100%"
      >
        <Suspense fallback="">
          <Sidebar />
        </Suspense>
        {ui.isAppReady && ui.isLoggedIn && children}
      </Flex>
    </Flex>
  );
};

export const getLayout = (page) => getSiteLayout(<AppLayout>{page}</AppLayout>);

export default AppLayout;
