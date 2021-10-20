import { CloseIcon } from "@chakra-ui/icons";
import { Flex, Center, Text, Link, IconButton } from "@chakra-ui/react";
import React, { Suspense, useContext, useState } from "react";
import UIContext from "../core/providers/UIProvider/context";
const Sidebar = React.lazy(() => import("../components/Sidebar"));
const Navbar = React.lazy(() => import("../components/Navbar"));

const RootLayout = (props) => {
  const ui = useContext(UIContext);
  const [showBanner, setShowBanner] = useState(false);

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
              bgColor="green.900"
              boxShadow="md"
              position="relative"
              className="banner"
            >
              <Center w="calc(100% - 60px)">
                {" "}
                <Text
                  fontWeight="600"
                  textColor="blue.900"
                  fontSize={["sm", "sm", "md", null]}
                >
                  Join early. Our first 1000 users get free lifetime access to
                  blockchain analytics. Contact our team on{" "}
                  <Link
                    isExternal
                    href={"https://discord.gg/K56VNUQGvA"}
                    color="orange.900"
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
                colorScheme="blue"
                variant="ghost"
                onClick={() => setShowBanner(false)}
              />
            </Flex>
          </Flex>
        )}
        {props.children}
      </Flex>
    </Flex>
  );
};

export const getLayout = (page) => <RootLayout>{page}</RootLayout>;

export default RootLayout;
