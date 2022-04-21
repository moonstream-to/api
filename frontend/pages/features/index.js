import React, { useEffect, useState, useLayoutEffect } from "react";
import dynamic from "next/dynamic";
import { getLayout } from "../../src/layouts/WideInfoPage";
import {
  Text,
  Flex,
  Stack,
  useMediaQuery,
  useBreakpointValue,
  Center,
} from "@chakra-ui/react";
import { AWS_ASSETS_PATH } from "../../src/core/constants";
import mixpanel from "mixpanel-browser";
import Link from "next/link";
import {
  MIXPANEL_PROPS,
  MIXPANEL_EVENTS,
} from "../../src/core/providers/AnalyticsProvider/constants";
import { useRouter } from "../../src/core/hooks";
import SplitWithImage from "../../src/components/SplitWithImage";
import RouteButton from "../../src/components/RouteButton";

const FaStoreAlt = dynamic(() =>
  import("react-icons/fa").then((mod) => mod.FaStoreAlt)
);

const GiRiver = dynamic(() =>
  import("react-icons/gi").then((mod) => mod.GiRiver)
);

const GiCrossedChains = dynamic(() =>
  import("react-icons/gi").then((mod) => mod.GiCrossedChains)
);

const GiChainedHeart = dynamic(() =>
  import("react-icons/gi").then((mod) => mod.GiChainedHeart)
);

const MdOutlineVerifiedUser = dynamic(() =>
  import("react-icons/md").then((mod) => mod.MdOutlineVerifiedUser)
);

const GiRadarCrossSection = dynamic(() =>
  import("react-icons/gi").then((mod) => mod.GiRadarCrossSection)
);

const GiMedallist = dynamic(() =>
  import("react-icons/gi").then((mod) => mod.GiMedallist)
);

const GiRobotGolem = dynamic(() =>
  import("react-icons/gi").then((mod) => mod.GiRobotGolem)
);

const CgUserlane = dynamic(() =>
  import("react-icons/cg").then((mod) => mod.CgUserlane)
);

const GiChaingun = dynamic(() =>
  import("react-icons/gi").then((mod) => mod.GiChaingun)
);

const GiQuickSlash = dynamic(() =>
  import("react-icons/gi").then((mod) => mod.GiQuickSlash)
);

const GiConcentrationOrb = dynamic(() =>
  import("react-icons/gi").then((mod) => mod.GiConcentrationOrb)
);

const GiTakeMyMoney = dynamic(() =>
  import("react-icons/gi").then((mod) => mod.GiTakeMyMoney)
);

const FaGithubSquare = dynamic(() =>
  import("react-icons/fa").then((mod) => mod.FaGithubSquare)
);
const GiMeshBall = dynamic(() =>
  import("react-icons/gi").then((mod) => mod.GiMeshBall)
);

const VscOrganization = dynamic(() =>
  import("react-icons/vsc").then((mod) => mod.VscOrganization)
);

const assets = {
  cryptoTraders: `${AWS_ASSETS_PATH}/crypto+traders.png`,
  lender: `${AWS_ASSETS_PATH}/lender.png`,
  DAO: `${AWS_ASSETS_PATH}/DAO .png`,
  NFT: `${AWS_ASSETS_PATH}/NFT.png`,
  smartDevelopers: `${AWS_ASSETS_PATH}/smart+contract+developers.png`,
};

