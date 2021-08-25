import React from "react";
import { VStack, Code } from "@chakra-ui/react";
import { Table, Thead, Tbody, Tr, Th, Td } from "@chakra-ui/react";

const ContractSource = ({ source_info }) => {
  return (
    <VStack spacing={3}>
      <Table>
        <Thead>
          <Tr>
            <Th>Contract Name</Th>
            <Th>Compiler version</Th>
          </Tr>
        </Thead>
        <Tbody>
          <Tr key={source_info.name}>
            <Td>{source_info.name} </Td>
            <Td>{source_info.compiler_version}</Td>
          </Tr>
        </Tbody>
      </Table>
      <Code colorScheme="blackAlpha" w="110%">
        {source_info.source_code}
      </Code>
    </VStack>
  );
};

export default ContractSource;
