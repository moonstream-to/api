import React, { useContext, useState, useEffect, useLayoutEffect } from "react";
import { Flex, useMediaQuery, Stack } from "@chakra-ui/react";
import UIContext from "../core/providers/UIProvider/context";
import { DEFAULT_METATAGS, AWS_ASSETS_PATH } from "../core/constants";
import { getLayout as getSiteLayout } from "./index";

const assets = {
  background720: `${AWS_ASSETS_PATH}/blog-background-720x405.png`,
  background1920: `${AWS_ASSETS_PATH}/blog-background-720x405.png`,
  background2880: `${AWS_ASSETS_PATH}/blog-background-720x405.png`,
  background3840: `${AWS_ASSETS_PATH}/blog-background-720x405.png`,
};

const InfoPageLayout = ({ children }) => {
  const ui = useContext(UIContext);
  const [background, setBackground] = useState("background720");
  const [backgroundLoaded720, setBackgroundLoaded720] = useState(false);
  const [backgroundLoaded1920, setBackgroundLoaded1920] = useState(false);
  const [backgroundLoaded2880, setBackgroundLoaded2880] = useState(false);
  const [backgroundLoaded3840, setBackgroundLoaded3840] = useState(false);

  const [
    isLargerThan720px,
    isLargerThan1920px,
    isLargerThan2880px,
    isLargerThan3840px,
  ] = useMediaQuery([
    "(min-width: 720px)",
    "(min-width: 1920px)",
    "(min-width: 2880px)",
    "(min-width: 3840px)",
  ]);

  useEffect(() => {
    assets["background720"] = `${AWS_ASSETS_PATH}/blog-background-720x405.png`;
    assets[
      "background1920"
    ] = `${AWS_ASSETS_PATH}/blog-background-1920x1080.png`;
    assets[
      "background2880"
    ] = `${AWS_ASSETS_PATH}/blog-background-2880x1620.png`;
    assets[
      "background3840"
    ] = `${AWS_ASSETS_PATH}/blog-background-3840x2160.png`;
  }, []);

  useLayoutEffect(() => {
    if (backgroundLoaded3840) {
      setBackground("background3840");
    } else if (backgroundLoaded2880) {
      setBackground("background2880");
    } else if (backgroundLoaded1920) {
      setBackground("background1920");
    } else {
      setBackground("background720");
    }
  }, [
    isLargerThan720px,
    isLargerThan1920px,
    isLargerThan2880px,
    isLargerThan3840px,
    backgroundLoaded720,
    backgroundLoaded1920,
    backgroundLoaded2880,
    backgroundLoaded3840,
  ]);

  useLayoutEffect(() => {
    const imageLoader720 = new Image();
    imageLoader720.src = `${AWS_ASSETS_PATH}/blog-background-720x405.png`;
    imageLoader720.onload = () => {
      setBackgroundLoaded720(true);
    };
  }, []);

  useLayoutEffect(() => {
    const imageLoader1920 = new Image();
    imageLoader1920.src = `${AWS_ASSETS_PATH}/blog-background-1920x1080.png`;
    imageLoader1920.onload = () => {
      setBackgroundLoaded1920(true);
    };
  }, []);

  useLayoutEffect(() => {
    const imageLoader2880 = new Image();
    imageLoader2880.src = `${AWS_ASSETS_PATH}/blog-background-2880x1620.png`;
    imageLoader2880.onload = () => {
      setBackgroundLoaded2880(true);
    };
  }, []);

  useLayoutEffect(() => {
    const imageLoader3840 = new Image();
    imageLoader3840.src = `${AWS_ASSETS_PATH}/blog-background-3840x2160.png`;
    imageLoader3840.onload = () => {
      setBackgroundLoaded3840(true);
    };
  }, []);
  const margin = ui.isMobileView ? "6%" : "22%";
  return (
    <Flex
      bgPos="bottom"
      bgColor="transparent"
      bgSize="cover"
      backgroundImage={`url(${assets[`${background}`]})`}
      minH="100vh"
      direction="column"
      alignItems="center"
      w="100%"
    >
      <Stack mx={margin} my={[4, 6, 12]} maxW="1700px" textAlign="justify">
        {children}
      </Stack>
    </Flex>
  );
};

export const getLayout = (page) =>
  getSiteLayout(<InfoPageLayout>{page}</InfoPageLayout>);

export const getLayoutProps = () => {
  const assetPreload = Object.keys(assets).map((key) => {
    return {
      rel: "preload",
      href: assets[key],
      as: "image",
    };
  });
  const preconnects = [{ rel: "preconnect", href: "https://s3.amazonaws.com" }];

  const preloads = assetPreload.concat(preconnects);

  return {
    props: { metaTags: { ...DEFAULT_METATAGS }, preloads },
  };
};
export default InfoPageLayout;
