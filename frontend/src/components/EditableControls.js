import React, { useContext, useState } from "react";
import { Skeleton, IconButton, Container, useEditable } from "@chakra-ui/react";
import {
    Td,
    Tr,
    Tooltip,
    Editable,
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



function EditableControls(editButtonClick) {
    const {
        isEditing,
        getSubmitButtonProps,
        getCancelButtonProps,
        getEditButtonProps,
        onEdit
    } = useEditable()

    React.useEffect(() => { if (editButtonClick) { onEdit() } }, [editButtonClick])

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

export default EditableControls;