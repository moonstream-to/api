
import { jsx } from "@emotion/react";
import { Skeleton, IconButton } from "@chakra-ui/react";
import {
  Table,
  Th,
  Td,
  Tr,
  Thead,
  Tbody,
  Editable,
  EditableInput,
  EditablePreview,
} from "@chakra-ui/react";
import { DeleteIcon } from "@chakra-ui/icons";
import moment from "moment";
import { CopyButton } from ".";

const List = ({ data, revoke, isLoading, updateCallback }) => {
  const userToken = localStorage.getItem("BUGOUT_ACCESS_TOKEN");

  if (data) {
    return (
      <Table
        variant="simple"
        colorScheme="primary"
        justifyContent="center"
        alignItems="baseline"
        h="auto"
        size="sm"
      >
        <Thead>
          <Tr>
            <Th>Token</Th>
            <Th>Date Created</Th>
            <Th>Note</Th>
            <Th>Actions</Th>
          </Tr>
        </Thead>
        <Tbody>
          {data.data.token.map((token) => {
            if (token.active) {
              if (userToken !== token.id) {
                return (
                  <Tr key={`token-row-${token.id}`}>
                    <Td mr={4} p={0}>
                      <CopyButton>{token.id}</CopyButton>
                    </Td>
                    <Td py={0}>{moment(token.created_at).format("L")}</Td>
                    <Td py={0}>
                      <Editable
                        colorScheme="primary"
                        placeholder="enter note here"
                        defaultValue={token.note}
                        onSubmit={(nextValue) =>
                          updateCallback({ token: token.id, note: nextValue })
                        }
                      >
                        <EditablePreview
                          maxW="40rem"
                          _placeholder={{ color: "black" }}
                        />
                        <EditableInput maxW="40rem" />
                      </Editable>
                    </Td>
                    <Td py={0}>
                      <IconButton
                        size="sm"
                        variant="ghost"
                        colorScheme="primary"
                        onClick={() => revoke(token.id)}
                        icon={<DeleteIcon />}
                      />
                    </Td>
                  </Tr>
                );
              } else return null;
            } else return null;
          })}
        </Tbody>
      </Table>
    );
  } else if (isLoading) {
    return <Skeleton />;
  } else {
    return "";
  }
};
export default List;
