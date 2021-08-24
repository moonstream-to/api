import React, { useEffect, useState, useLayoutEffect } from "react";
import {
  Heading,
  Text,
  Flex,
  Link,
  Stack,
  chakra,
  useMediaQuery,
  UnorderedList,
  ListItem,
  useBreakpointValue,
} from "@chakra-ui/react";
import { DEFAULT_METATAGS, AWS_ASSETS_PATH } from "../../src/core/constants";
export async function getStaticProps() {
  return {
    props: { metaTags: { ...DEFAULT_METATAGS } },
  };
}

const assets = {
  background720: `${AWS_ASSETS_PATH}/product-background-720x405.png`,
  background1920: `${AWS_ASSETS_PATH}/product-background-720x405.png`,
  background2880: `${AWS_ASSETS_PATH}/product-background-720x405.png`,
  background3840: `${AWS_ASSETS_PATH}/product-background-720x405.png`,
};

const Product = () => {
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
    assets[
      "background720"
    ] = `${AWS_ASSETS_PATH}/product-background-720x405.png`;
    assets[
      "background1920"
    ] = `${AWS_ASSETS_PATH}/product-background-1920x1080.png`;
    assets[
      "background2880"
    ] = `${AWS_ASSETS_PATH}/product-background-2880x1620.png`;
    assets[
      "background3840"
    ] = `${AWS_ASSETS_PATH}/product-background-3840x2160.png`;
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
    imageLoader720.src = `${AWS_ASSETS_PATH}/product-background-720x405.png`;
    imageLoader720.onload = () => {
      setBackgroundLoaded720(true);
    };
  }, []);

  useLayoutEffect(() => {
    const imageLoader1920 = new Image();
    imageLoader1920.src = `${AWS_ASSETS_PATH}/product-background-1920x1080.png`;
    imageLoader1920.onload = () => {
      setBackgroundLoaded1920(true);
    };
  }, []);

  useLayoutEffect(() => {
    const imageLoader2880 = new Image();
    imageLoader2880.src = `${AWS_ASSETS_PATH}/product-background-2880x1620.png`;
    imageLoader2880.onload = () => {
      setBackgroundLoaded2880(true);
    };
  }, []);

  useLayoutEffect(() => {
    const imageLoader3840 = new Image();
    imageLoader3840.src = `${AWS_ASSETS_PATH}/product-background-3840x2160.png`;
    imageLoader3840.onload = () => {
      setBackgroundLoaded3840(true);
    };
  }, []);

  const margin = useBreakpointValue({
    base: "1%",
    sm: "2%",
    md: "3%",
    lg: "15%",
    xl: "20%",
    "2xl": "25%",
  });

  return (
    <Flex
      bgPos="bottom"
      bgColor="transparent"
      backgroundImage={`url(${assets[`${background}`]})`}
      bgSize="cover"
      // boxSize="full"
      minH="100vh"
      direction="column"
      alignItems="center"
      pb={24}
    >
      <Stack mx={margin} my={12} maxW="1700px">
        <Heading as="h2" size="md" w="100%" px={12} py={2} borderTopRadius="xl">
          {`Why you'll love moonstream`}
        </Heading>
        <chakra.span pl={2} px={12} py={2}>
          <Text mb={2}>
            We strive for financial inclusion. With cryptocurrencies becoming
            mainstream, now is the time for anyone with a computer and access to
            the Internet to utilize this opportunity to make passive income.
            We’re here to make it easier.
          </Text>
          <Text mb={2}>
            Right now our source of data is Ethereum blockchain. Our goal is to
            provide a live view of the transactions taking place on every public
            blockchain - from the activity of specific accounts or smart
            contracts to updates about general market movements.
          </Text>
          <Text mb={2}>
            This information comes from the blockchains themselves, from their
            mempools/transaction pools, and from centralized exchanges, social
            media, and the news. This forms a stream of information tailored to
            your specific needs.
          </Text>
          <Text mb={2}>
            We’re giving you a macro view of the crypto market with direct
            access from Moonstream dashboards to execute transactions. You can
            also set up programs which execute (on- or off-chain) when your
            stream meets certain conditions.
          </Text>
          <Text mb={2}>
            Moonstream is accessible through dashboard, API and webhooks.
          </Text>
          <Text mb={2}>
            Moonstream’s financial inclusion goes beyond providing access to
            data. All of our work is open source as we do not believe that
            proprietary technologies are financially inclusive.
          </Text>
          <Text mb={2}>
            You can read{" "}
            <Link
              textColor="primary.500"
              isExternal
              href="https://github.com/bugout-dev/moonstream"
            >
              our code on GitHub.
            </Link>{" "}
            and keep track of our progress using{" "}
            <Link
              textColor="primary.500"
              isExternal
              href="https://github.com/bugout-dev/moonstream/milestones"
            >
              the Moonstream milestones
            </Link>
            .
          </Text>
        </chakra.span>
      </Stack>
      <Stack mx={margin} mb={12} maxW="1700px" bgTra>
        <Heading as="h2" size="md" w="100%" px={12} py={2} borderTopRadius="xl">
          Product
        </Heading>
        <chakra.span pl={2} px={12} py={2}>
          <Text mb={2}>
            Moonstream is a product which helps anyone participate in
            decentralized finance. From the most sophisticated flash
            arbitrageurs to people looking for yield from currency that would
            otherwise lie dormant in their exchange accounts.
          </Text>
          <Text mb={2}>
            We aim to go far beyond raw transaction information, enriching our
            view with context from centralized exchanges, the news, social
            media, and smart contract analysis.
          </Text>
          <Text mb={2}>
            Moonstream users can subscribe to events from any blockchain - from
            the activity of specific accounts or smart contracts to updates
            about general market movements. This information comes from the
            blockchains themselves, from their <b>mempools/transaction</b>{" "}
            pools, and from centralized exchanges, social media, and the news.
            This forms a stream of information tailored to their specific needs.
          </Text>
          <Text mb={2}>
            They can use this information to execute transactions directly from
            the Moonstream frontend or they can set up programs which execute
            (on- or off-chain) when their stream meets certain conditions.
          </Text>
          <Text mb={2}>
            Moonstream will be accessible to software through our API and
            webhooks.
          </Text>
          <chakra.span>
            <Text>Moonstream customers are:</Text>
            <UnorderedList w="75%" pl={4}>
              <ListItem>
                <b>Development teams deploying decentralized applications -</b>
                They use Moonstream to analyze how users are calling their
                dapps, and set up alerts for suspicious activity.{" "}
              </ListItem>
              <ListItem>
                <b>Algorithmic funds - </b> They use Moonstream to execute
                transactions directly on-chain under prespecified conditions.
              </ListItem>
              <ListItem>
                <b>Crypto traders -</b> They use Moonstream to evaluate trading
                strategies based on data from centralized exchanges, the
                blockchain, and the transaction pool.
              </ListItem>
            </UnorderedList>
          </chakra.span>
          <Text my={2}>
            Moonstream’s financial inclusion goes beyond providing access to
            data. We also help validators and stakers on proof of stake chains
            earn rewards in excess of the validation rewards. We pay validators
            to send mempool/transaction pool data back to Moonstream, and they
            divide these payments between themselves and their stakers. This
            helps validators attract more stake on proof of stake blockchains
            like Algorand, Solana, and post-merge Ethereum. It also ensures that
            Moonstream users have access to the freshest and most geographically
            diverse transaction pool data on the market.
          </Text>
          <Text mb={2}>
            All of our work is open source as we do not believe that proprietary
            technologies are financially inclusive.{" "}
            <Link
              textColor="primary.500"
              isExternal
              href="https://github.com/bugout-dev/moonstream"
            >
              You can read our code on GitHub.
            </Link>
          </Text>
        </chakra.span>
      </Stack>
    </Flex>
  );
};
export default Product;
