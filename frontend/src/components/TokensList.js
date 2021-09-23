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
  Button,
  EditablePreview,
} from "@chakra-ui/react";
import { DeleteIcon, TriangleDownIcon } from "@chakra-ui/icons";
import moment from "moment";
import CopyButton from "./CopyButton";

const SORT_BY_TYPES = {
  DATE: 0,
  LABEL: 1,
};
const SORT_DIRECTION_TYPES = {
  ASC: true,
  DESC: false,
};
const List = ({ data, revoke, isLoading, update }) => {
  const [stateData, setStateData] = useState(data);
  const userToken = localStorage.getItem("MOONSTREAM_ACCESS_TOKEN");
  const [sortBy, setSortBy] = useState({
    column: SORT_BY_TYPES.LABEL,
    direction: SORT_DIRECTION_TYPES.ASC,
  });
  useEffect(() => {
    if (data?.token?.length > 0) {
      const sortedTokens = data.token.sort(function (a, b) {
        var aName = a?.note?.toUpperCase();
        var bName = b?.note?.toUpperCase();

        if ((a.note || b.note) && sortBy.column === SORT_BY_TYPES.LABEL) {
          if (!b.note) return -1;
          if (sortBy.direction === SORT_DIRECTION_TYPES.ASC) {
            return aName < bName ? -1 : aName > bName ? 1 : 0;
          } else {
            return aName > bName ? -1 : aName < bName ? 1 : 0;
          }
        } else {
          if (sortBy.direction === SORT_DIRECTION_TYPES.ASC) {
            return new Date(b.created_at) - new Date(a.created_at);
          } else {
            return new Date(a.created_at) - new Date(b.created_at);
          }
        }
      });

      setStateData({ ...data, token: [...sortedTokens] });
    }
  }, [data, sortBy]);

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
            <Th>
              <Button
                variant="link"
                my={0}
                size="sm"
                colorScheme="blue"
                onClick={() =>
                  setSortBy({
                    column: SORT_BY_TYPES.LABEL,
                    direction:
                      sortBy.column !== SORT_BY_TYPES.LABEL
                        ? SORT_DIRECTION_TYPES.ASC
                        : !sortBy.direction,
                  })
                }
                rightIcon={
                  <TriangleDownIcon
                    boxSize="12px"
                    transform={
                      sortBy.direction === SORT_DIRECTION_TYPES.ASC
                        ? "rotate(180deg)"
                        : "rotate(0deg)"
                    }
                  />
                }
              >
                Label
              </Button>
            </Th>
            <Th {...cellProps}>Token</Th>
            <Th {...cellProps}>
              <Button
                variant="link"
                my={0}
                size="sm"
                colorScheme="blue"
                onClick={() =>
                  setSortBy({
                    column: SORT_BY_TYPES.DATE,
                    direction:
                      sortBy.column !== SORT_BY_TYPES.DATE
                        ? SORT_DIRECTION_TYPES.ASC
                        : !sortBy.direction,
                  })
                }
                rightIcon={
                  <TriangleDownIcon
                    boxSize="12px"
                    transform={
                      sortBy.direction === SORT_DIRECTION_TYPES.ASC
                        ? "rotate(180deg)"
                        : "rotate(0deg)"
                    }
                  />
                }
              >
                {" "}
                Date Created{" "}
              </Button>

              {/* <IconButton
                hidden={sortBy.column !== SORT_BY_TYPES.DATE}
                size="xs"
                variant="ghost"
                icon={}
                onClick={() =>
                  setSortBy({
                    column: SORT_BY_TYPES.DATE,
                    direction: !sortBy.direction,
                  })
                }

              /> */}
            </Th>
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
