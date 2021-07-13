
import { jsx } from "@emotion/react";
import { useState, useContext, useEffect } from "react";
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
import { IoIosJournal } from "react-icons/io";
import useRouter from "../core/hooks/useRouter";
import SearchBar from "./SearchBar";
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
            minW={["100%", "50%", "60%", "80%", null, "80%"]}
            id="SearchBarwButtons"
            position="relative"
            alignItems="baseline"
            // bgColor="unsafe.100"
          >
            <IconButton
              ml={4}
              colorScheme="blue"
              aria-label="App navigation"
              icon={<IoIosJournal />}
              onClick={() => {
                ui.isMobileView
                  ? ui.setSidebarToggled(!ui.sidebarToggled)
                  : ui.setSidebarVisible(!ui.sidebarVisible);
              }}
            />
            <SearchBar
              pl={4}
              position="absolute"
              left="64px"
              w={
                isSearchBarActive
                  ? [
                      "100%",
                      "calc(100% - 80px)",
                      "calc(100% - 0px)",
                      "calc(100% - 0px)",
                      null,
                      "100%",
                    ]
                  : ["64px", "64px", "50%", "55%", null, "60%"]
              }
              h="2rem"
              bgColor="primary.1200"
              alignSelf="center"
              transition="0.5s"
            />
            {/* <Fade in={!ui.searchBarActive}> */}
            {!ui.isMobileView && (
              <ButtonGroup
                position="relative"
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
                justifyContent="space-between"
                width={["64px", "70%", "60%", "45%", null, "40%"]}
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
                {/* <Button>Explore</Button> */}
                {/* <Button>Docs</Button> */}
              </ButtonGroup>
            )}
            {/* </Fade> */}
          </Flex>
          {/* <Spacer /> */}

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
            {/* <IconButton>Explore</IconButton>
        <IconButton>Docs</IconButton> */}
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
                // size={["md", "lg", null, "md"]}
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

            <SearchBar
              pl={4}
              // position="absolute"
              w={
                isSearchBarActive
                  ? [
                      "100%",
                      "calc(100%)",
                      "calc(100% - 64px)",
                      "calc(100% - 164px)",
                      null,
                      "100%",
                    ]
                  : ["32px", "32px", "40%", "55%", null, "60%"]
              }
              h="2rem"
              px={isSearchBarActive ? 2 : 0}
              bgColor="primary.1200"
              alignSelf="center"
              transition="0.5s"
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
