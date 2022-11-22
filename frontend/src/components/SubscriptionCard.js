import React, { useContext } from "react";
import { IconButton } from "@chakra-ui/react";
import {
  Td,
  Tr,
  Tooltip,
  Editable,
  EditableInput,
  EditablePreview,
  Image,
  Button,
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  AccordionIcon,
  Flex,
  Text,
  Spacer,
  Stack,
} from "@chakra-ui/react";
import { CheckIcon, DeleteIcon, EditIcon } from "@chakra-ui/icons";
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

const SubscriptionCard = ({ subscription, isDesktopView, iconLink }) => {
  const overlay = useContext(OverlayContext);
  const { updateSubscription, deleteSubscription, subscriptionTypeNames } =
    useSubscriptions();
  const [_isLoading, _setIsLoading] = React.useState(
    updateSubscription.isLoading
  );

  const updateCallback = ({ id, label, color }) => {
    const data = { id: id };
    label && (data.label = label);
    color && (data.color = color);
    updateSubscription.mutate(data);
  };

  const cellProps = {
    px: ["16px", "8px", "16px"],
  };

  React.useEffect(() => {
    console.log("update subscription ue");
    if (updateSubscription.isLoading) _setIsLoading(true);
    else _setIsLoading(false);
  }, [updateSubscription.isLoading]);

  return (
    <>
      {!isDesktopView && (
        <AccordionItem
          borderBottomColor="blue.500"
          key={`token-row-${subscription.id}`}
        >
          <h2>
            <AccordionButton>
              <Stack
                direction="row"
                textAlign="center"
                alignItems="center"
                w="100%"
              >
                <Tooltip
                  label={`${
                    subscriptionTypeNames[subscription.subscription_type_id]
                  }`}
                  fontSize="md"
                >
                  <Image
                    h={["32px", "16px", "32px", null]}
                    src={iconLink}
                    alt="pool icon"
                  />
                </Tooltip>
                <Text>{subscription.label}</Text>

                {/* <Input
                  w="100%"
                  colorScheme="blue"
                  placeholder="enter note here"
                  //   isDisabled={!isEditing}
                  isReadOnly={isEditing}
                  // isPreviewFocusable={false}
                  defaultValue={subscription.label}
                  onSubmit={handleSubmit}
                  value={inputState}
                  onChange={(e) => {
                    setInputState(e.target.value);
                  }}
                  // onClick={() => { setIsEditing(true) }}
                  ref={inputRef}
                  variant="outline"
                ></Input> */}
              </Stack>
              <AccordionIcon />
            </AccordionButton>
          </h2>
          <AccordionPanel pb={4} boxShadow="md">
            <Stack>
              <Stack fontSize="sm" h="min-content" pr={0}>
                <Text placeSelf="flex-start">Address:</Text>
                {/* <Spacer /> */}

                {subscription.address?.startsWith("tag") ? (
                  <CopyButton size="xs" copyString={subscription.address}>
                    {mapper[subscription.address]}
                  </CopyButton>
                ) : (
                  <Flex
                    alignItems="center"
                    size="xs"
                    position="relative"
                    maxWidth="200px"
                    // w="100%"
                    flexGrow={1}
                  >
                    <CopyButton copyString={subscription.address}></CopyButton>
                    <Text
                      isTruncated
                      dataFileType={subscription.address.slice(-3)}
                      whiteSpace="nowrap"
                      textOverflow="ellipsis"
                      overflow="hidden"
                      _after={{
                        content: "attr(datafiletype)",
                        position: "absolute",
                        top: 0,
                        left: "100%",
                        pt: "9px",
                        marginLeft: "-2px",
                      }}
                    >
                      {subscription.address}
                    </Text>
                  </Flex>
                )}
              </Stack>
              <Flex
                fontSize="sm"
                placeContent="center"
                h="min-content"
                alignItems="center"
                pr={0}
              >
                <Text>Abi:</Text>
                <Spacer />
                {subscription.abi ? (
                  <CheckIcon />
                ) : (
                  // <Button
                  //   colorScheme="orange"
                  //   size="xs"
                  //   py={2}
                  //   disabled={!subscription.address}
                  //   onClick={() =>
                  //     overlay.toggleModal({
                  //       type: MODAL_TYPES.UPLOAD_ABI,
                  //       props: { id: subscription.id },
                  //     })
                  //   }
                  // >
                  //   Upload
                  // </Button>
                  <Text>Not Available</Text>
                )}
              </Flex>
              <Flex fontSize="sm" placeContent="center" h="min-content" pr={0}>
                <Spacer />

                <Flex
                  alignItems="center"
                  direction="column"
                  spacing={0}
                  w="100%"
                >
                  {/* {isEditing && (
                    <ButtonGroup justifyContent="center" size="sm">
                      <IconButton icon={<CheckIcon />} onClick={handleSubmit} />
                      <IconButton
                        icon={<CloseIcon />}
                        onClick={() => setIsEditing(false)}
                      />
                    </ButtonGroup>
                  )} */}
                  <Button
                    m={0}
                    borderRadius={0}
                    borderTopRadius="md"
                    w="100%"
                    colorScheme="blue"
                    size="xs"
                    py={2}
                    disabled={!subscription.address}
                    onClick={() => {
                      console.log("rename button clicked");
                      overlay.toggleModal({
                        type: MODAL_TYPES.MOBILE_INPUT_FIELD,
                        props: {
                          title: "New name",
                          initialValue: subscription.label,
                          cancelText: "Cancel",
                          submitText: "Rename",
                          id: subscription.id,
                        },
                        _key: `rename-subscription-${subscription.id}-${_isLoading}`,
                      });
                      //   setIsEditing(true);
                    }}
                    leftIcon={<EditIcon />}
                  >
                    Rename
                  </Button>
                  <Button
                    m={0}
                    borderRadius={0}
                    w="100%"
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
                    leftIcon={<DeleteIcon />}
                  >
                    Upload Abi
                  </Button>
                  <ConfirmationRequest
                    bodyMessage={"please confirm"}
                    header={"Delete subscription"}
                    onConfirm={() => deleteSubscription.mutate(subscription.id)}
                  >
                    <Button
                      m={0}
                      borderRadius={0}
                      borderBottomRadius="md"
                      w="100%"
                      colorScheme="red"
                      size="xs"
                      py={2}
                      disabled={!subscription.address}
                      leftIcon={<DeleteIcon />}
                    >
                      Delete
                    </Button>
                  </ConfirmationRequest>
                </Flex>
              </Flex>
            </Stack>
          </AccordionPanel>
        </AccordionItem>
      )}
      {isDesktopView && (
        <Tr key={`token-row-${subscription.id}`}>
          <Td {...cellProps}>
            <Tooltip
              label={`${
                subscriptionTypeNames[subscription.subscription_type_id]
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
              <EditablePreview maxW="40rem" _placeholder={{ color: "black" }} />
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
      )}
    </>
  );
};

export default SubscriptionCard;
