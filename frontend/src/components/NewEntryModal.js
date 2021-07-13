
import { jsx } from "@emotion/react";
import { useEffect } from "react";
import { useForm } from "react-hook-form";
import {
  Heading,
  Box,
  FormControl,
  FormErrorMessage,
  InputGroup,
  Input,
  Button,
} from "@chakra-ui/react";
import { Modal } from ".";
import { useCreateEntry, useRouter } from "../core/hooks";

const NewEntryModal = ({ toggleModal, journalId }) => {
  const router = useRouter();
  const { handleSubmit, errors, register } = useForm();
  const { createEntry, isLoading, data } = useCreateEntry(journalId);

  useEffect(() => {
    if (!data) {
      return;
    }

    if (data.data?.id) {
      router.push({
        pathname: `/app/personal/${journalId}/entries/${data.data.id}`,
        query: { ...router.query, mode: "write" },
      });
    }
    toggleModal(null);
  }, [data, toggleModal, journalId, router]);

  return (
    <Modal onClose={() => toggleModal(null)}>
      <Heading mt={2} as="h2" fontSize={["lg", "2xl"]}>
        Create Entry
      </Heading>
      <form onSubmit={handleSubmit(createEntry)}>
        <FormControl position="relative" isInvalid={errors.title}>
          <InputGroup pt={4} width="100%">
            <Input
              colorScheme="primary"
              variant="filled"
              placeholder="Entry Title"
              name="title"
              ref={register({ required: "title is required!" })}
            />
          </InputGroup>
          <FormErrorMessage color="unsafe.400" pl="1">
            {errors.title && errors.title.message}
          </FormErrorMessage>
        </FormControl>
        <Box height="1px" width="100%" background="#eaebf8" mb="1.875rem" />
        <Button
          mt={8}
          variant="solid"
          colorScheme="primary"
          type="submit"
          size="lg"
          width="100%"
          isLoading={isLoading}
        >
          Create
        </Button>
      </form>
    </Modal>
  );
};

export default NewEntryModal;
