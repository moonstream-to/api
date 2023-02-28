import React, { useContext } from "react";
import { Flex } from "@chakra-ui/react";
import UIContext from "../core/providers/UIProvider/context";
import { DEFAULT_METATAGS, BACKGROUND_COLOR } from "../core/constants";
import { getLayout as getSiteLayout } from "./index";

const InfoPageLayout = ({ children }) => {
  const ui = useContext(UIContext);

  return (
    <Flex
      bgPos="bottom"
      bgSize="cover"
      bgColor={BACKGROUND_COLOR}
      minH="100vh"
      direction="column"
      alignItems="center"
      w="100%"
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
