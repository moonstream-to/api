import React, { useContext, useState } from "react";
import { Skeleton, IconButton, Container } from "@chakra-ui/react";
import {
  Table,
  Th,
  Td,
  Tr,
  Thead,
  Tbody,
  Tooltip,
  Input,
  Editable,
  EditableInput,
  EditablePreview,
  useEditableControls,
  Image,
  Button,
  ButtonGroup,
  useMediaQuery,
  Accordion,
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  AccordionIcon,
  Box,
  Flex,
  Text,
  Spacer,
  Stack
} from "@chakra-ui/react";
import { CheckIcon, CloseIcon, DeleteIcon, EditIcon } from "@chakra-ui/icons";
import moment from "moment";
import CopyButton from "./CopyButton";
import { useSubscriptions } from "../core/hooks";
import ConfirmationRequest from "./ConfirmationRequest";
import ColorSelector from "./ColorSelector";
import OverlayContext from "../core/providers/OverlayProvider/context";
import { MODAL_TYPES } from "../core/providers/OverlayProvider/constants";
import SubscriptionCard from "./SubscriptionCard";

const mapper = {
  "tag:erc721": "NFTs",
  "input:address": "Address",
};

const EditableControls = () => {
  const {
    isEditing,
    getSubmitButtonProps,
    getCancelButtonProps,
    getEditButtonProps,
  } = useEditableControls()

  return isEditing ? (
    <ButtonGroup justifyContent='center' size='sm'>
      <IconButton icon={<CheckIcon />} {...getSubmitButtonProps()} />
      <IconButton icon={<CloseIcon />} {...getCancelButtonProps()} />
    </ButtonGroup>
  ) : (
    <Flex justifyContent='center'>
      <IconButton size='sm' icon={<EditIcon />} {...getEditButtonProps()} />
    </Flex>
  )
}

// const truncateText = function(text) {
//   if(text.length > 7) {
//     return text.substring()
//   }
// }

const SubscriptionsList = ({ emptyCTA }) => {
  const [isLargerThan530px] = useMediaQuery(["(min-width: 530px)"]);
  const overlay = useContext(OverlayContext);
  const {
    subscriptionsCache,
    updateSubscription,
    deleteSubscription,
    subscriptionTypeIcons,
    subscriptionTypeNames,
  } = useSubscriptions();

  const [inputState, setInputState] = useState()

  const updateCallback = ({ id, label, color }) => {
    const data = { id: id };
    label && (data.label = label);
    color && (data.color = color);
    updateSubscription.mutate(data);
  };

  const cellProps = {
    px: ["16px", "8px", "16px"],
  };

  if (
    subscriptionsCache.data &&
    subscriptionsCache.data.subscriptions.length > 0
  ) {
    return (
      <>
        {isLargerThan530px && (
          <Table
            borderColor="gray.200"
            borderWidth="1px"
            variant="simple"
            colorScheme="blue"
            justifyContent="center"
            borderBottomRadius="xl"
            alignItems="baseline"
            h="auto"
            size="sm"
            mt={0}
          >
            <Thead>
              <Tr>
                <Th {...cellProps}>Token</Th>
                <Th {...cellProps}>Label</Th>
                <Th {...cellProps}>Address</Th>
                <Th {...cellProps}>abi</Th>
                <Th {...cellProps}>Color</Th>
                <Th {...cellProps}>Date Created</Th>
                <Th {...cellProps}>Actions</Th>
              </Tr>
            </Thead>

            <Tbody>
              {subscriptionsCache.data.subscriptions.map((subscription) => {
                const iconLink =
                  subscriptionTypeIcons[subscription.subscription_type_id];
                return (
                  <SubscriptionCard key={`token-row-${subscription.id}`} subscription={subscription} isDesktopView={isLargerThan530px} iconLink={iconLink} />
                );
              })}
            </Tbody>
          </Table>
        )}
        {!isLargerThan530px && (
          <Accordion
            allowToggle={true}>
            {subscriptionsCache.data.subscriptions.map((subscription) => {
              const iconLink =
                subscriptionTypeIcons[subscription.subscription_type_id];
              return (
                <SubscriptionCard key={`token-row-${subscription.id}`} subscription={subscription} isDesktopView={isLargerThan530px} iconLink={iconLink} />
              );
            })}

            <AccordionItem>
              <h2>
                <AccordionButton>
                  <Box flex="1" textAlign="left">
                    Section 2 title
                  </Box>
                  <AccordionIcon />
                </AccordionButton>
              </h2>
              <AccordionPanel pb={4}>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
                eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut
                enim ad minim veniam, quis nostrud exercitation ullamco laboris
                nisi ut aliquip ex ea commodo consequat.
              </AccordionPanel>
            </AccordionItem>
          </Accordion>
        )}
      </>
    );
  } else if (
    subscriptionsCache.data &&
    subscriptionsCache.data.subscriptions.length === 0
  ) {
    return (
      <Container>
        {` You don't have any subscriptions at the moment.`}
        {emptyCTA && <Button variant="green">Create one</Button>}
      </Container>
    );
  } else if (subscriptionsCache.isLoading) {
    return <Skeleton />;
  } else {
    return "";
  }
};
export default SubscriptionsList;
