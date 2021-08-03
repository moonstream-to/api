import React from "react";
import {
  Code,
  Stat,
  StatLabel,
  StatGroup,
  StatHelpText,
  StatNumber,
  Box,
  VStack,
} from "@chakra-ui/react";
import { Table, Thead, Tbody, Tr, Th, Td } from "@chakra-ui/react";

const TxABI = (props) => {
  const byteCode = props.byteCode;
  const abi = props.abi;
  console.log(abi.functions);
  return (
    <VStack spacing={3}>
      <br />
      <h2>Transaction smart contract bytecode:</h2>
      <Code w="95%" colorScheme="facebook">
        {byteCode}
      </Code>
      <h2>Smart contract abi:</h2>
      <Table>
        <Thead>
          <Tr>
            <Th>Signature hex</Th>
            <Th>Decompiled signature</Th>
            <Th>Signature type</Th>
          </Tr>
        </Thead>
        <Tbody>
          {abi.functions.concat(abi.events).map((el) => (
            <Tr key={el.hex_signature}>
              <Td>{el.hex_signature}</Td>
              <Td>
                {el.text_signature_candidates.length > 0
                  ? el.text_signature_candidates.join(", ")
                  : "Unknown"}
              </Td>
              <Td>{el.type}</Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
    </VStack>
  );
};
const TxInfo = (props) => {
    const transaction = props.transaction;
    const dont_display = (key) => {
        return !["input"].includes(key)
    }
    return (
        <Box boxShadow="xs" p="6" rounded="md">
            <StatGroup>
                <Stat>
                    <StatLabel>Value</StatLabel>
                    <StatNumber>{transaction.tx.value}</StatNumber>
                    <StatHelpText>amount of ETH to transfer in WEI</StatHelpText>
                </Stat>
                <Stat>
                    <StatLabel>Gas</StatLabel>
                    <StatNumber>{transaction.tx.gas}</StatNumber>
                    <StatHelpText>gas limit for transaction</StatHelpText>
                </Stat>
                <Stat>
                    <StatLabel>Gas price</StatLabel>
                    <StatNumber>{transaction.tx.gasPrice}</StatNumber>
                    <StatHelpText>the fee the sender pays per unit of gas</StatHelpText>
                </Stat>
            </StatGroup>
            
            <Table variant="simple" >
                <Tbody>
                    {Object.keys(transaction.tx).filter(dont_display).map((key) => (
                        (transaction.tx[key] != undefined && <Tr key = {key}>
                            <Td>{key}</Td>
                            <Td>{transaction.tx[key]}</Td>
                        </Tr>)
                    ))}
                </Tbody>
            </Table>
            {transaction.tx.input && transaction.tx.input !== "0x" &&
                <TxABI 
                byteCode={transaction.tx.input} 
                abi={transaction.abi}
                />
            }
        </Box>
        
            
    )
}
export default TxInfo;
