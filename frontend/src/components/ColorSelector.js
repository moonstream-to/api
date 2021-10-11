import { React, useEffect, useState } from "react";
import {
  Box,
  Popover,
  PopoverTrigger,
  PopoverContent,
  PopoverHeader,
  PopoverBody,
  PopoverFooter,
  PopoverArrow,
  PopoverCloseButton,
  Portal,
  Stack,
  IconButton,
  Text,
  Input,
  useDisclosure,
  Button,
} from "@chakra-ui/react";
import { makeColor } from "../core/utils/makeColor";
import { BiRefresh } from "react-icons/bi";
import { GithubPicker } from "react-color";

const ColorSelector = (props) => {
  const { onOpen, onClose, isOpen } = useDisclosure();
  const [color, setColor] = useState(props.initialColor ?? makeColor());
  const [triggerColor, setTriggerColor] = useState(color);

  useEffect(() => {
    setTriggerColor(props.initialColor);
  }, [props.initialColor]);

  const handleChangeColorComplete = (color) => {
    setColor(color.hex);
  };

  const handleChangeColor = (event) => setColor(event.target.value);

  return (
    <Popover isOpen={isOpen} onOpen={onOpen} onClose={onClose}>
      <PopoverTrigger>
        <Box
          placeSelf="center"
          boxSize="24px"
          borderRadius="sm"
          bgColor={triggerColor}
        ></Box>
      </PopoverTrigger>
      <Portal>
        <PopoverContent bg={"white.100"}>
          <PopoverArrow />
          <PopoverHeader>Change color</PopoverHeader>
          <PopoverCloseButton />
          <PopoverBody>
            <Stack direction="row" pb={2}>
              <Text fontWeight="600" alignSelf="center">
                Label color
              </Text>{" "}
              <IconButton
                size="md"
                color={"white.100"}
                _hover={{ bgColor: { color } }}
                bgColor={color}
                variant="outline"
                onClick={() => setColor(makeColor())}
                icon={<BiRefresh />}
              />
              <Input
                type="input"
                placeholder="color"
                name="color"
                value={color}
                onChange={handleChangeColor}
                w="200px"
                onSubmit={handleChangeColorComplete}
              ></Input>
            </Stack>
            <GithubPicker
              // color={this.state.background}
              onChangeComplete={handleChangeColorComplete}
            />
          </PopoverBody>
          <PopoverFooter>
            <Button
              onClick={() => {
                props.callback(color);
                onClose();
              }}
              colorScheme="green"
              variant="outline"
            >
              Apply
            </Button>
          </PopoverFooter>
        </PopoverContent>
      </Portal>
    </Popover>
  );
};

export default ColorSelector;