const Product = () => {
  const router = useRouter();

  return (
    <Stack
      direction={"column"}
      spacing={9}
      mx="7%"
      overscrollBehaviorY={"contain"}
    >
      <SplitWithImage
        key={"SplitWithImage-3"}
        cta={{
          colorScheme: "orange",
          onClick: () => {
            router.push("/whitepapers");
          },
          label: "NFT market report",
        }}
        socialButton={{
          url: "https://discord.gg/K56VNUQGvA",
          title: "Contact us on discord",
          icon: "discord",
        }}
        elementName={"element1"}
        colorScheme="green"
        badge={`Moonstream analytics`}
        bullets={[
          {
            text: `See how value flows into and out of every component of your economy.`,
            icon: GiRiver,
            color: "green.50",
            bgColor: "green.900",
          },
          {
            text: `Track inflation or deflation of your currencies.`,
            icon: GiTakeMyMoney,
            color: "green.50",
            bgColor: "green.900",
          },
          {
            text: `Track the concentration of wealth in your economy.`,
            icon: GiConcentrationOrb,
            color: "green.50",
            bgColor: "green.900",
          },
        ]}
        imgURL={assets["cryptoTraders"]}
      />
      <SplitWithImage
        key={"SplitWithImage-2"}
        socialButton={{
          url: "https://discord.gg/K56VNUQGvA",
          title: "Contact us on discord",
          icon: "discord",
        }}
        elementName={"element3"}
        colorScheme="orange"
        badge={`Moonstream engine`}
        bullets={[
          {
            text: `Deploy customizable and upgradable characters, items, and currencies into your economy`,
            icon: GiCrossedChains,
            color: "orange.50",
            bgColor: "orange.900",
          },
          {
            text: `Monitor interactions between these tokens`,
            icon: GiChainedHeart,
            color: "orange.50",
            bgColor: "orange.900",
          },
          {
            text: `Secure the tokens with Moonstream defense bots.`,
            icon: GiChaingun,
            color: "orange.50",
            bgColor: "orange.900",
          },
        ]}
        imgURL={assets["lender"]}
      />
      <SplitWithImage
        key={"SplitWithImage-1"}
        mirror
        socialButton={{
          url: "https://discord.gg/K56VNUQGvA",
          title: "Contact us on discord",
          icon: "discord",
        }}
        elementName={"element3"}
        colorScheme="red"
        badge={`Moonstream Loyalty`}
        bullets={[
          {
            text: `Track the most active participants in your economy and easily give them rewards for their engagement.`,
            icon: VscOrganization,
            color: "red.50",
            bgColor: "red.900",
          },
          {
            text: `Create and distribute whitelist tokens for your pre-sales. Make them tradeable on markets like OpenSea.`,
            icon: GiMedallist,
            color: "red.50",
            bgColor: "red.900",
          },
          {
            text: `Manage KYC information about your community.`,
            icon: CgUserlane,
            color: "red.50",
            bgColor: "red.900",
          },
        ]}
        imgURL={assets["DAO"]}
      />
      <SplitWithImage
        key={"SplitWithImage-0"}
        socialButton={{
          url: "https://discord.gg/K56VNUQGvA",
          title: "Contact us on discord",
          icon: "discord",
        }}
        elementName={"element3"}
        colorScheme="green"
        badge={`Moonstream security`}
        bullets={[
          {
            text: `Moonstream smart contracts have been vetted in production with over $1B in value transacted.`,
            icon: MdOutlineVerifiedUser,
            color: "green.50",
            bgColor: "green.900",
          },
          {
            text: `Moonstream scanners constantly monitor accounts and transactions in your economy and identify threats in seconds.`,
            icon: GiRadarCrossSection,
            color: "green.50",
            bgColor: "green.900",
          },
          {
            text: `One-click deploy defense bots which counter attacks as soon as they are detected.`,
            icon: GiRobotGolem,
            color: "green.50",
            bgColor: "green.900",
          },
        ]}
        imgURL={assets["smartDevelopers"]}
      />
    </Stack>
  );
};

export async function getStaticProps() {
  const metaTags = {
    title: "Moonstream.to: web3 analytics",
    description:
      "Moonstream brings product analytics to web3. Instantly get analytics for any smart contract you write.",
    keywords:
      "blockchain, crypto, data, trading, smart contracts, ethereum, solana, transactions, defi, finance, decentralized, analytics, product",
    url: "https://www.moonstream.to/product",
    image: `${AWS_ASSETS_PATH}/product_comic/solution.png`,
  };

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
    props: { metaTags, preloads },
  };
}
Product.layoutProps = { mxDesktop: "12%" };
Product.getLayout = getLayout;
export default Product;
