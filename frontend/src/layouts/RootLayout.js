import { Flex } from "@chakra-ui/react";
import React, { Suspense } from "react";
const Sidebar = React.lazy(() => import("../components/Sidebar"));
const Navbar = React.lazy(() => import("../components/Navbar"));

const RootLayout = (props) => {
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
        {props.children}
      </Flex>
    </Flex>
  );
};

export const getLayout = (page) => <RootLayout>{page}</RootLayout>;

export default RootLayout;
