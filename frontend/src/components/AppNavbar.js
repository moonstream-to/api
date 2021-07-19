import React, { useState, useContext, useEffect } from "react";
import RouterLink from "next/link";
import {
  Flex,
  Button,
  Image,
  ButtonGroup,
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
} from "@chakra-ui/react";
import {
  HamburgerIcon,
  PlusSquareIcon,
  QuestionOutlineIcon,
  BellIcon,
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

  const SupportPopover = () => {
    return (
      <Popover usePortal>
        <PopoverTrigger>
          <IconButton
            colorScheme="primary"
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
                href="mailto:support@bugout.dev"
                fontWeight="600"
                textColor="primary.500"
              >
                support@bugout.dev
              </Link>
            </Text>
            <Text fontWeight="700" textColor="primary.500">
              <Link href="https://join.slack.com/t/bugout-dev/shared_invite/zt-fhepyt87-5XcJLy0iu702SO_hMFKNhQ">
                Slack
              </Link>
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
          <Flex
            width="100%"
            id="SearchBarwButtons"
            position="relative"
            alignItems="baseline"
            justifyContent="flex-end"
          >
            {!ui.isMobileView && (
              <ButtonGroup
                // position="relative"
                left={
                  isSearchBarActive
                    ? "100%"
                    : ["64px", "30%", "50%", "55%", null, "60%"]
                }
                // hidden={ui.searchBarActive}
                display={isSearchBarActive ? "hidden" : "block"}
                variant="link"
                colorScheme="secondary"
                spacing={4}
                px={2}
                zIndex={ui.searchBarActive ? -10 : 0}
                size={["xs", "xs", "xs", "lg", null, "lg"]}
              >
                <RouterLink href="/pricing" passHref>
                  <Button color="white" fontWeight="400">
                    Pricing
                  </Button>
                </RouterLink>
                <RouterLink href="/product" passHref>
                  <Button color="white" fontWeight="400">
                    Product
                  </Button>
                </RouterLink>
              </ButtonGroup>
            )}
          </Flex>

          <Flex justifyContent="flex-end" width="30%" pr={2}>
            <IconButton
              hidden={true}
              colorScheme="primary"
              variant="link"
              h="32px"
              size="lg"
              color="gray.100"
              borderColor="transparent"
              borderWidth={0}
              aria-label="Create new"
              icon={<PlusSquareIcon />}
            />
            <SupportPopover />

            <IconButton
              hidden={true}
              colorScheme="primary"
              variant="link"
              h="32px"
              size="lg"
              color="gray.100"
              outlineColor="transparent"
              // colorScheme="blue"
              aria-label="Alerts"
              icon={<BellIcon />}
            />
            <AccountIconButton
              colorScheme="primary"
              variant="link"
              color="gray.100"
              size="lg"
              h="32px"
            />
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
                  router.params?.entryId && ui.entriesViewMode === "entry"
                    ? ui.setEntriesViewMode("list")
                    : router.nextRouter.back();
                }}
              />
            )}
            {!isSearchBarActive && (
              <Link href="/" alignSelf="center">
                <Image
                  alignSelf="center"
                  // as={Link}
                  // to="/"
                  h="2.5rem"
                  minW="2.5rem"
                  src="/icons/ant-white.svg"
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
                  router.params?.entryId && ui.entriesViewMode === "list"
                    ? ui.setEntriesViewMode("entry")
                    : history.forward();
                }}
              />
            )}
            {!isSearchBarActive && <SupportPopover />}

            {!isSearchBarActive && (
              <AccountIconButton
                variant="link"
                mx={0}
                justifyContent="space-evenly"
                alignContent="center"
                h="32px"
                size={iconSize}
                colorScheme="primary"
              />
            )}
          </Flex>
        </Flex>
      )}
    </>
  );
};

export default AppNavbar;
