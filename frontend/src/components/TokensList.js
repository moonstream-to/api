import React, { useEffect, useState, useMemo } from "react";
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
  useBreakpointValue,
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
const List = ({ data, revoke, isLoading, update, filter }) => {
  const [stateData, setStateData] = useState(data);
  const userToken = localStorage.getItem("MOONSTREAM_ACCESS_TOKEN");
  const [sortBy, setSortBy] = useState({
    column: SORT_BY_TYPES.LABEL,
    direction: SORT_DIRECTION_TYPES.ASC,
  });

  const buttonSize = useBreakpointValue({
    base: "xs",
    sm: "sm",
    md: "sm",
    lg: "sm",
    xl: "sm",
    "2xl": "sm",
  });

  const sortedTokens = useMemo(() => {
    return data?.token?.sort(function (a, b) {
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
  }, [sortBy, data]);

  useEffect(() => {
    if (data?.token?.length > 0) {
      const filteredTokens = sortedTokens.filter((item) => {
        if (filter === null || filter === undefined || filter === "") {
          return true;
        } else return item.note?.includes(filter);
      });

      setStateData({ ...data, token: [...filteredTokens] });
    }
  }, [data, sortBy, filter, sortedTokens]);

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
                mx={0}
                size={buttonSize}
                colorScheme={
                  sortBy.column !== SORT_BY_TYPES.LABEL ? "blue" : "orange"
                }
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
                    color={
                      sortBy.column !== SORT_BY_TYPES.LABEL && "transparent"
                    }
                    boxSize="12px"
                    transform={
                      sortBy.direction === SORT_DIRECTION_TYPES.ASC
                        ? "rotate(0deg)"
                        : "rotate(180deg)"
                    }
                  />
                }
              >
                Label
              </Button>
            </Th>
            <Th {...cellProps} fontSize={["xx-small", "xs", null]}>
              Token
            </Th>
            <Th {...cellProps} fontSize={["xx-small", "xs", null]}>
              <Button
                mx={0}
                variant="link"
                my={0}
                size={buttonSize}
                colorScheme={
                  sortBy.column !== SORT_BY_TYPES.DATE ? "blue" : "orange"
                }
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
                    color={
                      sortBy.column !== SORT_BY_TYPES.DATE && "transparent"
                    }
                    boxSize="12px"
                    transform={
                      sortBy.direction === SORT_DIRECTION_TYPES.ASC
                        ? "rotate(0deg)"
                        : "rotate(180deg)"
                    }
                  />
                }
              >
                {`Date Created`}
              </Button>
            </Th>
            <Th {...cellProps} fontSize={["xx-small", "xs", null]}>
              Actions
            </Th>
          </Tr>
        </Thead>
        <Tbody>
          {stateData.token?.map((token) => {
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
