import React from "react";
import { Flex, Heading } from "@chakra-ui/react";
import { getLayout, getLayoutProps } from "../src/layouts/InfoPageLayout";
import WhitepaperCard from "../src/components/molecules/WhitepaperCard";
import { AWS_ASSETS_PATH } from "../src/core/constants";

const Papers = () => {
  return (
    <Flex direction="column" px="7%" width="100%" alignItems="center" pb="40px">
      <Heading pb={["40px", "40px", "60px"]} pt={["122px", "122px", "142px"]}>
        Whitepapers
      </Heading>
      <WhitepaperCard
        maxW={["340px", "340px", "890px"]}
        href="https://github.com/bugout-dev/moonstream/blob/main/datasets/nfts/papers/ethereum-nfts.pdf"
        img={`${AWS_ASSETS_PATH}/nft_market_analysis_i.png`}
        title="An analysis of 7,020,950 NFT transactions on the Ethereum blockchain"
        date="October 22, 2021"
        text="We present the Ethereum NFTs dataset, a representation of the activity on the Ethereum non-fungible token (NFT) market between April 1, 2021 and September 25, 2021, constructed purely from on-chain data. This dataset consists of all 7 020 950 token mints and transfers across 727 102 accounts between block 12 150 245 and block 13 296 011."
      />
    </Flex>
  );
};

Papers.getLayout = getLayout;
export async function getStaticProps() {
  const metaTags = {
    title: "Moonstream: Whitepapers",
    description: "Whitepapers by moonstream.to",
    keywords:
      "blockchain, crypto, data, trading, smart contracts, ethereum, solana, transactions, defi, finance, decentralized, analytics, product, whitepapers",
    url: "https://www.moonstream.to/whitepapers",
  };
  const layoutProps = getLayoutProps();
  layoutProps.props.metaTags = { ...layoutProps.props.metaTags, ...metaTags };
  return { ...layoutProps };
}

export default Papers;
