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
  Accordion,
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  AccordionIcon,
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
                  Greetings traveler!
                </Heading>
                <Text fontWeight="semibold" pl={2}>
                  We are very excited to see you onboard!
                </Text>

                <Text fontWeight="semibold" pl={2}>
                  Moonstream is a product which helps anyone participate in
                  decentralized finance.
                </Text>
                <Text fontWeight="semibold" pl={2}>
                  Moonstream is meant to give you critical insights you’ll need
                  to succeed in your crypto quest!
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
                <Accordion allowToggle>
                  <AccordionItem borderWidth={0}>
                    <h2>
                      <AccordionButton borderWidth={0}>
                        <Heading as="h4" size="md">
                          How does Moonstream work?
                        </Heading>
                        <AccordionIcon />
                      </AccordionButton>
                    </h2>
                    <AccordionPanel pb={4} borderWidth={0}>
                      <Stack direction="column">
                        <chakra.span fontWeight="semibold" pl={2}>
                          <Text fontWeight="bold" display="inline">
                            We run nodes
                          </Text>{" "}
                          - Get precise and accurate data by querying our
                          database. You’re getting the same data miners have
                          access to and you don’t have to maintain your own
                          node.
                        </chakra.span>
                        <chakra.span fontWeight="semibold" pl={2}>
                          <Text fontWeight="bold" display="inline">
                            We crawl data
                          </Text>{" "}
                          - We analyze millions of transactions, data, and smart
                          contract code to link them together.
                        </chakra.span>

                        <chakra.span fontWeight="semibold" pl={2}>
                          <Text fontWeight="bold" display="inline">
                            We provide data
                          </Text>
                          - You can fetch data through our front end or through
                          API.
                        </chakra.span>

                        <chakra.span fontWeight="semibold" pl={2}>
                          <Text fontWeight="bold" display="inline">
                            We analyze data
                          </Text>
                          - We find the most interesting information and
                          highlight it
                        </chakra.span>
                      </Stack>
                    </AccordionPanel>
                  </AccordionItem>
                </Accordion>
              </Stack>
              <Stack
                px={12}
                // mt={24}
                bgColor="gray.50"
                borderRadius="xl"
                boxShadow="xl"
                py={4}
              >
                <Accordion allowToggle>
                  <AccordionItem borderWidth={0}>
                    <h2>
                      <AccordionButton borderWidth={0}>
                        <Heading as="h4" size="md">
                          UI navigation basics
                        </Heading>
                        <AccordionIcon />
                      </AccordionButton>
                    </h2>
                    <AccordionPanel pb={4} borderWidth={0}>
                      <Stack dir="column">
                        <Text fontWeight="semibold" pl={2}>
                          Use the sidebar on the left for navigation:
                        </Text>
                        <chakra.span fontWeight="semibold" pl={2}>
                          <Text fontWeight="bold" display="inline">
                            Subscriptions
                          </Text>
                          Set up addresses you would like to monitor.{" "}
                          <i>
                            NB: Without any subscriptions, Moonstream will feel
                            quite empty!
                          </i>{" "}
                          No worries, we will help you set up your
                          subscriptions.
                          <i>
                            NB: Without setting up subscriptions moonstream will
                            have quite empty feel!{" "}
                          </i>{" "}
                          No worries, we will help you to set up your
                          subscriptions in the next steps!
                        </chakra.span>
                        <chakra.span fontWeight="semibold" pl={2}>
                          <Text fontWeight="bold" display="inline">
                            Stream
                          </Text>{" "}
                          This view is similar to a bank statement. You can
                          define a date range and see what happened with your
                          subscriptions during that time. You can also apply
                          filters to it.
                        </chakra.span>

                        <chakra.span fontWeight="semibold" pl={2}>
                          <Text fontWeight="bold" display="inline">
                            Stream Entry
                          </Text>{" "}
                          - See a detailed view of stream cards with specific
                          and essential data, like methods called in smart
                          contracts etc
                        </chakra.span>

                        <chakra.span fontWeight="semibold" pl={2}>
                          <Text fontWeight="bold" display="inline">
                            Analytics
                          </Text>{" "}
                          - This section is under construction. Soon you will be
                          able to create dashboards there. Right now you can
                          fill out a form to tell us what analytical tools you’d
                          want to see. We’d really appreciate that :)
                        </chakra.span>
                      </Stack>
                    </AccordionPanel>
                  </AccordionItem>
                </Accordion>
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
                  Tell us more about your needs
                </Heading>
                <Text fontWeight="semibold" pl={2}>
                  In order to create the best possible experience, we would love
                  to find out some more about you.
                </Text>
                <Text fontWeight="semibold" pl={2}>
                  Please tell us what profile describes you best.{" "}
                  <i>
                    This is purely analytical data, you can change it anytime
                    later.
                  </i>
                </Text>
                <RadioGroup
                  position="relative"
                  onChange={setProfile}
                  value={profile}
                  // fontWeight="bold"
                  colorScheme="secondary"
                  // py={0}
                  // my={0}
                >
                  <Stack
                    direction={["column", "row", null]}
                    justifyContent="space-evenly"
                  >
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
                  Subscriptions are an essential tool of Moonstream. We gather
                  data for you based on addresses you have subscribed to.
                  <br />
                  Subscribe to any address you are interested in and it will
                  become part of your stream.
                  <br />
                  Name of subscription (you can change it later).
                  <UnorderedList>
                    <ListItem>
                      Color - you can set colors to easily identify a
                      subscription in your stream
                    </ListItem>
                    <ListItem>Address - the address you subscribe to</ListItem>
                    <ListItem>
                      Label - we recommend using a human-readable name that
                      represents the subscription
                    </ListItem>
                    <ListItem>
                      Source - In Alpha we’re only supporting Ethereum
                      blockchain, but more sources are coming soon!
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
                  {`Stream is where you can read data you've subscribed to. There are different cards for different subscription types.`}
                  <br />
                  If the card has some extra details, there will be an orange
                  button on the right hand side inviting you to see more!
                  <br />
                  Below is a typical card for an Ethereum blockchain event.
                  Useful information right on the card:
                  <UnorderedList py={2}>
                    <ListItem>Hash - Unique ID of the event</ListItem>
                    <ListItem>
                      From - Sender address. If it is one of your subscription
                      addresses, it will appear in color with a label
                    </ListItem>
                    <ListItem>
                      To - Receiver address. If it is one of your subscription
                      addresses, it will appear in color with a label
                    </ListItem>
                    <ListItem>
                      Nonce - Counter how many transaction addresses have been
                      sent. It also determines the sequence of transactions!
                    </ListItem>
                    <ListItem>
                      Gas Price - This is how much ether is being paid per gas
                      unit
                    </ListItem>
                    <ListItem>Gas - Amount of gas this event consumes</ListItem>
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
                    subscription_type_id: "0",
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
                  You can apply various filters by clicking the filter menu
                  button.
                  <br />
                  {`Right now you can use it to select addresses from and to, and we are adding more complex queries soon — stay tuned!`}
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
            Go back
          </Button>
          <Spacer />
          <Button
            colorScheme={
              ui.onboardingStep < ui.onboardingSteps.length - 1
                ? `secondary`
                : `suggested`
            }
            variant={
              ui.onboardingStep < ui.onboardingSteps.length - 1
                ? `solid`
                : `outline`
            }
            rightIcon={
              ui.onboardingStep < ui.onboardingSteps.length - 1 && (
                <ArrowRightIcon />
              )
            }
            onClick={() => handleNextClick()}
          >
            {ui.onboardingStep < ui.onboardingSteps.length - 1
              ? `Next`
              : `Finish and move to stream`}
          </Button>
        </ButtonGroup>
      </Stack>
    </Scrollable>
  );
};
Welcome.getLayout = getLayout;
export default Welcome;
