import React, { useContext, useEffect, useState } from "react";
import { Skeleton, IconButton, Container, useEditable, useOutsideClick } from "@chakra-ui/react";
import {
    Td,
    Tr,
    Tooltip,
    Editable,
    Input,
    EditableInput,
    EditablePreview,
    useEditableControls,
    Image,
    Button,
    ButtonGroup,
    useMediaQuery,
    AccordionItem,
    AccordionButton,
    AccordionPanel,
    AccordionIcon,
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
import EditableControls from "./EditableControls";
import { BiHandicap } from "react-icons/bi";

const mapper = {
    "tag:erc721": "NFTs",
    "input:address": "Address",
};


const SubscriptionCard = ({ subscription, isDesktopView, iconLink }) => {
    const overlay = useContext(OverlayContext);
    const {
        updateSubscription,
        deleteSubscription,
        subscriptionTypeNames,
    } = useSubscriptions();

    const [inputState, setInputState] = useState()
    const [isEditing, setIsEditing] = useState(false)
    const inputRef = React.useRef()
    useEffect(() => {
        if (isEditing && inputRef.current) {
            inputRef.current.focus()
        }
    }, [isEditing, inputRef.current])

    useOutsideClick({ ref: inputRef, handler: () => { setIsEditing(false) } })

    const updateCallback = ({ id, label, color }) => {
        const data = { id: id };
        label && (data.label = label);
        color && (data.color = color);
        updateSubscription.mutate(data);
    };

    const handleSubmit = () => {
        updateCallback({
            id: subscription.id,
            label: inputState,
        })
    }

    const cellProps = {
        px: ["16px", "8px", "16px"],
    };

    console.log(isEditing);
    return (
        <>
            {!isDesktopView && (
                <AccordionItem
                    bgColor="blue.50"
                    borderBottomColor="blue.500"
                    key={`token-row-${subscription.id}`}>
                    <h2>
                        <AccordionButton>
                            <Stack
                                direction="row"
                                textAlign="center"
                                alignItems="center"
                                w="100%"
                            >
                                <Tooltip
                                    label={`${subscriptionTypeNames[
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

                                <Input
                                    w="100%"
                                    colorScheme="blue"
                                    placeholder="enter note here"
                                    // isPreviewFocusable={false}
                                    defaultValue={subscription.label}
                                    onSubmit={handleSubmit}
                                    value={inputState}
                                    onChange={(e) => { setInputState(e.target.value) }}
                                    // onClick={() => { setIsEditing(true) }}
                                    ref={inputRef}
                                    variant="flushed"
                                >

                                </Input>
                            </Stack>
                            <AccordionIcon />
                        </AccordionButton>
                    </h2>
                    <AccordionPanel
                        pb={4}
                        bgColor="blue.100"
                        boxShadow="md">
                        <Stack>
                            <Flex
                                fontSize="sm"
                                h="min-content"
                                pr={0}
                            >
                                <Text
                                    placeSelf="flex-start">Address:</Text>
                                {/* <Spacer /> */}

                                {subscription.address?.startsWith("tag") ? (
                                    <CopyButton
                                        size="xs"
                                        copyString={subscription.address}
                                    >
                                        {mapper[subscription.address]}
                                    </CopyButton>
                                ) : (
                                    <Flex
                                        size="xs"
                                        copyString={subscription.address}
                                        position="relative"
                                        maxWidth="200px"
                                        // w="100%"
                                        flexGrow={1}
                                    >
                                        <Text

                                            isTruncated
                                            dataFileType={subscription.address.slice(-3)}
                                            whiteSpace="nowrap"
                                            textOverflow="ellipsis"
                                            overflow="hidden"
                                            _after={{ content: "attr(datafiletype)", position: "absolute", top: 0, left: "100%" }}>{subscription.address}
                                        </Text>
                                    </Flex>
                                )}
                            </Flex>
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
                                    <Text>
                                        Not Available
                                    </Text>
                                )}
                            </Flex>
                            <Flex
                                fontSize="sm"
                                placeContent="center"
                                h="min-content"
                                pr={0}
                            >
                                <Spacer />

                                <Flex
                                    alignItems="center"
                                    direction="column"
                                    spacing={0}
                                    w="100%">
                                    {isEditing &&
                                        <ButtonGroup justifyContent='center' size='sm'>
                                            <IconButton icon={<CheckIcon />} onClick={handleSubmit} />
                                            <IconButton icon={<CloseIcon />} onClick={() => setIsEditing(false)} />
                                        </ButtonGroup>}
                                    <Button
                                        m={0}
                                        borderRadius={0}
                                        borderTopRadius="md"
                                        w="100%"
                                        colorScheme="blue"
                                        size="xs"
                                        py={2}
                                        disabled={!subscription.address}
                                        isDisabled={isEditing}
                                        onClick={() => {
                                            console.log("rename button clicked")
                                            setIsEditing(true)
                                        }
                                        }
                                        leftIcon={<EditIcon />}

                                    >
                                        Rename111
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
                                        onConfirm={() =>
                                            deleteSubscription.mutate(subscription.id)
                                        }
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
                            </Flex>
                        </Stack>
                    </AccordionPanel>
                </AccordionItem>
            )}
            {isDesktopView && (
                <Tr key={`token-row-${subscription.id}`}>
                    <Td {...cellProps}>
                        <Tooltip
                            label={`${subscriptionTypeNames[
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
            )}
        </>
    );
}

export default SubscriptionCard;

