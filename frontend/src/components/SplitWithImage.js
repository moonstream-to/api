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
  Spacer,
} from "@chakra-ui/react";
import React, { useContext } from "react";
import UIContext from "../core/providers/UIProvider/context";
import { FaGithubSquare } from "react-icons/fa";
import RouteButton from "../components/RouteButton";

const Feature = ({ text, icon, iconBg, bullets }) => {
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
  socialButton,
}) => {
  const buttonSize = useBreakpointValue({
    base: "md",
    sm: "md",
    md: "md",
    lg: "lg",
    xl: "lg",
    "2xl": "lg",
  });

  const ui = useContext(UIContext);

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
        <Stack spacing={4} justifyContent="center">
          <Stack direction="row">
            <Text
              id={`MoonBadge ${elementName}`}
              // id={`MoonBadge${elementName}`}
              textTransform={"uppercase"}
              color={useColorModeValue(
                `${colorScheme}.50`,
                `${colorScheme}.900`
              )}
              fontWeight={600}
              fontSize={"sm"}
              bg={useColorModeValue(`${colorScheme}.900`, `${colorScheme}.50`)}
              p={2}
              alignSelf={mirror && !ui.isMobileView ? "flex-end" : "flex-start"}
              rounded={"md"}
            >
              {badge}
            </Text>
          </Stack>
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
                <Flex w="100%" flexWrap="wrap">
                  <Button
                    colorScheme={colorScheme}
                    variant="outline"
                    mt={[0, 0, null, 16]}
                    fontSize={["xs", "sm", "lg", null, "lg"]}
                    size={buttonSize}
                    onClick={cta.onClick}
                  >
                    {cta.label}
                  </Button>
                  <Spacer />
                  {socialButton && (
                    <RouteButton
                      isExternal
                      href={socialButton.url}
                      mt={[0, 0, null, 16]}
                      fontSize={["xs", "sm", "lg", null, "lg"]}
                      size={buttonSize}
                      variant="outline"
                      colorScheme="primary"
                      leftIcon={<FaGithubSquare />}
                    >
                      Check out our github
                    </RouteButton>
                  )}
                </Flex>
              </Center>
            </Container>
          </Stack>
        </Stack>
        {(!mirror || ui.isMobileView) && (
          <Flex justifyContent="center">
            <Image
              rounded={"md"}
              alt={"feature image"}
              src={imgURL}
              objectFit={"contain"}
              // boxSize={ui.isMobileView ? "lg" : null}
            />
          </Flex>
        )}
      </SimpleGrid>
    </Container>
  );
};

export default SplitWithImage;
