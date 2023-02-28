import React from "react";
import { Flex } from "@chakra-ui/react";
import { DEFAULT_METATAGS, BACKGROUND_COLOR } from "../core/constants";
import { getLayout as getSiteLayout } from "./index";

const InfoPageLayout = ({ children }) => {
  const margin = 0;
  return (
    <Flex
      bgPos="bottom"
      bgColor={BACKGROUND_COLOR}
      bgSize="cover"
      minH="100vh"
      direction="column"
      alignItems="center"
      w="100%"
      px="7%"
    >
      {children}
    </Flex>
  );
};

export const getLayout = (page) =>
  getSiteLayout(<InfoPageLayout>{page}</InfoPageLayout>);

export const getLayoutProps = () => {
  const preconnects = [{ rel: "preconnect", href: "https://s3.amazonaws.com" }];

  return {
    props: { metaTags: { ...DEFAULT_METATAGS }, preconnects },
  };
};
export default InfoPageLayout;
