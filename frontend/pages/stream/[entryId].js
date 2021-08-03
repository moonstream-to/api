import React from "react";
import { Flex, HStack, Skeleton, Heading } from "@chakra-ui/react";
//import { useTxInfo, useRouter } from "../../src/core/hooks";
import { useRouter } from "../../src/core/hooks";
// import FourOFour from "../../src/components/FourOFour";
// import FourOThree from "../../src/components/FourOThree";
import Tags from "../../src/components/Tags";
import Scrollable from "../../src/components/Scrollable";
import TxInfo from "../../src/components/TxInfo";
import { getLayout } from "../../src/layouts/EntriesLayout";

const Entry = () => {
  const router = useRouter();
  const { entryId } = router.params;
  /*  const {
    data: entry,
    isFetchedAfterMount,
    isLoading,
    isError,
    error,
  } = useJournalEntry(journalId, entryId, "personal");
*/
  const raw_transaction = {
    tx: {
      blockHash:
        "0x2f1cb4055fa3ba8af199aeba564917999b3e661d582082e5928721c3f4ef04ca",
      blockNumber: 12882164,
      from: "0x52f200565581ae950c765b67f574cfc99f662657",
      gas: 400000,
      gasPrice: 12500000000,
      hash: "0xee3d2c14cacc0e5b8085c0b1a0cbacb6ed79762220dcee0a9c19a5a25e59a331",
      input:
        "0x6102a8610026600b82828239805160001a60731461001957fe5b30600052607381538281f3fe73000000000000000000000000000000000000000030146080604052600436106100355760003560e01c80636e8af2721461003a575b600080fd5b6100576004803603602081101561005057600080fd5b50356100b2565b6040518083815260200180602001828103825283818151815260200191508051906020019060200280838360005b8381101561009d578181015183820152602001610085565b50505050905001935050505060405180910390f35b60048101546000906060908067ffffffffffffffff811180156100d457600080fd5b506040519080825280602002602001820160405280156100fe578160200160208202803683370190505b50915060005b8181101561017757600061014f670de0b6b3a764000061014688600401858154811061012c57fe5b6000918252602090912001546001600160a01b031661017e565b600f0b906101ff565b905080850194508084838151811061016357fe5b602090810291909101015250600101610104565b5050915091565b6000816001600160a01b031663ac969a73306040518263ffffffff1660e01b815260040180826001600160a01b0316815260200191505060206040518083038186803b1580156101cd57600080fd5b505afa1580156101e1573d6000803e3d6000fd5b505050506040513d60208110156101f757600080fd5b505192915050565b60008161020e5750600061026c565b600083600f0b121561021f57600080fd5b600f83900b6fffffffffffffffffffffffffffffffff8316810260401c90608084901c026001600160c01b0381111561025757600080fd5b60401b811981111561026857600080fd5b0190505b9291505056fea2646970667358221220bf54788224a5a22890835d5e41e3e9622b1a055984390a38ae02a95c53dccfd864736f6c63430007030033",
      nonce: 184,
      r: "0xe7e8e58deccd5f277928d25f7fc66548be1a84af811db8927dd86fbd08c5acd6",
      s: "0x2214b48d9ce2b80c11586ddaff5214429c99e09188f75c04b7b0d0b7536ec94c",
      to: null,
      transactionIndex: 76,
      type: "0x0",
      v: "0x25",
      value: 0,
    },
  };

  let isFetchedAfterMount = false;
  let isLoading = false;
  let isError = false;

  const ETHER_TX = {
    tx: {
      gas: 400000,
      gasPrice: 12500000000,
      value: 0,
      from: "0x52f200565581ae950c765b67f574cfc99f662657",
      to: null,
      hash: "0xee3d2c14cacc0e5b8085c0b1a0cbacb6ed79762220dcee0a9c19a5a25e59a331",
      blockHash:
        "0x2f1cb4055fa3ba8af199aeba564917999b3e661d582082e5928721c3f4ef04ca",
      blockNumber: 12882164,
      input:
        "0x6102a8610026600b82828239805160001a60731461001957fe5b30600052607381538281f3fe73000000000000000000000000000000000000000030146080604052600436106100355760003560e01c80636e8af2721461003a575b600080fd5b6100576004803603602081101561005057600080fd5b50356100b2565b6040518083815260200180602001828103825283818151815260200191508051906020019060200280838360005b8381101561009d578181015183820152602001610085565b50505050905001935050505060405180910390f35b60048101546000906060908067ffffffffffffffff811180156100d457600080fd5b506040519080825280602002602001820160405280156100fe578160200160208202803683370190505b50915060005b8181101561017757600061014f670de0b6b3a764000061014688600401858154811061012c57fe5b6000918252602090912001546001600160a01b031661017e565b600f0b906101ff565b905080850194508084838151811061016357fe5b602090810291909101015250600101610104565b5050915091565b6000816001600160a01b031663ac969a73306040518263ffffffff1660e01b815260040180826001600160a01b0316815260200191505060206040518083038186803b1580156101cd57600080fd5b505afa1580156101e1573d6000803e3d6000fd5b505050506040513d60208110156101f757600080fd5b505192915050565b60008161020e5750600061026c565b600083600f0b121561021f57600080fd5b600f83900b6fffffffffffffffffffffffffffffffff8316810260401c90608084901c026001600160c01b0381111561025757600080fd5b60401b811981111561026857600080fd5b0190505b9291505056fea2646970667358221220bf54788224a5a22890835d5e41e3e9622b1a055984390a38ae02a95c53dccfd864736f6c63430007030033",
      nonce: 184,
      r: "0xe7e8e58deccd5f277928d25f7fc66548be1a84af811db8927dd86fbd08c5acd6",
      s: "0x2214b48d9ce2b80c11586ddaff5214429c99e09188f75c04b7b0d0b7536ec94c",
      v: "0x25",
      transactionIndex: 76,
      type: "0x0",
    },
    is_smart_contract_deployment: true,
    is_smart_contract_call: false,
    smart_contract_address: "0x2f7E36b386F40d01A867BaffF3F321bC01882F7f",
    abi: {
      functions: [
        {
          hex_signature: "0x6e8af272",
          text_signature_candidates: [],
          type: "function",
        },
        {
          hex_signature: "0xac969a73",
          text_signature_candidates: ["viewNumeraireBalance(address)"],
          type: "function",
        },
        {
          hex_signature: "0xffffffff",
          text_signature_candidates: ["test266151307()", "lololo()"],
          type: "function",
        },
      ],
      events: [
        {
          hex_signature: "0x123456",
          text_signature_candidates: ["viewNumeraireBalance(address)"],
          type: "event",
        },
        {
          hex_signature: "0x123436",
          text_signature_candidates: [],
          type: "event",
        },
      ],
    },
    errors: [],
  };
  let entry = {
    title: ETHER_TX.tx.hash,
    content: "```json\n" + JSON.stringify(ETHER_TX) + "```",
  };

  // if (isError && error.response.status === 404) return <FourOFour />;
  // if (isError && error.response.status === 403) return <FourOThree />;
  // if (!entry || isLoading) return "";

  return (
    <Flex
      id="Entry"
      height="100%"
      flexGrow="1"
      flexDirection="column"
      key={entryId}
    >
      <Skeleton
        id="EntryNameSkeleton"
        mx={2}
        mt={2}
        overflow="initial"
        isLoaded={!isLoading}
      >
        <HStack id="EntryHeader" width="100%" m={0}>
          <Heading
            overflow="hidden"
            width={entry?.context_url ? "calc(100% - 28px)" : "100%"}
            // height="auto"
            minH="36px"
            style={{ marginLeft: "0" }}
            m={0}
            p={0}
            fontWeight="600"
            fontSize="1.5rem"
            textAlign="left"
          >
            {entry?.title}
          </Heading>
        </HStack>
      </Skeleton>
      <Skeleton
        id="TagsSkeleton"
        mx={2}
        overflow="initial"
        mt={1}
        isLoaded={isFetchedAfterMount || entry}
      >
        <Tags entry={entry} />
      </Skeleton>
      <Skeleton
        height="10px"
        flexGrow={1}
        id="EditorSkeleton"
        mx={2}
        mr={isFetchedAfterMount || entry ? 0 : 2}
        mt={1}
        isLoaded={isFetchedAfterMount || entry}
      >
        <Scrollable>
          <TxInfo transaction={ETHER_TX}></TxInfo>
        </Scrollable>
      </Skeleton>
    </Flex>
  );
};

Entry.getLayout = getLayout;
export default Entry;
