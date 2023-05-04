import React, { useState, useContext, useEffect } from "react";
import RouterLink from "next/link";
import {
  Flex,
  Image,
  Text,
  IconButton,
  Link,
  Popover,
  PopoverTrigger,
  PopoverContent,
  PopoverHeader,
  PopoverBody,
  PopoverArrow,
  PopoverCloseButton,
  useBreakpointValue,
  Spacer,
  ButtonGroup,
  Button,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  Portal,
} from "@chakra-ui/react";
import {
  HamburgerIcon,
  QuestionOutlineIcon,
  ArrowLeftIcon,
  ArrowRightIcon,
  ChevronDownIcon,
} from "@chakra-ui/icons";
import useRouter from "../core/hooks/useRouter";
import UIContext from "../core/providers/UIProvider/context";
import AccountIconButton from "./AccountIconButton";
import RouteButton from "./RouteButton";
import AddNewIconButton from "./AddNewIconButton";
import {
  USER_NAV_PATHES,
  SITEMAP,
  PRIMARY_MOON_LOGO_URL,
  PAGETYPE,
} from "../core/constants";

const AppNavbar = () => {
  const ui = useContext(UIContext);
  const [isSearchBarActive, setSearchBarState] = useState(false);

  const router = useRouter();
  useEffect(() => {
    setSearchBarState(ui.searchBarActive);
  }, [ui.searchBarActive]);

  const iconSize = useBreakpointValue({
    base: "md",
    sm: "lg",
    md: "lg",
    lg: "lg",
    xl: "lg",
    "2xl": "lg",
  });

  const SupportPopover = () => {
    return (
      <Popover usePortal>
        <PopoverTrigger>
          <IconButton
            colorScheme="blue"
            variant="link"
            h="32px"
            size="lg"
            color="gray.100"
            outlineColor="transparent"
            // colorScheme="blue"
            aria-label="Request support"
            icon={<QuestionOutlineIcon />}
          />
        </PopoverTrigger>
        <PopoverContent bgColor="white.100" color="black">
          <PopoverArrow />
          <PopoverCloseButton />
          <PopoverHeader>Support</PopoverHeader>
          <PopoverBody bgColor="white">
            <Text>
              {`If you have any questions please don't hestitate to contact
            us!`}
            </Text>
            <Text>
              <Link
                href="mailto:support@moonstream.to"
                fontWeight="600"
                textColor="blue.500"
              >
                support@moonstream.to
              </Link>
            </Text>
            <Text fontWeight="700" textColor="blue.500">
              <Link href="https://discord.gg/K56VNUQGvA">Discord</Link>
            </Text>
          </PopoverBody>
        </PopoverContent>
      </Popover>
    );
  };

  return (
    <>
      {!ui.isMobileView && (
        <>
          <Flex px={2} minH="72px" maxH="72px" alignItems="center">
            <RouterLink href="/" passHref>
              <Image
                w="160px"
                py="0.75rem"
                pl={1}
                ml="15px"
                src={PRIMARY_MOON_LOGO_URL}
                alt="Moonstream To"
                cursor="pointer"
              />
            </RouterLink>
            <Spacer />
            <Flex h="100%" alignItems="center">
              <ButtonGroup variant="link" spacing={4}>
                {SITEMAP.map((item, idx) => {
                  if (
                    !item.children &&
                    item.type !== PAGETYPE.FOOTER_CATEGORY
                  ) {
                    return (
                      <RouteButton
                        key={`${idx}-${item.title}-landing-all-links`}
                        variant="link"
                        href={item.path}
                        isActive={!!(router.pathname === item.path)}
                      >
                        <Text color="black">{item.title}</Text>
                      </RouteButton>
                    );
                  } else if (!item.footerOnly) {
                    return (
                      <Menu key={`menu-${idx}`}>
                        <MenuButton
                          key={`menu-button-${idx}`}
                          as={Button}
                          rightIcon={<ChevronDownIcon />}
                          color="white"
                          fontWeight="500"
                          _expanded={{ color: "white", fontWeight: "700" }}
                          _focus={{ textDecoration: "none" }}
                          _hover={{ textDecoration: "none", fontWeight: "700" }}
                        >
                          {item.title}
                        </MenuButton>
                        <Portal>
                          <MenuList
                            zIndex={100}
                            bg="#1A1D22"
                            w="auto"
                            minW="auto"
                            borderRadius="10px"
                            p="20px 20px 10px 20px"
                            border="1px solid white"
                          >
                            {item.children.map((child, idx) => (
                              <RouterLink
                                shallow={true}
                                key={`${idx}-${item.title}-menu-links`}
                                href={child.path}
                                passHref
                              >
                                <MenuItem
                                  key={`menu-${idx}`}
                                  as={"a"}
                                  target={
                                    child.type === PAGETYPE.EXTERNAL
                                      ? "_blank"
                                      : "_self"
                                  }
                                  m={0}
                                  color="white"
                                  fontWeight="400"
                                  px="0px"
                                  mb="10px"
                                  h="22px"
                                  _hover={{
                                    backgroundColor: "black.300",
                                    color: "#F56646",
                                    fontWeight: "700",
                                  }}
                                  _focus={{ backgroundColor: "black.300" }}
                                >
                                  {child.title}
                                </MenuItem>
                              </RouterLink>
                            ))}
                          </MenuList>
                        </Portal>
                      </Menu>
                    );
                  }
                })}
                {USER_NAV_PATHES.map((item, idx) => {
                  return (
                    <RouteButton
                      key={`${idx}-${item.title}-navlink`}
                      variant="link"
                      href={item.path}
                      isActive={!!(router.nextRouter.pathname === item.path)}
                    >
                      <Text color="white">{item.title}</Text>
                    </RouteButton>
                  );
                })}
              </ButtonGroup>
              <SupportPopover />
              <AddNewIconButton
                colorScheme="blue"
                variant="link"
                color="gray.100"
                size="lg"
                h="32px"
              />
              <AccountIconButton
                colorScheme="blue"
                variant="link"
                color="gray.100"
                size="lg"
                h="32px"
              />
            </Flex>
          </Flex>
        </>
      )}
      {ui.isMobileView && (
        <Flex direction="row" w="100%" justifyContent="center">
          <Flex w="100%" justifyContent="space-evenly">
            {!isSearchBarActive && (
              <IconButton
                variant="link"
                justifyContent="space-evenly"
                alignContent="center"
                h="32px"
                m={0}
                size={iconSize}
                colorScheme="gray"
                aria-label="App navigation"
                icon={<HamburgerIcon />}
                onClick={() => {
                  ui.isMobileView
                    ? ui.setSidebarToggled(ui.sidebarToggled ? false : true)
                    : ui.setSidebarVisible(ui.sidebarVisible ? false : true);
                }}
              />
            )}
            <AddNewIconButton
              variant="link"
              justifyContent="space-evenly"
              alignContent="center"
              size={iconSize}
              colorScheme="blue"
              m={0}
              h="100%"
            />
            {!isSearchBarActive && (
              <IconButton
                m={0}
                variant="link"
                justifyContent="space-evenly"
                alignContent="center"
                h="32px"
                size={iconSize}
                colorScheme="gray"
                aria-label="App navigation"
                icon={<ArrowLeftIcon />}
                onClick={() => {
                  router.nextRouter.pathname === "/stream" &&
                  ui.isEntryDetailView
                    ? ui.setEntryDetailView(false)
                    : router.nextRouter.back();
                }}
              />
            )}
            {!isSearchBarActive && (
              <Link href="/" alignSelf="center">
                <Image
                  alignSelf="center"
                  maxH="2.5rem"
                  src={PRIMARY_MOON_LOGO_URL}
                  alt="Go to app root"
                />
              </Link>
            )}
            {!isSearchBarActive && (
              <IconButton
                m={0}
                variant="link"
                justifyContent="space-evenly"
                alignContent="center"
                h="32px"
                size={iconSize}
                colorScheme="gray"
                aria-label="App navigation"
                icon={<ArrowRightIcon />}
                onClick={() => {
                  router.nextRouter.pathname === "/stream" &&
                  !ui.isEntryDetailView
                    ? ui.setEntryDetailView(true)
                    : history.forward();
                }}
              />
            )}
            {!isSearchBarActive && <SupportPopover />}

            {!isSearchBarActive && (
              <AccountIconButton
                variant="link"
                justifyContent="space-evenly"
                alignContent="center"
                h="32px"
                size={iconSize}
                colorScheme="blue"
              />
            )}
          </Flex>
        </Flex>
      )}
    </>
  );
};

export default AppNavbar;
