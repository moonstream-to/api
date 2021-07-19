import React from "react";
import { Skeleton, IconButton } from "@chakra-ui/react";
import {
  Table,
  Th,
  Td,
  Tr,
  Thead,
  Tbody,
  Editable,
  EditableInput,
  Image,
  EditablePreview,
} from "@chakra-ui/react";
import { DeleteIcon } from "@chakra-ui/icons";
import moment from "moment";
import CopyButton from "./CopyButton";
import { useSubscriptions } from "../core/hooks";
import ConfirmationRequest from "./ConfirmationRequest";

const List = () => {
  const { subscriptionsCache, changeNote, deleteSubscription } =
    useSubscriptions();

  const updateCallback = ({ id, note }) => {
    changeNote.mutate({ id, note });
  };

  if (subscriptionsCache.data) {
    return (
      <Table
        borderColor="gray.200"
        borderWidth="1px"
        variant="simple"
        colorScheme="primary"
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
            <Th>Address</Th>
            <Th>Date Created</Th>
            <Th>Note</Th>
            <Th>Actions</Th>
          </Tr>
        </Thead>
        <Tbody>
          {subscriptionsCache.data.subscriptions.map((subscription) => {
            return (
              <Tr key={`token-row-${subscription.address}`}>
                <Td>
                  <Image
                    h="32px"
                    src="https://ethereum.org/static/c48a5f760c34dfadcf05a208dab137cc/31987/eth-diamond-rainbow.png"
                  />
                </Td>
                <Td mr={4} p={0}>
                  <CopyButton>{subscription.address}</CopyButton>
                </Td>
                <Td py={0}>{moment(subscription.created_at).format("L")}</Td>
                <Td py={0}>
                  <Editable
                    colorScheme="primary"
                    placeholder="enter note here"
                    defaultValue={subscription.note}
                    onSubmit={(nextValue) =>
                      updateCallback({
                        id: subscription.id,
                        note: nextValue,
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
                <Td py={0}>
                  <ConfirmationRequest
                    bodyMessage={"please confirm"}
                    header={"Delete subscription"}
                    onConfirm={() => deleteSubscription.mutate(subscription.id)}
                  >
                    <IconButton
                      size="sm"
                      variant="ghost"
                      colorScheme="primary"
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
  } else if (subscriptionsCache.isLoading) {
    return <Skeleton />;
  } else {
    return "";
  }
};
export default List;
