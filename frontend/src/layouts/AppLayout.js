import { Flex } from "@chakra-ui/react";
import { getLayout as getSiteLayout } from "./RootLayout";
import React, { useContext } from "react";
import UIContext from "../core/providers/UIProvider/context";

const AppLayout = ({ children }) => {
  const ui = useContext(UIContext);

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
