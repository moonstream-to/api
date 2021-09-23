import React, { useEffect, useState } from "react";
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
import CopyButton from "./CopyButton";

const List = ({ data, revoke, isLoading, update }) => {
  const [stateData, setStateData] = useState(data);
  const userToken = localStorage.getItem("MOONSTREAM_ACCESS_TOKEN");

  useEffect(() => {
    if (data?.token?.length > 0) {
      const sortedTokens = data.token.sort(function (a, b) {
        var aName = a?.note?.toUpperCase();
        var bName = b?.note?.toUpperCase();
        if (a.note || b.note) {
          return aName < bName ? -1 : aName < bName ? 1 : 0;
        } else {
          return new Date(b.created_at) - new Date(a.created_at);
        }
      });

      setStateData({ ...data, token: [...sortedTokens] });
    }
  }, [data]);

  const cellProps = {
    px: ["2px", "6px", "inherit"],
  };
  if (stateData) {
    return (
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
            <Th>Label</Th>
            <Th {...cellProps}>Token</Th>
            <Th {...cellProps}>Date Created</Th>
            <Th {...cellProps}>Actions</Th>
          </Tr>
        </Thead>
        <Tbody>
          {stateData.token.map((token) => {
            if (token.active) {
              if (userToken !== token.id) {
                return (
                  <Tr key={`token-row-${token.id}`}>
                    <Td py={0} {...cellProps}>
                      <Editable
                        colorScheme="blue"
                        placeholder="Click to set up label"
                        defaultValue={token.note}
                        onSubmit={(nextValue) =>
                          update.mutate({ token: token.id, note: nextValue })
                        }
                      >
                        <EditablePreview
                          maxW="40rem"
                          textColor={token.note ? "inherit" : "gray.900"}
                          _placeholder={{ color: "black" }}
                        />
                        <EditableInput maxW="40rem" />
                      </Editable>
                    </Td>
                    <Td
                      mr={4}
                      py={0}
                      {...cellProps}
                      isTruncated
                      maxW={["100px", "150px", "300px"]}
                    >
                      <CopyButton>{token.id}</CopyButton>
                    </Td>
                    <Td py={0} {...cellProps}>
                      {moment(token.created_at).format("L")}
                    </Td>
                    <Td py={0} {...cellProps}>
                      <IconButton
                        size="sm"
                        variant="ghost"
                        colorScheme="blue"
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
