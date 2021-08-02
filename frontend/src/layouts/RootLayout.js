import { Flex, Spinner } from "@chakra-ui/react";
import React, { Suspense, useContext, useState, useEffect } from "react";
const Sidebar = React.lazy(() => import("../components/Sidebar"));
const Navbar = React.lazy(() => import("../components/Navbar"));
import UIContext from "../core/providers/UIProvider/context";

const RootLayout = (props) => {
  const ui = useContext(UIContext);
  const [showSpinner, setSpinner] = useState(true);

  useEffect(() => {
    if (ui.isAppView && ui.isAppReady) {
      setSpinner(false);
    } else if (!ui.isAppView) {
      setSpinner(false);
    } else {
      setSpinner(true);
    }
  }, [ui, setSpinner]);

  return (
    <Flex
      direction="row"
      id="Bugout"
      className="Main"
      w="100%"
      h="100%"
      maxH="100%"
    >
      <Suspense fallback="">
        <Sidebar />
      </Suspense>
      <Flex
        direction="column"
        flexGrow={1}
        flexBasis="100px"
        overflowX="hidden"
      >
        <Suspense fallback="">
          <Navbar />
        </Suspense>
        {!showSpinner && props.children}
        {showSpinner && <Spinner />}
      </Flex>
    </Flex>
  );
};

export const getLayout = (page) => <RootLayout>{page}</RootLayout>;

export default RootLayout;
