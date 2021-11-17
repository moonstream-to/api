import React, { useEffect, useRef } from "react";
import { getLayout } from "../src/layouts/AppLayout";
import {
  Heading,
  Text,
  Stack,
  Fade,
  chakra,
  Accordion,
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  AccordionIcon,
  Link,
} from "@chakra-ui/react";
import Scrollable from "../src/components/Scrollable";
import RouterLink from "next/link";

const Welcome = () => {
  useEffect(() => {
    if (typeof window !== "undefined") {
      document.title = `Welcome to moonstream.to!`;
    }
  }, []);

  const scrollRef = useRef();

  return (
    <Scrollable>
      <Stack px="7%" pt={4} w="100%" spacing={4} ref={scrollRef}>
        {/* <StepProgress
          numSteps={ui.onboardingSteps.length}
          currentStep={ui.onboardingStep}
          colorScheme="blue"
          buttonCallback={progressButtonCallback}
          buttonTitles={[
            "Moonstream basics",
            "Setup subscriptions",
            "How to read stream",
          ]}
          style="arrows"
        /> */}

        {true && (
          <Fade in>
            <Stack spacing={4} pb={14}>
              <Stack
                px={[0, 12, null]}
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
                  We are very excited welcome you on board!
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
                px={[0, 12, null]}
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
                  <AccordionItem borderWidth={0}>
                    <h2>
                      <AccordionButton borderWidth={0}>
                        <Heading as="h4" size="md">
                          How do I build my smart contract dashboard?
                        </Heading>
                        <AccordionIcon />
                      </AccordionButton>
                    </h2>
                    <AccordionPanel pb={4} borderWidth={0}>
                      <Stack direction="column">
                        <chakra.span fontWeight="semibold" pl={2}>
                          <Text fontWeight="bold" display="inline">
                            1. Subscribe
                          </Text>{" "}
                          - First step is to tell us what addresses you want
                          moonstream to track activity at. You can do this at{" "}
                          <RouterLink passHref href="/subscriptions">
                            <Link color="orange.500">subscriptions page</Link>
                          </RouterLink>{" "}
                          or simply by just clicking + on navigation bar of this
                          page.
                        </chakra.span>
                        <chakra.span fontWeight="semibold" pl={2}>
                          <Text fontWeight="bold" display="inline">
                            2. Provide ABI to subscription
                          </Text>{" "}
                          - In order for us to know what data to track, you need
                          to provide an ABI to subscription. You can upload one
                          at{" "}
                          <RouterLink passHref href="/subscriptions">
                            <Link color="orange.500">subscriptions page</Link>
                          </RouterLink>
                          . If you are not sure what is abi ABI or which is
                          correct for you - ask us on{" "}
                          <Link
                            color="orange.500"
                            isExternal
                            href={"https://discord.gg/K56VNUQGvA"}
                          >
                            Discord
                          </Link>{" "}
                          . <br />
                          <i>
                            N.B: Right now we have automatic dashboards only
                            availible. This means that dashboard will contain
                            analytics for ALL interfaces listed in ABI that was
                            provided. I you need only fraction of it - leave
                            these interfaces of interest in ABI when uploading
                            and remove rest.
                          </i>
                        </chakra.span>

                        <chakra.span fontWeight="semibold" pl={2}>
                          <Text fontWeight="bold" display="inline">
                            3. Create your dashboard
                          </Text>{" "}
                          - Press {`"New dashboard"`} on sidebar, or from + on
                          navbar menu. Fill in name, select subscriptons you
                          like to track to and checkbox what are you interested
                          in. If there is no ABI - tracking contract specific
                          elements {`won't`} be availible.
                        </chakra.span>

                        <chakra.span fontWeight="semibold" pl={2}>
                          <Text fontWeight="bold" display="inline">
                            4. Get some coffee -
                          </Text>{" "}
                          Your dashboard will appear on sidebar right away after
                          succesfull creation. However, populating initially
                          with data will take some time. Crawlers usually run in
                          5 minutes cycle, they will start from newest block and
                          will move down till genesis block. While you can make
                          your favorite drink of choice and get back to see the
                          dashboard!
                        </chakra.span>
                      </Stack>
                    </AccordionPanel>
                  </AccordionItem>
                </Accordion>
              </Stack>
            </Stack>
          </Fade>
        )}

        {/* <ButtonGroup>
          <Button
            colorScheme="orange"
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
                ? `orange`
                : `green`
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
        </ButtonGroup> */}
      </Stack>
    </Scrollable>
  );
};
Welcome.getLayout = getLayout;
export default Welcome;
