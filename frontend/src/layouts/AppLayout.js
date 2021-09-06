import { Flex } from "@chakra-ui/react";
import { getLayout as getSiteLayout } from "./RootLayout";
import React, { useContext, useLayoutEffect } from "react";
import UIContext from "../core/providers/UIProvider/context";

const AppLayout = ({ children }) => {
  const ui = useContext(UIContext);

  useLayoutEffect(() => {
    if (ui.isAppReady) {
      ui.setAppView(true);
      return () => {
        ui.setAppView(false);
      };
    }
    //eslint-disable-next-line
  }, [ui.isAppReady]);

  return (
    <Flex
      direction="row"
      id="JournalsWrapper"
      flexGrow={1}
      maxH="100%"
      w="100%"
      overflow="hidden"
    >
      {ui.isAppReady && ui.isLoggedIn && children}
    </Flex>
  );
};

export const getLayout = (page) => getSiteLayout(<AppLayout>{page}</AppLayout>);

export default AppLayout;
