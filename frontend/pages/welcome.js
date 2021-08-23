import React, { useContext, useEffect, useRef } from "react";
import { getLayout } from "../src/layouts/AppLayout";
import UIContext from "../src/core/providers/UIProvider/context";
import {
  Heading,
  Text,
  Button,
  Stack,
  ButtonGroup,
  Spacer,
  Radio,
  RadioGroup,
  UnorderedList,
  ListItem,
  Fade,
  chakra,
  useBoolean,
  Flex,
  IconButton,
  Tooltip,
} from "@chakra-ui/react";
import StepProgress from "../src/components/StepProgress";
import { ArrowLeftIcon, ArrowRightIcon } from "@chakra-ui/icons";
import Scrollable from "../src/components/Scrollable";
import AnalyticsContext from "../src/core/providers/AnalyticsProvider/context";
import NewSubscription from "../src/components/NewSubscription";
import StreamEntry from "../src/components/StreamEntry";
import SubscriptionsList from "../src/components/SubscriptionsList";
import { useSubscriptions } from "../src/core/hooks";
import router from "next/router";
import { FaFilter } from "react-icons/fa";

const Welcome = () => {
  console.count("render welcome!");
  const { subscriptionsCache } = useSubscriptions();
  const ui = useContext(UIContext);
  const { mixpanel, isLoaded, MIXPANEL_PROPS } = useContext(AnalyticsContext);
  const [profile, setProfile] = React.useState();
  const [showSubscriptionForm, setShowSubscriptionForm] = useBoolean(true);

  useEffect(() => {
    if (typeof window !== "undefined") {
      document.title = `Welcome to moonstream.to!`;
    }
  }, []);

  const progressButtonCallback = (index) => {
    ui.setOnboardingStep(index);
  };

  useEffect(() => {
    if (profile && isLoaded) {
      mixpanel.people.set({
        [`${MIXPANEL_PROPS.USER_SPECIALITY}`]: profile,
      });
    }
  }, [profile, MIXPANEL_PROPS, isLoaded, mixpanel]);

  const SubscriptonCreatedCallback = () => {
    setShowSubscriptionForm.off();
  };

  const scrollRef = useRef();
  const handleNextClick = () => {
    if (ui.onboardingStep < ui.onboardingSteps.length - 1) {
      ui.setOnboardingStep(ui.onboardingStep + 1);
      scrollRef?.current?.scrollIntoView();
    } else {
      ui.setisOnboardingComplete(true);
      router.push("/stream");
    }
  };

  return (
    <Scrollable>
      <Stack px="7%" pt={4} w="100%" spacing={4} ref={scrollRef}>
        <StepProgress
          numSteps={ui.onboardingSteps.length}
          currentStep={ui.onboardingStep}
          colorScheme="primary"
          buttonCallback={progressButtonCallback}
          buttonTitles={[
            "Moonstream basics",
            "Setup subscriptions",
            "How to read stream",
          ]}
          style="arrows"
        />

        {ui.onboardingStep === 0 && (
          <Fade in>
            <Stack spacing={4}>
              <Stack
                px={12}
                // mt={24}
                bgColor="gray.50"
                borderRadius="xl"
                boxShadow="xl"
                py={4}
              >
                <Heading as="h4" size="md">
                  Greetings traveller!
                </Heading>
                <Text fontWeight="semibold" pl={2}>
                  {" "}
                  We are very excited to see you onboard!
                </Text>

                <Text fontWeight="semibold" pl={2}>
                  Moonstream is a product which helps anyone participate in
                  decentralized finance. From the most sophisticated flash
                  arbitrageurs to people looking for yield from currency that
                  would otherwise lie dormant in their exchange accounts.
                </Text>
                <Text fontWeight="semibold" pl={2}>
                  Moonstream is ment to give you critical insights needed to
                  succeed in your crypto quest!
                </Text>
              </Stack>
              <Stack
                px={12}
                // mt={24}
                bgColor="gray.50"
                borderRadius="xl"
                boxShadow="xl"
                py={4}
              >
                <Heading as="h4" size="md">
                  How does Moonstream work?
                </Heading>
                <chakra.span fontWeight="semibold" pl={2}>
                  <Text fontWeight="bold" display="inline">
                    We run nodes
                  </Text>{" "}
                  - Now get most precise and accurate data you can just query
                  our database. You {`don't`} need to maintain your node, and
                  still have data that miners have access to!
                </chakra.span>
                <chakra.span fontWeight="semibold" pl={2}>
                  <Text fontWeight="bold" display="inline">
                    We crawl data
                  </Text>{" "}
                  We analyze millions of transactions, data, smart contract code
                  to link all them together
                </chakra.span>

                <chakra.span fontWeight="semibold" pl={2}>
                  <Text fontWeight="bold" display="inline">
                    We provide data
                  </Text>{" "}
                  We allow you to fetch data trough the website or trough API
                </chakra.span>

                <chakra.span fontWeight="semibold" pl={2}>
                  <Text fontWeight="bold" display="inline">
                    We analyze data
                  </Text>{" "}
                  We find most interesting stuff and show it to you!
                </chakra.span>
              </Stack>
              <Stack
                px={12}
                // mt={24}
                bgColor="gray.50"
                borderRadius="xl"
                boxShadow="xl"
                py={4}
              >
                <Heading as="h4" size="md">
                  UI 101?
                </Heading>
                <Text fontWeight="semibold" pl={2}>
                  On the left side corner there is sidebar that you can use to
                  navigate across the website. There are following views you can
                  navigate to:
                </Text>
                <chakra.span fontWeight="semibold" pl={2}>
                  <Text fontWeight="bold" display="inline">
                    Subscriptions
                  </Text>{" "}
                  - Use this screen to set up addresses you would like to
                  monitor to.{" "}
                  <i>
                    NB: Without setting up subscriptions moonstream will have
                    quite empty feel!{" "}
                  </i>{" "}
                  No worries, we will help you to set up your subscriptions in
                  the next steps!
                </chakra.span>
                <chakra.span fontWeight="semibold" pl={2}>
                  <Text fontWeight="bold" display="inline">
                    Stream
                  </Text>{" "}
                  This view is somewhat similar to a bank statement where you
                  can define time range and see what happened in that time over
                  your subscriptions. In next steps we will show how you can
                  apply filters to it!
                </chakra.span>

                <chakra.span fontWeight="semibold" pl={2}>
                  <Text fontWeight="bold" display="inline">
                    Stream Entry
                  </Text>{" "}
                  You can see detailed view of stream cards with very specific
                  and essential data, like methods called in smart contracts
                  etc!!
                </chakra.span>

                <chakra.span fontWeight="semibold" pl={2}>
                  <Text fontWeight="bold" display="inline">
                    Analytics
                  </Text>{" "}
                  This section is under construction yet. Soon you will be able
                  to create your dashboard with data of your interest. We will
                  really appretiate if you visit that section, and fill up form
                  describing what analytical tools you would love to see there!
                </chakra.span>
              </Stack>

              <Stack
                px={12}
                // mt={24}
                bgColor="gray.50"
                borderRadius="xl"
                boxShadow="xl"
                py={4}
              >
                <Heading as="h4" size="md">
                  Tell us more about your needs?
                </Heading>
                <Text fontWeight="semibold" pl={2}>
                  In order to fetch best possible experience, we would like to
                  know some details about you
                </Text>
                <Text fontWeight="semibold" pl={2}>
                  Please tell us what profile describes you best?{" "}
                  <i>
                    This is purely analytical data, you can change it anytime
                    later
                  </i>
                </Text>
                <RadioGroup
                  onChange={setProfile}
                  value={profile}
                  fontWeight="bold"
                >
                  <Stack direction="row" justifyContent="space-evenly">
                    <Radio value="trader">I am trading crypto currency</Radio>
                    <Radio value="fund">I represent investment fund</Radio>
                    <Radio value="developer">I am developer</Radio>
                  </Stack>
                </RadioGroup>
              </Stack>
            </Stack>
          </Fade>
        )}
        {ui.onboardingStep === 1 && (
          <Fade in>
            <Stack px="7%">
              <Stack
                px={12}
                // mt={24}
                bgColor="gray.50"
                borderRadius="xl"
                boxShadow="xl"
                py={4}
                my={2}
              >
                <Heading as="h4" size="md">
                  Subscriptions
                </Heading>
                <chakra.span fontWeight="semibold" pl={2}>
                  Subscriptions is essential tool of Moonstream. We gather data
                  for you based on addresses you have subscribed for.
                  <br />
                  Subscribe to any addres which you are interested in and they
                  will become part of your stream!
                  <UnorderedList>
                    <ListItem>
                      Color - you can define color to easily identify this
                      subscription in your stream
                    </ListItem>
                    <ListItem>Address - thing you subscribe to</ListItem>
                    <ListItem>
                      Label - Its good idea to use human readible name that
                      represents address
                    </ListItem>
                    <ListItem>
                      Source - In Alpha we support only Ethereum blockchain,
                      more sources are coming soon!
                    </ListItem>
                  </UnorderedList>
                </chakra.span>
              </Stack>
              {subscriptionsCache.data.subscriptions.length > 0 &&
                !subscriptionsCache.isLoading && (
                  <>
                    <Heading>
                      {" "}
                      You already have some subscriptions set up
                    </Heading>
                  </>
                )}
              <SubscriptionsList />
              {showSubscriptionForm && (
                <>
                  <Heading pt={12}>{`Let's add new subscription!`}</Heading>

                  <NewSubscription
                    isFreeOption={true}
                    onClose={SubscriptonCreatedCallback}
                  />
                </>
              )}
              {!showSubscriptionForm && (
                <Button
                  colorScheme="suggested"
                  variant="solid"
                  onClick={() => setShowSubscriptionForm.on()}
                >
                  Add another subscription
                </Button>
              )}
            </Stack>
          </Fade>
        )}
        {ui.onboardingStep === 2 && (
          <Fade in>
            <Stack>
              <Stack
                px={12}
                // mt={24}
                bgColor="gray.50"
                borderRadius="xl"
                boxShadow="xl"
                py={4}
                my={2}
              >
                <Heading as="h4" size="md">
                  Stream
                </Heading>
                <chakra.span fontWeight="semibold" pl={2}>
                  We are almost done!
                  <br />
                  {`Stream is where you can read data you've subscribed for. Here
                  you have different cards for different subscription types.`}
                  <br />
                  If card has some extra details - there will be orange button
                  on right hand side inviting you to see more!
                  <br />
                  Below is typical card for ethereum blockchain event. Useful
                  information right on the card:
                  <UnorderedList py={2}>
                    <ListItem>Hash - unique ID of the event </ListItem>
                    <ListItem>
                      From - sender address. If it is one of your subscription
                      addresses - will appear in color and with label{" "}
                    </ListItem>
                    <ListItem>
                      To - receiver address. If it is one of your subscription
                      addresses - will appear in color and with label{" "}
                    </ListItem>
                    <ListItem>
                      Nonce - Counter how many transactions address has sent. It
                      also determines sequence of transaction!{" "}
                    </ListItem>
                    <ListItem>
                      Gas Price - this is how much ether is being paid per gas
                      unit
                    </ListItem>
                    <ListItem>
                      Gas - Ammount of gas this event consumes
                    </ListItem>
                  </UnorderedList>
                </chakra.span>
              </Stack>
              <Stack
                pb={ui.isMobileView ? 24 : 8}
                w={ui.isMobileView ? "100%" : "calc(100% - 300px)"}
                alignSelf="center"
              >
                <Flex h="3rem" w="100%" bgColor="gray.100" alignItems="center">
                  <Flex maxW="90%"></Flex>
                  <Spacer />
                  <Tooltip
                    variant="onboarding"
                    placement={ui.isMobileView ? "bottom" : "right"}
                    label="Filtering menu"
                    isOpen={true}
                    maxW="150px"
                    hasArrow
                  >
                    <IconButton
                      mr={4}
                      // onClick={onOpen}
                      colorScheme="primary"
                      variant="ghost"
                      icon={<FaFilter />}
                    />
                  </Tooltip>
                </Flex>
                <StreamEntry
                  mt={20}
                  entry={{
                    event_type: "ethereum_blockchain",
                    from_address: "this is address from",
                    to_address: "this is to address",
                    hash: "this is hash",
                  }}
                  showOnboardingTooltips={true}
                />
              </Stack>
              <Stack
                px={12}
                // mt={24}
                bgColor="gray.50"
                borderRadius="xl"
                boxShadow="xl"
                py={4}
                my={2}
              >
                <Heading as="h4" size="md">
                  Applying filters
                </Heading>
                <chakra.span fontWeight="semibold" pl={2}>
                  You can apply various filters by clicking filter menu button
                  <br />
                  {`Right now you can use it to select address from and to, we are adding more complex queries soon, stay tuna! `}
                  <br />
                </chakra.span>
              </Stack>
            </Stack>
          </Fade>
        )}

        <ButtonGroup>
          <Button
            colorScheme="secondary"
            leftIcon={<ArrowLeftIcon />}
            variant="outline"
            hidden={ui.onboardingStep === 0}
            disabled={ui.onboardingStep === 0}
            onClick={() => {
              ui.setOnboardingStep(ui.onboardingStep - 1);
              scrollRef?.current?.scrollIntoView();
            }}
          >
            Previous
          </Button>
          <Spacer />
          <Button
            colorScheme="secondary"
            variant="solid"
            rightIcon={<ArrowRightIcon />}
            // hidden={!(ui.onboardingStep < ui.onboardingSteps.length - 1)}
            // disabled={!(ui.onboardingStep < ui.onboardingSteps.length - 1)}
            onClick={() => handleNextClick()}
          >
            {ui.onboardingStep < ui.onboardingSteps.length - 1
              ? `Next`
              : `Finish `}
          </Button>
        </ButtonGroup>
      </Stack>
    </Scrollable>
  );
};
Welcome.getLayout = getLayout;
export default Welcome;
