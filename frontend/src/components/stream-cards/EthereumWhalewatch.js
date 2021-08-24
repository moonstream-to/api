import React, { useContext, useEffect, useState } from "react";
import {
  Text,
  Stack,
  Tooltip,
  useClipboard,
  Heading,
  Image,
  useMediaQuery,
  Spacer,
  Spinner,
  chakra,
} from "@chakra-ui/react";
import UIContext from "../../core/providers/UIProvider/context";
import { useToast } from "../../core/hooks";
import { useSubscriptions } from "../../core/hooks";

const EthereumWhalewatchCard_ = ({
  entry,
  showOnboardingTooltips,
  className,
}) => {
  const { subscriptionsCache, subscriptionTypeIcons } = useSubscriptions();
  const ui = useContext(UIContext);
  const [copyString, setCopyString] = useState(false);
  const [icon, setIcon] = useState(null);
  const { onCopy, hasCopied } = useClipboard(copyString, 1);
  const toast = useToast();

  useEffect(() => {
    if (hasCopied && copyString) {
      toast("Copied to clipboard", "success");
      setCopyString(false);
    } else if (copyString) {
      onCopy();
    }
  }, [copyString, onCopy, hasCopied, toast]);

  useEffect(() => {
    if (subscriptionTypeIcons) {
      setIcon(subscriptionTypeIcons.ethereum_whalewatch);
    }
  }, [subscriptionTypeIcons, setIcon]);

  const [showFullView] = useMediaQuery(["(min-width: 420px)"]);
  if (subscriptionsCache.isLoading) return <Spinner />;

  const whales = {
    transactionsOut: entry?.event_data?.transactions_out[0] || {},
    transactionsIn: entry?.event_data?.transactions_in[0] || {},
    valueOut: entry?.event_data?.value_out[0] || {},
    valueIn: entry?.event_data?.value_in[0] || {},
  };

  Object.values(whales).forEach((whaleInfo) => {
    whaleInfo.color =
      subscriptionsCache.data.subscriptions.find((obj) => {
        return obj.address === whaleInfo.address;
      })?.color ?? "gray.500";
    whaleInfo.label =
      subscriptionsCache.data.subscriptions.find((obj) => {
        return obj.address === whaleInfo.address;
      })?.label ?? whaleInfo.address;
  });

  const rowLabels = {
    transactionsOut: "Number of transactions sent",
    transactionsIn: "Number of transactions received",
    valueOut: "WEI sent",
    valueIn: "WEI received",
  };

  return (
    <Stack className={className}>
      <Tooltip
        hasArrow
        isOpen={showOnboardingTooltips}
        label="This is an Ethereum whale watch event. It shows top movers on the Ethereum blockchain in the given time period."
        variant="onboarding"
        placement="top"
      >
        <Stack
          className="title"
          direction="row"
          w="100%"
          h="1.6rem"
          minH="1.6rem"
          textAlign="center"
          spacing={0}
          alignItems="center"
          bgColor="gray.300"
        >
          {icon ? <Image boxSize="16px" src={icon} /> : ""}
          <Heading px={1} size="xs">
            Ethereum whale watch
          </Heading>
          <Spacer />
          <Text isTruncated pr={12}>
            {`${entry.event_data.date_range.start_time} to ${entry.event_data.date_range.end_time}`}
          </Text>
        </Stack>
      </Tooltip>
      {Object.keys(whales).map((whaleType) => {
        return (
          <Stack
            className={whaleType}
            direction={showFullView ? "row" : "column"}
            w="100%"
            h={showFullView ? "1.6rem" : "3.2rem"}
            minH="1.6rem"
            spacing={0}
            alignItems="center"
            key={`${whaleType}-${entry.event_data.date_range.start_time}-${entry.event_data.date_range.end_time}`}
          >
            <Stack
              overflow="hidden"
              textOverflow="ellipsis"
              whiteSpace="nowrap"
              direction="row"
              fontSize="sm"
              fontWeight="600"
              w={showFullView ? "calc(30%)" : "calc(100%)"}
              h="100%"
              borderColor="gray.1200"
              borderRightWidth={showFullView ? "1px" : "0px"}
              placeContent="center"
              spacing={0}
            >
              <Tooltip
                hasArrow
                isOpen={showOnboardingTooltips && !ui.isMobileView}
                label={`This row represents the following statistic: ${rowLabels[whaleType]}`}
                aria-label={`This row represents the following statistic: ${rowLabels[whaleType]}`}
                variant="onboarding"
                placement={ui.isMobileView ? "bottom" : "left"}
                maxW="150px"
              >
                <Text
                  h="100%"
                  fontSize="sm"
                  py="2px"
                  px={2}
                  w={showFullView ? null : "120px"}
                >
                  {rowLabels[whaleType]}
                </Text>
              </Tooltip>
            </Stack>
            <Stack
              overflow="hidden"
              textOverflow="ellipsis"
              whiteSpace="nowrap"
              direction="row"
              fontSize="sm"
              fontWeight="600"
              minw="min-content"
              w={showFullView ? "calc(70%)" : "calc(100%)"}
              h="100%"
              spacing={0}
              textAlign="left"
            >
              <Text
                mx={0}
                py="2px"
                fontSize="sm"
                bgColor={whales[whaleType].color}
                isTruncated
                w="calc(100%)"
                h="100%"
                onClick={() => setCopyString(whales[whaleType].address)}
              >
                {whales[whaleType].label} -- {whales[whaleType].statistic}
              </Text>
            </Stack>
          </Stack>
        );
      })}
    </Stack>
  );
};

const EthereumWhalewatchCard = chakra(EthereumWhalewatchCard_, {
  baseStyle: {
    my: 0,
    direction: "column",
    flexBasis: "10px",
    flexGrow: 1,
    borderWidth: "2px",
    borderLeftRadius: "md",
    borderColor: "gray.600",
    spacing: 0,
    h: "auto",
    overflowX: "hidden",
    overflowY: "visible",
  },
});

export default EthereumWhalewatchCard;
