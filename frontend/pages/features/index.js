import React, { useContext } from "react";
import { Container } from "@chakra-ui/react";
import RouteButton from "../../src/components/RouteButton";
import { getLayout, getLayoutProps } from "../../src/layouts/WideInfoPage";
import { AWS_ASSETS_PATH } from "../../src/core/constants";
import FeatureCard from "../../src/components/FeatureCard";
import UIContext from "../../src/core/providers/UIProvider/context";
import AnalyticsContext from "../../src/core/providers/AnalyticsProvider/context";

const assets = {
  airdrop: `${AWS_ASSETS_PATH}/airdrop.png`,
  openLootbox: `${AWS_ASSETS_PATH}/open-lootbox.png`,
  craftingRecipe: `${AWS_ASSETS_PATH}/crafting-recipe.png`,
  minigame: `${AWS_ASSETS_PATH}/minigame.png`,
};

const Features = () => {
  const ui = useContext(UIContext);
  const { buttonReport } = useContext(AnalyticsContext);

  return (
    <Container id="container" maxW="1238" mt="142px" p="0px">
      {!ui.isMobileView && (
        <RouteButton
          variant="plainOrange"
          onClick={() => buttonReport("Learn More", "main")}
          href={"/discordleed"}
          isExternal
          minW={["150", "150", "150", "200px", "300px", "300px"]}
          fontSize={["md", "lg", "xl", "2xl", "3xl", "3xl"]}
          position="absolute"
          bottom="10px"
          right="10px"
        >
          Learn More
        </RouteButton>
      )}
      <FeatureCard
        pt="0px"
        id="airdrops"
        headingText="Airdrops"
        image={assets["airdrop"]}
        cardOrder={1}
        isMobile={ui.isMobileView}
        onClick={() => buttonReport("Learn More", "airdrops")}
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
        image={assets["minigame"]}
        cardOrder={-1}
        isMobile={ui.isMobileView}
        onClick={() => buttonReport("Learn More", "minigames")}
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
        image={assets["openLootbox"]}
        cardOrder={1}
        isMobile={ui.isMobileView}
        onClick={() => buttonReport("Learn More", "lootboxes")}
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
        image={assets["craftingRecipe"]}
        cardOrder={-1}
        isMobile={ui.isMobileView}
        pb="40px"
        onClick={() => buttonReport("Learn More", "crafting")}
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
