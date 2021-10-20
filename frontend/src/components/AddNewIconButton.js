import React, { useContext } from "react";
import {
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  MenuGroup,
  MenuDivider,
  IconButton,
  chakra,
  useDisclosure,
  Drawer,
  DrawerBody,
  DrawerFooter,
  DrawerHeader,
  DrawerOverlay,
  DrawerContent,
  DrawerCloseButton,
  FormLabel,
  Input,
  Stack,
  InputGroup,
  InputLeftAddon,
  Box,
  Textarea,
  Button,
} from "@chakra-ui/react";
import { PlusSquareIcon } from "@chakra-ui/icons";
import UIContext from "../core/providers/UIProvider/context";

const AddNewIconButton = (props) => {
  const ui = useContext(UIContext);
  const { onOpen, isOpen, onClose } = useDisclosure();
  const firstField = React.useRef();
  return (
    <>
      <Drawer
        isOpen={isOpen}
        placement="top"
        size="full"
        initialFocusRef={firstField}
        onClose={onClose}
      >
        <DrawerOverlay />
        <DrawerContent>
          <DrawerCloseButton />
          <DrawerHeader borderBottomWidth="1px">
            Create a new dashboard from an ABI
          </DrawerHeader>

          <DrawerBody>
            <Stack spacing="24px">
              <Box>
                <FormLabel htmlFor="username">Name dashboard</FormLabel>
                <Input
                  ref={firstField}
                  id="username"
                  type="search"
                  placeholder="Please enter user name"
                />
              </Box>

              <Box>
                <FormLabel htmlFor="url">Address</FormLabel>
                <InputGroup>
                  <InputLeftAddon>Contract @</InputLeftAddon>
                  <Input
                    type="url"
                    id="url"
                    placeholder="Please enter ens domain or address"
                  />
                </InputGroup>
              </Box>

              <Box>
                <FormLabel htmlFor="desc">ABI</FormLabel>
                <Textarea
                  id="desc"
                  placeholder="ABI Upload element should be here instead"
                />
              </Box>
            </Stack>
          </DrawerBody>

          <DrawerFooter borderTopWidth="1px">
            <Button variant="outline" mr={3} onClick={onClose}>
              Cancel
            </Button>
            <Button
              colorScheme="blue"
              onClick={() => {
                console.log("submit clicked");
              }}
            >
              Submit
            </Button>
          </DrawerFooter>
        </DrawerContent>
      </Drawer>
      <Menu>
        <MenuButton
          {...props}
          as={IconButton}
          aria-label="Account menu"
          icon={<PlusSquareIcon />}
          // variant="outline"
          color="gray.100"
        />
        <MenuList
          zIndex="dropdown"
          width={["100vw", "100vw", "18rem", "20rem", "22rem", "24rem"]}
          borderRadius={0}
        >
          <MenuGroup>
            <MenuItem onClick={onOpen}>New Dashboard...</MenuItem>

            {ui.isInDashboard && <MenuItem>New report...</MenuItem>}
          </MenuGroup>
          <MenuDivider />
        </MenuList>
      </Menu>
    </>
  );
};

const ChakraAddNewIconButton = chakra(AddNewIconButton);

export default ChakraAddNewIconButton;
