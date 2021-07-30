import {
  Container,
  SimpleGrid,
  Image,
  Flex,
  Heading,
  Text,
  Stack,
  StackDivider,
  Icon,
  useColorModeValue,
  Button,
  Center,
  useBreakpointValue,
} from "@chakra-ui/react";
// import Xarrow, { useXarrow } from "react-xarrows";
import React, { useContext, useEffect } from "react";
import UIContext from "../core/providers/UIProvider/context";

const Feature = ({ text, icon, iconBg, bullets }) => {
  // const updateXarrow = useXarrow();
  useEffect(() => {
    // updateXarrow();
  }, []);
  console.log("bullets;", bullets);
  return (
    <Flex direction="column">
      <Stack direction={"row"} align={"center"}>
        <Flex
          w={8}
          maxW={8}
          maxH={8}
          h={8}
          flexShrink={0}
          align={"center"}
          justify={"center"}
          rounded={"full"}
          bg={iconBg}
        >
          {icon}
        </Flex>
        <Text fontWeight={600}>{text}</Text>
      </Stack>
      {bullets?.length > 0 && (
        <Stack pt={8} pl={8} direction={"column"} spacing={2}>
          {bullets.map((bullet, idx) => {
            return (
              <Feature
                key={`nested-bullet-${idx}-${bullet.text}`}
                iconBg={bullet.bgColor}
                text={bullet.text}
                {...bullet}
                icon={
                  <Icon as={bullet.icon} color={bullet.color} w={5} h={5} />
                }
              />
            );
          })}
        </Stack>
      )}
    </Flex>
  );
};

const SplitWithImage = ({
  badge,
  title,
  body,
  bullets,
  colorScheme,
  imgURL,
  mirror,
  elementName,
  cta,
}) => {
  const buttonSize = useBreakpointValue({
    base: "md",
    sm: "md",
    md: "md",
    lg: "lg",
    xl: "xl",
    "2xl": "xl",
  });

  const ui = useContext(UIContext);
  // const updateXarrow = useXarrow();
  const iconBgColor = useColorModeValue(
    `${colorScheme}.100`,
    `${colorScheme}.900`
  );

  const [isVisible, setVisible] = React.useState(true);
  const domRef = React.useRef();
  React.useEffect(() => {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => setVisible(entry.isIntersecting));
    });
    observer.observe(domRef.current);
    const current = domRef.current;
    return () => observer.unobserve(current);
  }, []);

  return (
    <Container
      maxW={"7xl"}
      py={0}
      className={`fade-in-section ${isVisible ? "is-visible" : ""}`}
      ref={domRef}
      // onAnimationIteration={() => updateXarrow()}
    >
      <SimpleGrid columns={{ base: 1, md: 2 }} spacing={[0, 0, 10, null, 10]}>
        {mirror && !ui.isMobileView && (
          <Flex>
            <Image
              rounded={"md"}
              alt={"feature image"}
              src={imgURL}
              objectFit={"contain"}
            />
          </Flex>
        )}
        <Stack spacing={4}>
          <Text
            id={`MoonBadge ${elementName}`}
            // id={`MoonBadge${elementName}`}
            textTransform={"uppercase"}
            color={useColorModeValue(`${colorScheme}.50`, `${colorScheme}.900`)}
            fontWeight={600}
            fontSize={"sm"}
            bg={useColorModeValue(`${colorScheme}.900`, `${colorScheme}.50`)}
            p={2}
            alignSelf={mirror && !ui.isMobileView ? "flex-end" : "flex-start"}
            rounded={"md"}
          >
            {badge}
          </Text>
          {/* <Xarrow
            dashness={{
              strokeLen: 10,
              nonStrokeLen: 15,
              animation: -2,
            }}
            color="#212990"
            showHead={false}
            start={"CryptoTraderButton"} //can be react ref
            end={`MoonBadge ${elementName}`} //or an id
          /> */}
          <Heading>{title}</Heading>
          <Text color={`primary.500`} fontSize={"lg"}>
            {body}
          </Text>
          <Stack
            spacing={4}
            divider={
              <StackDivider
                borderColor={useColorModeValue("gray.100", "gray.700")}
              />
            }
          >
            {bullets?.map((bullet, idx) => {
              console.log("bullet1", bullet?.bullets);
              return (
                <Feature
                  key={`splitWImageBullet-${idx}-${title}`}
                  icon={
                    <Icon as={bullet.icon} color={bullet.color} w={5} h={5} />
                  }
                  iconBg={bullet.bgColor}
                  text={bullet.text}
                  bullets={bullet?.bullets}
                />
              );
            })}
            <Container>
              <Center>
                <Button
                  colorScheme={colorScheme}
                  variant="outline"
                  mt={[0, 0, null, 16]}
                  textTransform={"uppercase"}
                  fontSize={["xs", "sm", "lg", null, "lg"]}
                  size={buttonSize}
                >
                  {cta}
                </Button>
              </Center>
            </Container>
          </Stack>
        </Stack>
        {(!mirror || ui.isMobileView) && (
          <Flex>
            <Image
              rounded={"md"}
              alt={"feature image"}
              src={imgURL}
              objectFit={"cover"}
            />
          </Flex>
        )}
      </SimpleGrid>
    </Container>
  );
};

export default SplitWithImage;
