import { CloseIcon } from "@chakra-ui/icons";
import {
  Flex,
  Spinner,
  Center,
  Text,
  Link,
  IconButton,
} from "@chakra-ui/react";
import React, { Suspense, useContext, useState, useEffect } from "react";
const Sidebar = React.lazy(() => import("../components/Sidebar"));
const Navbar = React.lazy(() => import("../components/Navbar"));
import UIContext from "../core/providers/UIProvider/context";

const RootLayout = (props) => {
  const ui = useContext(UIContext);
  const [showSpinner, setSpinner] = useState(true);
  const [showBanner, setShowBanner] = useState(true);

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
        {!ui.isAppView && (
          <Flex
            w="100%"
            h={showBanner ? ["6.5rem", "4.5rem", "3rem", null] : "0"}
            minH={showBanner ? ["6.5rem", "4.5rem", "3rem", null] : "0"}
            animation="linear"
            transition="1s"
            overflow="hidden"
          >
            <Flex
              px="20px"
              w="100%"
              minH={["6.5rem", "4.5rem", "3rem", null]}
              h={["6.5rem", "4.5rem", "3rem", null]}
              placeContent="center"
              bgColor="suggested.900"
              boxShadow="md"
              position="relative"
              className="banner"
            >
              <Center w="calc(100% - 60px)">
                {" "}
                <Text
                  fontWeight="600"
                  textColor="primary.900"
                  fontSize={["sm", "sm", "md", null]}
                >
                  Join early. Our first 1000 users get free lifetime access to
                  blockchain analytics. Contact our team on{" "}
                  <Link
                    href={"https://discord.gg/V3tWaP36"}
                    color="secondary.900"
                  >
                    Discord
                  </Link>
                </Text>
              </Center>
              {/* <Spacer /> */}
              <IconButton
                position="absolute"
                top="0"
                right="0"
                icon={<CloseIcon />}
                colorScheme="primary"
                variant="ghost"
                onClick={() => setShowBanner(false)}
              />
            </Flex>
          </Flex>
        )}
        {!showSpinner && props.children}
        {showSpinner && <Spinner />}
      </Flex>
    </Flex>
  );
};

export const getLayout = (page) => <RootLayout>{page}</RootLayout>;

export default RootLayout;
