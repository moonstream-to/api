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
  useBreakpointValue,
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
  imgBoxShadow,
  py,
}) => {
  var buttonSize = useBreakpointValue({
    base: { single: "sm", double: "xs" },
    sm: { single: "md", double: "sm" },
    md: { single: "md", double: "sm" },
    lg: { single: "lg", double: "lg" },
    xl: { single: "lg", double: "lg" },
    "2xl": { single: "lg", double: "lg" },
  });

  //idk why but sometimes buttonSize gets undefined
  if (!buttonSize) buttonSize = "lg";

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

  const themeColor = useColorModeValue(
    `${colorScheme}.50`,
    `${colorScheme}.900`
  );

  const bgThemeColor = useColorModeValue(
    `${colorScheme}.900`,
    `${colorScheme}.50`
  );

  return (
    <Container
      maxW={"100%"}
      py={py}
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
              boxShadow={imgBoxShadow ?? "inherit"}
            />
          </Flex>
        )}
        <Stack spacing={[2, 4]} justifyContent="center">
          {badge && (
            <Stack direction="row" placeContent={"flex-start"}>
              <Text
                id={`MoonBadge ${elementName}`}
                textTransform={"uppercase"}
                color={themeColor}
                fontWeight={600}
                fontSize={["xs", "sm"]}
                bg={bgThemeColor}
                p={[1, 2]}
                rounded={"md"}
              >
                {badge}
              </Text>
            </Stack>
          )}
          <Heading size="md">{title}</Heading>
          <Text color={`blue.500`} fontSize={["sm", "md", "lg"]}>
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

            <Flex
              w="100%"
              flexWrap="nowrap"
              display={["column", "column", null, "row"]}
            >
              {cta && (
                <Button
                  colorScheme={colorScheme}
                  w={["100%", "100%", "fit-content", null]}
                  maxW={["250px", null, "fit-content"]}
                  variant="outline"
                  mt={[0, 0, null, 16]}
                  size={socialButton ? buttonSize.double : buttonSize.single}
                  onClick={cta.onClick}
                >
                  {cta.label}
                </Button>
              )}

              {socialButton && (
                <RouteButton
                  isExternal
                  w={["100%", "100%", "fit-content", null]}
                  maxW={["250px", null, "fit-content"]}
                  href={socialButton.url}
                  mt={[0, 0, null, 16]}
                  size={socialButton ? buttonSize.double : buttonSize.single}
                  variant="outline"
                  colorScheme={colorScheme}
                  leftIcon={<FaGithubSquare />}
                >
                  git clone moonstream
                </RouteButton>
              )}
            </Flex>
          </Stack>
        </Stack>
        {(!mirror || ui.isMobileView) && (
          <Flex justifyContent="center" alignItems="center">
            <Image
              rounded={"md"}
              alt={"feature image"}
              src={imgURL}
              objectFit={"contain"}
              h="fit-content"
              boxShadow={imgBoxShadow ?? "inherit"}
            />
          </Flex>
        )}
      </SimpleGrid>
    </Container>
  );
};

export default SplitWithImage;
