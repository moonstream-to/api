import React, { useEffect, useState, useLayoutEffect, useContext } from "react";
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
  Box,
  SimpleGrid,
} from "@chakra-ui/react";
import { DEFAULT_METATAGS, AWS_ASSETS_PATH } from "../../src/core/constants";
import UIContext from "../../src/core/providers/UIProvider/context";
import TeamCard from "../../src/components/TeamCard";

const assets = {
  background720: `${AWS_ASSETS_PATH}/blog-background-720x405.png`,
  background1920: `${AWS_ASSETS_PATH}/blog-background-720x405.png`,
  background2880: `${AWS_ASSETS_PATH}/blog-background-720x405.png`,
  background3840: `${AWS_ASSETS_PATH}/blog-background-720x405.png`,
  team: `${AWS_ASSETS_PATH}/Team-page-illustration.png`,
  dragonfly: `${AWS_ASSETS_PATH}/dragonfly.jpg`,
  ladybird: `${AWS_ASSETS_PATH}/ladybird.jpg`,
  locust: `${AWS_ASSETS_PATH}/locust.jpg`,
  mantis: `${AWS_ASSETS_PATH}/mantis.jpg`,
  centipede: `${AWS_ASSETS_PATH}/centipede.jpg`,
  spider: `${AWS_ASSETS_PATH}/spider.jpg`,
  ant: `${AWS_ASSETS_PATH}/ant.jpg`,
  firefly: `${AWS_ASSETS_PATH}/firefly.jpg`,
};

