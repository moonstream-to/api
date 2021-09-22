import { Fragment, React } from "react";
import {
  useClipboard,
  IconButton,
  Popover,
  PopoverTrigger,
  PopoverContent,
  PopoverHeader,
  PopoverArrow,
} from "@chakra-ui/react";
import { BiCopy } from "react-icons/bi";

const CopyButton = (props) => {
  const children = props.children ? props.children : "";
  const copyString = props.prefix ? props.prefix + children : children;

  const { onCopy } = useClipboard(copyString);

  return (
    <Fragment>
      <Popover placement="bottom-start">
        {({ isOpen, onClose }) => {
          if (isOpen) {
            setTimeout(() => onClose(), 1000);
          }
          return (
            <Fragment>
              <PopoverTrigger>
                <IconButton
                  onClick={onCopy}
                  icon={<BiCopy />}
                  colorScheme="orange"
                  variant="ghost"
                  size="sm"
                />
              </PopoverTrigger>
              <PopoverContent
                border="none"
                bgColor="teal.500"
                width="min-content"
              >
                <PopoverHeader border="none" color="white.100">
                  Copied!
                </PopoverHeader>
                <PopoverArrow
                  borderWidth="0"
                  border="none"
                  bgColor="teal.500"
                />
              </PopoverContent>
            </Fragment>
          );
        }}
      </Popover>
      {props.children}
    </Fragment>
  );
};

export default CopyButton;
