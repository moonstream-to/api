import React, { useState, useEffect, useLayoutEffect } from "react";
import TokensList from "../../src/components/TokensList";
import TokenRequest from "../../src/components/TokenRequest";
import { useTokens } from "../../src/core/hooks";
import {
  VStack,
  Stack,
  Input,
  Box,
  Center,
  Spinner,
  ScaleFade,
  Button,
  Heading,
  useDisclosure,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalCloseButton,
  InputGroup,
} from "@chakra-ui/react";
import { getLayout } from "../../src/layouts/AccountLayout";

const Tokens = () => {
  const { onOpen, onClose, isOpen } = useDisclosure();
  const [newToken, setNewToken] = useState(null);
  const [filter, setFilter] = useState("");
  const [tokens, setTokens] = useState();
  const { list, updateMutation, revoke, isLoading, data } = useTokens();

  useEffect(() => {
    list();
    //eslint-disable-next-line
  }, []);

  useLayoutEffect(() => {
    if (newToken) {
      const newData = { ...tokens };
      newData.token.push(newToken);
      setTokens(newData);
      setNewToken(null);
    }
  }, [newToken, list, data, tokens]);

  useLayoutEffect(() => {
    if (data?.data?.user_id) {
      setTokens(data.data);
    }
  }, [data, isLoading]);

  useEffect(() => {
    document.title = `Tokens`;
  }, []);

  const handleChange = (event) => setFilter(event.target.value);
  return (
    <Box>
      {isLoading && !tokens ? (
        <Center>
          <Spinner
            hidden={false}
            my={8}
            size="lg"
            color="blue.500"
            thickness="4px"
            speed="1.5s"
          />
        </Center>
      ) : (
        <ScaleFade in>
          <Modal isOpen={isOpen} onClose={onClose} size="lg" trapFocus={false}>
            <ModalOverlay />
            <ModalContent>
              <ModalHeader>New API access token</ModalHeader>
              <ModalCloseButton />
              <ModalBody>
                <TokenRequest setNewToken={setNewToken} onClose={onClose} />
              </ModalBody>
            </ModalContent>
          </Modal>
          <Heading variant="tokensScreen"> My API tokens </Heading>
          <VStack overflow="initial" maxH="unset" height="100%" maxW="100%">
            <Stack direction={["column", "row", null]} w="100%">
              <InputGroup size="sm" variant="outline">
                <Input
                  type="search"
                  maxW="300px"
                  flexBasis="50px"
                  flexGrow={1}
                  display="flex"
                  minW="150px"
                  w="unset"
                  borderRadius="md"
                  placeholder="Type here to filter by label name"
                  value={filter}
                  onChange={handleChange}
                />
              </InputGroup>
              <Button
                alignSelf="flex-end"
                onClick={onOpen}
                colorScheme="orange"
                variant="solid"
                px="2rem"
                size="sm"
              >
                Add new token
              </Button>
            </Stack>
            <TokensList
              data={tokens}
              filter={filter}
              revoke={revoke}
              isLoading={isLoading}
              update={updateMutation}
            />
          </VStack>
        </ScaleFade>
      )}
    </Box>
  );
};

Tokens.getLayout = getLayout;
export default Tokens;
