import React from "react";
import { IconButton } from "@chakra-ui/react";
import {
  Table,
  Th,
  Td,
  Tr,
  Thead,
  Tbody,
  Text,
  Center,
  Spinner,
} from "@chakra-ui/react";
import { DeleteIcon } from "@chakra-ui/icons";
import { CopyButton, ConfirmationRequest, NewTokenTr } from ".";
import { useForm } from "react-hook-form";

const TokenList = ({
  tokens,
  revoke,
  isLoading,
  isNewTokenOpen,
  toggleNewToken,
  createToken,
  journalName,
}) => {
  const { register, handleSubmit, errors } = useForm();
  if (isLoading)
    return (
      <Center>
        <Spinner />
      </Center>
    );

  const handleTokenSubmit = ({ appName, appVersion }) => {
    createToken({ appName, appVersion }).then(() => toggleNewToken(false));
  };

  return (
    <form onSubmit={handleSubmit(handleTokenSubmit)}>
      <Table
        variant="simple"
        colorScheme="blue"
        justifyContent="center"
        alignItems="baseline"
        h="auto"
        size="sm"
      >
        <Thead>
          <Tr>
            <Th>Token</Th>
            <Th>App Name</Th>
            <Th>App version</Th>
            <Th>Action</Th>
          </Tr>
        </Thead>
        <Tbody>
          {tokens.map((token, idx) => {
            return (
              <Tr key={`RestrictedToken-row-${idx}`}>
                <Td mr={4} p={0}>
                  <CopyButton>{token.restricted_token_id}</CopyButton>
                </Td>
                <Td py={0}>{token.app_name}</Td>
                <Td py={0}>{token.app_version}</Td>
                <Td py={0}>
                  <ConfirmationRequest
                    bodyMessage={"please confirm"}
                    header={"Delete token"}
                    onConfirm={() => revoke(token.restricted_token_id)}
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
            );
          })}

          <NewTokenTr
            isOpen={isNewTokenOpen}
            toggleSelf={toggleNewToken}
            errors={errors}
            register={register}
            journalName={journalName}
          />
        </Tbody>
      </Table>
      {tokens.length < 1 && (
        <Center>
          <Text my={4}>Create Usage report tokens here</Text>
        </Center>
      )}
    </form>
  );
};
export default TokenList;
