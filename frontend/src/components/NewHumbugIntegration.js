
import { jsx } from "@emotion/react";
import { useRef, useEffect } from "react";
import {
  Box,
  Button,
  GridItem,
  Grid,
  Text,
  Heading,
  Input,
  FormErrorMessage,
  FormControl,
  InputGroup,
} from "@chakra-ui/react";
import { useHumbugs } from "../core/hooks";
import { useForm } from "react-hook-form";

const NewHumbugIntegration = ({ team }) => {
  const { createHumbugMutation } = useHumbugs();
  const inputRef = useRef();
  const {
    handleSubmit: addHumbugHandleSubmit,
    register: addHumbugRegister,
    errors: errorHambugRegister,
  } = useForm();

  const addHumbugHandler = ({ groupId, journalName }) => {
    createHumbugMutation.createHumbug({ groupId, journalName });
  };

  useEffect(() => {
    setTimeout(() => inputRef.current.focus(), 100);
  }, [inputRef]);

  return (
    <form onSubmit={addHumbugHandleSubmit(addHumbugHandler)}>
      <Box justifyContent="space-evenly">
        <Heading size="md">New Usage reports project</Heading>
        <Box>
          <Text>How would you like to name it? </Text>
          <FormControl isInvalid={errorHambugRegister.journalName}>
            <InputGroup>
              <Input
                name="journalName"
                placeholder="Usage report project name"
                ref={(e) => {
                  addHumbugRegister(e, { required: "Name is required" });
                  inputRef.current = e;
                }}
              />
            </InputGroup>
            <FormErrorMessage color="unsafe.400" pl="1">
              {errorHambugRegister.journalName &&
                errorHambugRegister.journalName.message}
            </FormErrorMessage>
          </FormControl>
          <Input
            type="hidden"
            name="groupId"
            ref={addHumbugRegister}
            defaultValue={team.group_id}
          ></Input>
          <Grid
            templateColumns="repeat(8, 1fr)"
            gap={1}
            alignItems="baseline"
            mt="1"
          >
            <GridItem colSpan={7} />
            <GridItem></GridItem>
          </Grid>
        </Box>
        <Button
          variant="outline"
          colorScheme="suggested"
          type="submit"
          isLoading={createHumbugMutation.isLoading}
        >
          Create
        </Button>
      </Box>
    </form>
  );
};

export default NewHumbugIntegration;
