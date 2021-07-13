
import { jsx } from "@emotion/react";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import {
  Heading,
  Box,
  FormControl,
  FormErrorMessage,
  InputGroup,
  Button,
  Input,
} from "@chakra-ui/react";
import Modal from "./Modal";
import { useCreateJournal } from "../core/hooks";

const NewJournalModal = ({ toggleModal }) => {
  const { handleSubmit, errors, register } = useForm();
  const [inputCount, setInputCount] = useState("0");
  const [createJournal, { isLoading, data }] = useCreateJournal();

  const handleInput = (e) => {
    if (inputCount === 50) {
      return;
    }

    setInputCount(e.target.value.length);
  };

  useEffect(() => {
    if (!data) {
      return;
    }

    toggleModal(null);
  }, [data, toggleModal]);

  return (
    <Modal onClose={() => toggleModal(null)}>
      <Heading mt={2} size="lg">
        Create Journal
      </Heading>
      <form onSubmit={handleSubmit(createJournal)}>
        <FormControl position="relative" isInvalid={errors.name}>
          <InputGroup pt={4} width="100%">
            <Input
              colorScheme="primary"
              variant="filled"
              onChange={(e) => handleInput(e)}
              placeholder="Journal name"
              name="name"
              ref={register({ required: "name is required!" })}
            />
          </InputGroup>
          <Box
            right="0"
            position="absolute"
            fontSize="sm"
            color="gray.200"
            as="span"
          >
            {inputCount}/50
          </Box>
          <FormErrorMessage color="unsafe.400" pl="1">
            {errors.name && errors.name.message}
          </FormErrorMessage>
        </FormControl>
        <Box height="1px" width="100%" background="#eaebf8" mb="1.875rem" />
        <Button
          mt={8}
          type="submit"
          width="100%"
          variant="solid"
          colorScheme="primary"
          isLoading={isLoading}
        >
          Create
        </Button>
      </form>
    </Modal>
  );
};

export default NewJournalModal;