const Product = () => {
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

  const margin = ui.isMobileView ? "3%" : "22%";

  return (
    <Flex
      bgPos="bottom"
      bgColor="transparent"
      backgroundImage={`url(${assets[`${background}`]})`}
      bgSize="cover"
      minH="100vh"
      direction="column"
      alignItems="center"
      w="100%"
    >
      <Stack mx={margin} maxW="1700px" w="100%">
        <SimpleGrid
          px={12}
          alignItems="start"
          columns={{ base: 1, md: 2 }}
          // mb={24}
          spacingY={{ base: 10, md: 32 }}
          spacingX={{ base: 10, md: 24 }}
        >
          <Box>
            <Heading as="h2" size="md" w="100%" py={6} borderTopRadius="xl">
              Meet The Moonstream Team
            </Heading>
            <chakra.span pl={2} py={2}>
              <Text mb={2}>
                We are a distributed team of nerds with very strong expertise in
                math, software engineering, machine learning, and cryptography.
                Members of our team worked at Google, at OpenAI and other great
                companies.
              </Text>
              <Text mb={2}>
                We believe that the crypto world opens opportunities for
                financial inclusion. Meaning that people from all walks of life
                and financial situations can have a new source of income. We are
                passionate about developing technology that helps people become
                active participants in this field and take advantage of this
                opportunity. We’re striving to debunk harmful stereotypes and
                make the crypto field more inclusive.
              </Text>
            </chakra.span>
          </Box>
          <Box
            w="full"
            py={48}
            backgroundImage={`url(${assets[`team`]})`}
            backgroundSize="cover"
            bgPos="bottom"
            bgColor="transparent"
          ></Box>
        </SimpleGrid>
      </Stack>
      <Stack mx={margin} mb={6} mt={0} maxW="1700px" w="100%">
        <Heading
          as="h2"
          size="md"
          w="100%"
          px={12}
          pb={2}
          pt={0}
          borderTopRadius="xl"
        >
          Values that we share within our team:
        </Heading>
        <chakra.span pl={2} px={12} py={2}>
          <UnorderedList w="75%" pl={4}>
            <ListItem>
              <b>Be bold</b>
            </ListItem>
            <ListItem>
              <b>Be curious</b>
            </ListItem>
            <ListItem>
              <b>Don’t be an ass</b>
            </ListItem>
            <ListItem>
              <b>And always be kind to each other</b>
            </ListItem>
          </UnorderedList>
          <Text my={2}>
            We are always looking to hire new talents, regardless of their
            backgrounds. If you are interested in working with us, send us a
            message at{" "}
            <Link textColor="orange.900" href="mailto: careers@moonstream.to">
              careers@moonstream.to
            </Link>
          </Text>
        </chakra.span>
      </Stack>
      <Stack mx={margin} mb={12} maxW="1700px" w="100%">
        <Heading as="h2" size="md" w="100%" px={12} py={2} borderTopRadius="xl">
          Our engineering team
        </Heading>
        <Stack
          w="100%"
          direction={"row"}
          flexWrap="wrap"
          spacing={4}
          justifyContent="space-between"
          px={[3, 6, 12]}
          placeContent={"center"}
        >
          <TeamCard
            avatarURL={assets["ant"]}
            name={"Neeraj Kashyap"}
            atName={"@zomglings"}
            content={` Founder. Number theorist. Loves playing chess while programming. Fan of GO, backgammon, and video games.`}
          />
          <TeamCard
            avatarURL={assets["spider"]}
            name={"Sergei Sumarokov"}
            atName={"@kompotkot"}
            content={`Keeper of Secrets. Likes information
            security since childhood, loves mountains and goes hiking from
            time to time. Had a close call with a wild bear in a forest once.`}
          />
          <TeamCard
            avatarURL={assets["locust"]}
            name={"Andrey Dolgolev"}
            atName={"@Andrei-Dolgolev"}
            content={`Wizard. Loves mountains, bicycling, and
            hiking. A practicing Python wizard. Also likes to cook and play
            the guitar in between data witchcraft.`}
          />
          <TeamCard
            avatarURL={assets["dragonfly"]}
            name={"Tim Pechersky"}
            atName={"@peersky"}
            content={`Spectral hopper. Has special ability to perceive world trough spectral domain. Occasionaly
            shifts in time domain to spend some in doing flow
            arts, surfing, and connecting with nature.`}
          />
          <TeamCard
            avatarURL={assets["centipede"]}
            name={"Yhtyyar Sahatov"}
            atName={"@Yhtiyar"}
            content={`Wunderkind. Interested in Math, NLP. Loves
            programming language parsing and Algorithms & Data structures.
            Implementing his own dialect of LISP programming language for
            scientific calculations.`}
          />
          <TeamCard
            avatarURL={assets["mantis"]}
            name={"Kellan Wampler"}
            atName={"@wampleek"}
            content={`News junkie. Reformed mathematician. Fantasy Football enthusiast.
            Enjoys soduku and its variants. Follows artificial intelligence scene for 
            Chess and Go. Experiments with grilling recipes.`}
          />
        </Stack>
      </Stack>
      <Stack mx={margin} mb={12} maxW="1700px" w="100%">
        <Heading as="h2" size="md" w="100%" px={12} py={2} borderTopRadius="xl">
          Our marketing and growth team
        </Heading>
        <Stack
          w="100%"
          direction={"row"}
          flexWrap="wrap"
          spacing={4}
          justifyContent="space-between"
          px={[3, 6, 12]}
          placeContent={"center"}
        >
          <TeamCard
            avatarURL={assets["ladybird"]}
            name={"Sophia Aryan"}
            atName={"@pahita"}
            content={`Dreamer. An alien who pretends to be a human.
            So far so good. Loves ecstatic dance, being alone in nature and
            dreaming.`}
          />
          <TeamCard
            avatarURL={assets["mantis"]}
            name={"Daria Navoloshnikova"}
            atName={"@in_technicolor"}
            content={`Mediator. Loves stand-up comedy and
            crying at nights. Volunteered at a horse farm once. Portrait
            artist, puts the pain in painting.`}
          />
          <TeamCard
            avatarURL={assets["spider"]}
            name={"Dasha Bochkareva"}
            atName={"@dashab"}
            content={`Born explorer. Always in search of something
            new to master. Enjoys being close to the sea. Loves yoga, 
            dogs and dancing. Can walk 30km when under stress.`}
          />
          <TeamCard
            avatarURL={assets["locust"]}
            name={"Sam Kamani"}
            atName={"@samkamani"}
            content={`Extrovert. Podcaster, Author & Keynote speaker.
            Loves learning about new technology, macro economics and
            talking with other ambitious people. Plays multiplayer FPS,
            tennis or oil painting to relax.`}
          />
        </Stack>
      </Stack>
    </Flex>
  );
};

export async function getStaticProps() {
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
}
export default Product;
