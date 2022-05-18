import React, { useContext } from "react";
import { Container } from "@chakra-ui/react";
import RouteButton from "../../src/components/RouteButton";
import mixpanel from "mixpanel-browser";
import { getLayout, getLayoutProps } from "../../src/layouts/WideInfoPage";
import { AWS_ASSETS_PATH } from "../../src/core/constants";
import { MIXPANEL_EVENTS } from "../../src/core/providers/AnalyticsProvider/constants";
import FeatureCard from "../../src/components/FeatureCard";
import useRouter from "../../src/core/hooks/useRouter";
import UIContext from "../../src/core/providers/UIProvider/context";

const assets = {
  cryptoTraders: `${AWS_ASSETS_PATH}/crypto+traders.png`,
  lender: `${AWS_ASSETS_PATH}/lender.png`,
  DAO: `${AWS_ASSETS_PATH}/DAO .png`,
  NFT: `${AWS_ASSETS_PATH}/NFT.png`,
};

const Features = () => {
  const router = useRouter();
  const ui = useContext(UIContext);

  const mixpanelReport = function (name, section) {
    const _report = function () {
      if (mixpanel.get_distinct_id()) {
        mixpanel.track(`${MIXPANEL_EVENTS.BUTTON_CLICKED}`, {
          full_url: router.nextRouter.asPath,
          buttonName: name,
          page: `features`,
          section: section,
        });
      }
    };
    return _report;
  };

  return (
    <Container id="container" maxW="container.xl">
      {!ui.isMobileView && (
        <RouteButton
          variant="orangeAndBlue"
          onClick={mixpanelReport("Learn More", "main")}
          href={"/discordleed"}
          isExternal
          minW={["150", "150", "150", "200px", "300px", "300px"]}
          fontSize={["md", "lg", "xl", "2xl", "3xl", "3xl"]}
          position="absolute"
          bottom="10px"
          right="5px"
        >
          Learn More
        </RouteButton>
      )}
      <FeatureCard
        id="airdrops"
        headingText="Airdrops"
        image={assets["lender"]}
        cardOrder={1}
        isMobile={ui.isMobileView}
        clickEvent={mixpanelReport("Learn More", "airdrops")}
      >
        <>
          Use Moonstream to distribute ERC20 tokens, NFTs, items, or
          achievements to your community. All you have to do is upload a
          spreadsheet listing the amount that each community member should
          receive.
          <br />
          <br />
          Our smart contracts and APIs handle the rest. Integrate your frontends
          or game clients with our APIs for full control over the claim
          experience. Use Moonstream-backed leaderboards to automatically reward
          players for their on-chain activity.
          <br />
          <br />
          Gaming projects have used Moonstream to drop over $80,000,000 worth of
          tokens and items to date.
        </>
      </FeatureCard>
      <FeatureCard
        id="minigames"
        headingText="Minigames"
        image={assets["DAO"]}
        cardOrder={-1}
        isMobile={ui.isMobileView}
        clickEvent={mixpanelReport("Learn More", "minigames")}
      >
        <>
          Use Moonstream to deploy on-chain minigames into your project. Our
          growing minigame library contains games of various genres. Use these
          minigames as faucets to tokens into your economy, and as sinks to take
          tokens out of your economy.
          <br />
          <br />
          Our minigame smart contracts process over $700,000,000 per month in
          transaction volume.
        </>
      </FeatureCard>
      <FeatureCard
        id="lootboxes"
        headingText="Lootboxes"
        image={assets["cryptoTraders"]}
        cardOrder={1}
        isMobile={ui.isMobileView}
        clickEvent={mixpanelReport("Learn More", "lootboxes")}
      >
        <>
          Use Moonstream Lootboxes to reward your players on-chain for
          completing quests, defeating bosses, or improving your community.
          Lootboxes can hold ERC20 tokens, items, consumables, or NFTs.
          Moonstream Lootboxes can be randomized using Chainlink VRF and you
          have full control over drop rates.
          <br />
          <br />
          There are currently over 14,000 Moonstream Lootboxes in circulation.
        </>
      </FeatureCard>
      <FeatureCard
        id="crafting"
        headingText="Crafting"
        image={assets["NFT"]}
        cardOrder={-1}
        isMobile={ui.isMobileView}
        clickEvent={mixpanelReport("Learn More", "crafting")}
      >
        <>
          Use Moonstream to set up a fully on-chain crafting system and give
          your players the power to create new items in your game economy.
          Productive players are the key to sustainable blockchain games, and
          Moonstream Crafting allows your players to act as producers.
          <br />
          <br />
          Upload your crafting recipes as spreadsheets and watch as players
          craft items that breathe life into your economy. Moonstream Crafting
          is an alpha feature of our engine. Reach out to us on Discord for
          early access.
        </>
      </FeatureCard>
    </Container>
  );
};

Features.getLayout = getLayout;

export async function getStaticProps() {
  const metaTags = {
    title: "Moonstream: Features page",
    description: "Descriptions of Moonstream services",
    keywords:
      "blockchain, crypto, data, trading, smart contracts, ethereum, solana, transactions, defi, finance, decentralized, analytics, product, whitepapers",
    url: "https://www.moonstream.to/features",
  };
  const layoutProps = getLayoutProps();
  layoutProps.props.metaTags = { ...layoutProps.props.metaTags, ...metaTags };
  return { ...layoutProps };
}

export default Features;
