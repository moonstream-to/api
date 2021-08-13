import React, { useState, useContext, useEffect, useRef } from "react";
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
  useOutsideClick,
  Tooltip,
  chakra,
} from "@chakra-ui/react";
import {
  HamburgerIcon,
  QuestionOutlineIcon,
  ArrowLeftIcon,
  ArrowRightIcon,
} from "@chakra-ui/icons";
import { MdTimeline } from "react-icons/md";
import useRouter from "../core/hooks/useRouter";
import UIContext from "../core/providers/UIProvider/context";
import AccountIconButton from "./AccountIconButton";

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

  const ref = useRef();
  useOutsideClick({
    ref: ref,
    handler: () => ui.setShowPopOvers.off(),
  });

  const SupportPopover = () => {
    return (
      <Popover usePortal isOpen={false}>
        <PopoverTrigger>
          <IconButton
            ref={ref}
            colorScheme="primary"
            variant="link"
            h="32px"
            size="lg"
            color="gray.100"
            outlineColor="transparent"
            // colorScheme="blue"
            aria-label="Request support"
            onClick={() => ui.setShowPopOvers.toggle()}
            icon={<QuestionOutlineIcon />}
          />
        </PopoverTrigger>
        <PopoverContent bgColor="white.100">
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
                textColor="primary.500"
              >
                support@moonstream.to
              </Link>
            </Text>
            <Text fontWeight="700" textColor="primary.500">
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
          <Flex width="100%" px={2}>
            <Spacer />
            <Flex placeSelf="flex-end">
              <SupportPopover />
              <AccountIconButton
                colorScheme="primary"
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
        <Flex
          direction="row"
          w="100%"
          justifyContent="center"
          justifyItems="center"
        >
          <Flex w="100%" justifyContent="space-evenly">
            {!isSearchBarActive && (
              <Tooltip
                hasArrow
                label="menu"
                isOpen={ui.showPopOvers}
                variant="onboarding"
              >
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
              </Tooltip>
            )}
            <Tooltip
              hasArrow
              label="stream view"
              isOpen={ui.showPopOvers}
              variant="onboarding"
            >
              <chakra.span alignSelf="center">
                <RouterLink href="/stream" passHref>
                  <IconButton
                    m={0}
                    variant="link"
                    justifyContent="space-evenly"
                    alignContent="center"
                    h="32px"
                    size={iconSize}
                    colorScheme="gray"
                    aria-label="go to ticker"
                    icon={<MdTimeline />}
                  />
                </RouterLink>
              </chakra.span>
            </Tooltip>

            {!isSearchBarActive && (
              <Tooltip
                hasArrow
                label="Go back"
                isOpen={ui.showPopOvers}
                variant="onboarding"
              >
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
              </Tooltip>
            )}
            {!isSearchBarActive && (
              <Tooltip
                hasArrow
                label="homepage"
                isOpen={ui.showPopOvers}
                variant="onboarding"
                // shouldWrapChildren
              >
                <Link href="/" alignSelf="center">
                  <Image
                    alignSelf="center"
                    // as={Link}
                    // to="/"
                    h="2.5rem"
                    minW="2.5rem"
                    src="https://s3.amazonaws.com/static.simiotics.com/moonstream/assets/White+logo.svg"
                    alt="Go to app root"
                  />
                </Link>
              </Tooltip>
            )}
            {!isSearchBarActive && (
              <Tooltip
                hasArrow
                label="Go forward"
                isOpen={ui.showPopOvers}
                variant="onboarding"
                // shouldWrapChildren
              >
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
              </Tooltip>
            )}
            {!isSearchBarActive && <SupportPopover />}

            {!isSearchBarActive && (
              <Tooltip
                hasArrow
                label="Account menu"
                isOpen={ui.showPopOvers}
                variant="onboarding"
                shouldWrapChildren
              >
                <AccountIconButton
                  variant="link"
                  justifyContent="space-evenly"
                  alignContent="center"
                  h="32px"
                  size={iconSize}
                  colorScheme="primary"
                />
              </Tooltip>
            )}
          </Flex>
        </Flex>
      )}
    </>
  );
};

export default AppNavbar;
