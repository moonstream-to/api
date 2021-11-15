import React, { useContext } from "react";
import { Skeleton, IconButton, Container } from "@chakra-ui/react";
import {
  Table,
  Th,
  Td,
  Tr,
  Thead,
  Tbody,
  Tooltip,
  Editable,
  EditableInput,
  Image,
  EditablePreview,
  Button,
} from "@chakra-ui/react";
import { CheckIcon, DeleteIcon } from "@chakra-ui/icons";
import moment from "moment";
import CopyButton from "./CopyButton";
import { useSubscriptions } from "../core/hooks";
import ConfirmationRequest from "./ConfirmationRequest";
import ColorSelector from "./ColorSelector";
import OverlayContext from "../core/providers/OverlayProvider/context";
import { MODAL_TYPES } from "../core/providers/OverlayProvider/constants";

const mapper = {
  "tag:erc721": "NFTs",
  "input:address": "Address",
};

const SubscriptionsList = ({ emptyCTA }) => {
  const overlay = useContext(OverlayContext);
  const {
    subscriptionsCache,
    updateSubscription,
    deleteSubscription,
    subscriptionTypeIcons,
  } = useSubscriptions();

  const updateCallback = ({ id, label, color }) => {
    const data = { id: id };
    label && (data.label = label);
    color && (data.color = color);
    updateSubscription.mutate(data);
  };

  if (
    subscriptionsCache.data &&
    subscriptionsCache.data.subscriptions.length > 0
  ) {
    return (
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
            <Th>Token</Th>
            <Th>Label</Th>
            <Th>Address</Th>
            <Th>abi</Th>
            <Th>Color</Th>
            <Th>Date Created</Th>
            <Th>Actions</Th>
          </Tr>
        </Thead>
        <Tbody>
          {subscriptionsCache.data.subscriptions.map((subscription) => {
            const iconLink =
              subscriptionTypeIcons[subscription.subscription_type_id];
            return (
              <Tr key={`token-row-${subscription.id}`}>
                <Td>
                  <Tooltip label="Ethereum blockchain" fontSize="md">
                    <Image h="32px" src={iconLink} alt="pool icon" />
                  </Tooltip>
                </Td>
                <Td py={0}>
                  <Editable
                    colorScheme="blue"
                    placeholder="enter note here"
                    defaultValue={subscription.label}
                    onSubmit={(nextValue) =>
                      updateCallback({
                        id: subscription.id,
                        label: nextValue,
                      })
                    }
                  >
                    <EditablePreview
                      maxW="40rem"
                      _placeholder={{ color: "black" }}
                    />
                    <EditableInput maxW="40rem" />
                  </Editable>
                </Td>
                <Td mr={4} p={0}>
                  {subscription.address?.startsWith("tag") ? (
                    <CopyButton>{mapper[subscription.address]}</CopyButton>
                  ) : (
                    <CopyButton>{subscription.address}</CopyButton>
                  )}
                </Td>
                <Td mr={4} p={0}>
                  {subscription.abi ? (
                    <CheckIcon />
                  ) : (
                    <Button
                      colorScheme="orange"
                      size="xs"
                      py={2}
                      disabled={!subscription.address}
                      onClick={() =>
                        overlay.toggleModal({
                          type: MODAL_TYPES.UPLOAD_ABI,
                          props: { id: subscription.id },
                        })
                      }
                    >
                      Upload
                    </Button>
                  )}
                </Td>
                <Td>
                  <ColorSelector
                    // subscriptionId={subscription.id}
                    initialColor={subscription.color}
                    callback={(color) =>
                      updateCallback({ id: subscription.id, color: color })
                    }
                  />
                </Td>
                <Td py={0}>{moment(subscription.created_at).format("L")}</Td>

                <Td py={0}>
                  <ConfirmationRequest
                    bodyMessage={"please confirm"}
                    header={"Delete subscription"}
                    onConfirm={() => deleteSubscription.mutate(subscription.id)}
                  >
                    <IconButton
                      size="sm"
                      variant="ghost"
                      colorScheme="blue"
                      icon={<DeleteIcon />}
                    />
                  </ConfirmationRequest>
                </Td>
              </Tr>
            );
          })}
        </Tbody>
      </Table>
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
