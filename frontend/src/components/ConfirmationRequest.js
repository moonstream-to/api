import React, { Fragment } from "react";
import {
  Popover,
  PopoverTrigger,
  PopoverContent,
  PopoverCloseButton,
  PopoverHeader,
  PopoverFooter,
  PopoverBody,
  Button,
} from "@chakra-ui/react";

const ConfirmationRequest = (props) => {
  return (
    <Popover>
      {({ onClose }) => (
        <Fragment>
          <PopoverTrigger>{props.children}</PopoverTrigger>
          <PopoverContent zIndex={100} bg="White">
            <PopoverCloseButton />
            <PopoverHeader fontWeight="bold">{props.header}</PopoverHeader>
            <PopoverBody fontSize="md">{props.bodyMessage}</PopoverBody>
            <PopoverFooter>
              <Button
                onClick={onClose}
                colorScheme="blue"
                variant="outline"
                size="sm"
              >
                No
              </Button>
              <Button
                onClick={() => {
                  props.onConfirm();
                  onClose();
                }}
                colorScheme="red"
                variant="solid"
                size="sm"
              >
                Yes
              </Button>
            </PopoverFooter>
          </PopoverContent>
        </Fragment>
      )}
    </Popover>
  );
};

export default ConfirmationRequest;
