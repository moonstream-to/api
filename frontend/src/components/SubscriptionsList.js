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
  EditablePreview,
  Image,
  Button,
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
  Stack,
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
  const [isLargerThan530px] = useMediaQuery(["(min-width: 530px)"]);
  const overlay = useContext(OverlayContext);
  const {
    subscriptionsCache,
    updateSubscription,
    deleteSubscription,
    subscriptionTypeIcons,
    subscriptionTypeNames,
  } = useSubscriptions();

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
                  <Tr key={`token-row-${subscription.id}`}>
                    <Td {...cellProps}>
                      <Tooltip
                        label={`${
                          subscriptionTypeNames[
                            subscription.subscription_type_id
                          ]
                        }`}
                        fontSize="md"
                      >
                        <Image
                          h={["32px", "16px", "32px", null]}
                          src={iconLink}
                          alt="pool icon"
                        />
                      </Tooltip>
                    </Td>
                    <Td py={0} {...cellProps} wordBreak="break-word">
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
                    <Td mr={4} p={0} wordBreak="break-word" {...cellProps}>
                      {subscription.address?.startsWith("tag") ? (
                        <CopyButton>{mapper[subscription.address]}</CopyButton>
                      ) : (
                        <CopyButton>{subscription.address}</CopyButton>
                      )}
                    </Td>
                    <Td mr={4} p={0} {...cellProps}>
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
                    <Td {...cellProps}>
                      <ColorSelector
                        // subscriptionId={subscription.id}
                        initialColor={subscription.color}
                        callback={(color) =>
                          updateCallback({ id: subscription.id, color: color })
                        }
                      />
                    </Td>
                    <Td py={0} {...cellProps} wordBreak="break-word">
                      {moment(subscription.created_at).format("L")}
                    </Td>

                    <Td py={0} {...cellProps}>
                      <ConfirmationRequest
                        bodyMessage={"please confirm"}
                        header={"Delete subscription"}
                        onConfirm={() =>
                          deleteSubscription.mutate(subscription.id)
                        }
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
        )}
        {!isLargerThan530px && (
          <Accordion>
            {subscriptionsCache.data.subscriptions.map((subscription) => {
              const iconLink =
                subscriptionTypeIcons[subscription.subscription_type_id];
              return (
                <AccordionItem key={`token-row-${subscription.id}`}>
                  <h2>
                    <AccordionButton>
                      <Stack
                        direction="row"
                        textAlign="left"
                        alignItems="center"
                      >
                        <Tooltip
                          label={`${
                            subscriptionTypeNames[
                              subscription.subscription_type_id
                            ]
                          }`}
                          fontSize="md"
                        >
                          <Image
                            h={["32px", "16px", "32px", null]}
                            src={iconLink}
                            alt="pool icon"
                          />
                        </Tooltip>
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
                      </Stack>
                      <AccordionIcon />
                    </AccordionButton>
                  </h2>
                  <AccordionPanel pb={4}>
                    <Stack>
                      <Flex
                        fontSize="sm"
                        placeContent="center"
                        h="min-content"
                        alignItems="center"
                        pr={8}
                      >
                        <Text>Address:</Text>
                        <Spacer />
                        {subscription.address?.startsWith("tag") ? (
                          <CopyButton
                            size="xs"
                            copyString={subscription.address}
                          >
                            {mapper[subscription.address]}
                          </CopyButton>
                        ) : (
                          <CopyButton
                            size="xs"
                            copyString={subscription.address}
                          >
                            <Text isTruncated>{subscription.address}</Text>
                          </CopyButton>
                        )}
                      </Flex>
                      <Flex
                        fontSize="sm"
                        placeContent="center"
                        h="min-content"
                        alignItems="center"
                        pr={8}
                      >
                        <Text>Abi:</Text>
                        <Spacer />
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
                      </Flex>
                      <Flex
                        fontSize="sm"
                        placeContent="center"
                        h="min-content"
                        pr={8}
                      >
                        <Spacer />
                        <ConfirmationRequest
                          bodyMessage={"please confirm"}
                          header={"Delete subscription"}
                          onConfirm={() =>
                            deleteSubscription.mutate(subscription.id)
                          }
                        >
                          <Button
                            colorScheme="red"
                            size="xs"
                            py={2}
                            disabled={!subscription.address}
                            onClick={() =>
                              overlay.toggleModal({
                                type: MODAL_TYPES.UPLOAD_ABI,
                                props: { id: subscription.id },
                              })
                            }
                            leftIcon={<DeleteIcon />}
                          >
                            Delete
                          </Button>
                        </ConfirmationRequest>
                      </Flex>
                    </Stack>
                  </AccordionPanel>
                </AccordionItem>
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
