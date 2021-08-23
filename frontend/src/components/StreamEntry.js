import React, { useContext } from "react";
import { Flex, IconButton, Stack, Tooltip, chakra } from "@chakra-ui/react";
import { ArrowRightIcon } from "@chakra-ui/icons";
import UIContext from "../core/providers/UIProvider/context";
import EthereumMempoolCard from "./stream-cards/EthereumMempool";

const StreamEntry_ = ({ entry, showOnboardingTooltips, className }) => {
  const ui = useContext(UIContext);

  return (
    <Flex
      className={className}
      p={0}
      m={1}
      mr={2}
      borderRadius="md"
      borderTop="1px"
      bgColor="gray.100"
      borderColor="white.300"
      transition="0.1s"
      flexBasis="50px"
      direction="row"
      justifySelf="center"
      justifyContent="normal"
      alignItems="baseline"
      boxShadow="lg"
      minH="fit-content"
    >
      <Stack
        direction="row"
        flexBasis="100px"
        flexGrow={1}
        minW="100px"
        h="100%"
        spacing={0}
      >
        {entry.subscription_type_id === "0" && (
          <EthereumMempoolCard entry={entry} />
        )}

        {/* ToDo: Add another types of cards in here

        {entryType === "<name>" && (
          <Card entry={entry} />
        )}

        */}
        <Flex>
          <Tooltip
            hasArrow
            isOpen={showOnboardingTooltips}
            placement={ui.isMobileView ? "bottom" : "right"}
            label="Clicking side arrow will bring up detailed view"
            variant="onboarding"
            maxW="150px"
          >
            <IconButton
              m={0}
              onClick={() => ui.setCurrentTransaction(entry)}
              h="full"
              borderLeftRadius={0}
              variant="solid"
              px={0}
              minW="24px"
              colorScheme="secondary"
              icon={<ArrowRightIcon w="24px" />}
            />
          </Tooltip>
        </Flex>
      </Stack>
    </Flex>
  );
};

const StreamEntry = chakra(StreamEntry_);

export default StreamEntry;
