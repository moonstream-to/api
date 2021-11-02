import React, { useRef } from "react";
import { Box, Button } from "@chakra-ui/react";
import DragOnGrid from "../src/components/DragOnGrid";
import Xarrow from "react-xarrows";

const Sch = () => {
  const ref1 = useRef(null);
  const ref2 = useRef(null);
  const ref3 = useRef(null);
  const ref4 = useRef(null);
  const ref5 = useRef(null);
  const ref6 = useRef(null);
  const ref7 = useRef(null);
  const ref8 = useRef(null);
  return (
    <>
      <Box minH="100vh" w="100%" className="bgGrid">
        <DragOnGrid ref={ref1} defaultPosition={{ x: 0, y: 0 }}>
          <Button
            m={0}
            ref={ref1}
            className="handle"
            boxSize="60px"
            bg="green.900"
            color="white"
            textAlign="center"
            zIndex={10}
          >
            ERC20
          </Button>
        </DragOnGrid>
        <DragOnGrid ref={ref2} defaultPosition={{ x: 120, y: 0 }}>
          <Button
            m={0}
            ref={ref2}
            className="handle"
            boxSize="60px"
            bg="blue.900"
            color="white"
            textAlign="center"
            zIndex={10}
          >
            DEX
          </Button>
        </DragOnGrid>
        <DragOnGrid ref={ref3} defaultPosition={{ x: 180, y: 0 }}>
          <Button
            m={0}
            ref={ref3}
            className="handle"
            boxSize="60px"
            bg="orange.900"
            color="white"
            textAlign="center"
            zIndex={10}
          >
            NFT
          </Button>
        </DragOnGrid>
        <DragOnGrid ref={ref4} defaultPosition={{ x: 240, y: 0 }}>
          <Button
            m={0}
            ref={ref4}
            className="handle"
            boxSize="60px"
            bg="red.900"
            color="white"
            textAlign="center"
            zIndex={10}
          >
            MSTR
          </Button>
        </DragOnGrid>
        <DragOnGrid ref={ref4} defaultPosition={{ x: 240, y: 0 }}>
          <Button
            m={0}
            ref={ref5}
            className="handle"
            boxSize="60px"
            bg="red.900"
            color="white"
            textAlign="center"
            zIndex={10}
          >
            EIP1155
          </Button>
        </DragOnGrid>
        <DragOnGrid ref={ref4} defaultPosition={{ x: 240, y: 0 }}>
          <Button
            m={0}
            ref={ref6}
            className="handle"
            boxSize="60px"
            bg="blue.900"
            color="white"
            textAlign="center"
            zIndex={10}
          >
            ERC721
          </Button>
        </DragOnGrid>
        <DragOnGrid ref={ref4} defaultPosition={{ x: 240, y: 0 }}>
          <Button
            m={0}
            ref={ref7}
            className="handle"
            boxSize="60px"
            bg="green.900"
            color="white"
            textAlign="center"
            zIndex={10}
          >
            DAO
          </Button>
        </DragOnGrid>
        <DragOnGrid ref={ref4} defaultPosition={{ x: 240, y: 0 }}>
          <Button
            m={0}
            ref={ref8}
            className="handle"
            boxSize="60px"
            bg="orange.900"
            color="white"
            textAlign="center"
            zIndex={10}
          >
            ORACLE
          </Button>
        </DragOnGrid>
      </Box>
      <Xarrow
        dashness={{
          strokeLen: 10,
          nonStrokeLen: 15,
          animation: 1 * 1,
        }}
        color="#920050"
        path="grid"
        gridBreak="30px"
        //   startAnchor={"top"}
        showHead={false}
        start={ref3} //can be react ref
        end={ref4} //or an id
      />
      <Xarrow
        dashness={{
          strokeLen: 10,
          nonStrokeLen: 15,
          animation: 1 * 1,
        }}
        color="#113350"
        path="grid"
        gridBreak="30px"
        showHead={false}
        start={ref2} //can be react ref
        end={ref4} //or an id
      />
      <Xarrow
        dashness={{
          strokeLen: 10,
          nonStrokeLen: 15,
          animation: 1 * 1,
        }}
        color="#92D0F0"
        gridBreak="30px"
        path="grid"
        //   startAnchor={"top"}
        showHead={false}
        start={ref1} //can be react ref
        end={ref4} //or an id
      />
      <Xarrow
        dashness={{
          strokeLen: 10,
          nonStrokeLen: 15,
          animation: 1 * 1,
        }}
        color="#92D0F0"
        gridBreak="30px"
        path="grid"
        //   startAnchor={"top"}
        showHead={false}
        start={ref5} //can be react ref
        end={ref4} //or an id
      />
      <Xarrow
        dashness={{
          strokeLen: 10,
          nonStrokeLen: 15,
          animation: 1 * 1,
        }}
        color="#92D0F0"
        gridBreak="30px"
        path="grid"
        //   startAnchor={"top"}
        showHead={false}
        start={ref6} //can be react ref
        end={ref4} //or an id
      />
      <Xarrow
        dashness={{
          strokeLen: 10,
          nonStrokeLen: 15,
          animation: 1 * 1,
        }}
        color="#92D0F0"
        gridBreak="30px"
        path="grid"
        showHead={false}
        start={ref7} //can be react ref
        end={ref4} //or an id
      />
      <Xarrow
        dashness={{
          strokeLen: 10,
          nonStrokeLen: 15,
          animation: 1 * 1,
        }}
        color="#92D0F0"
        gridBreak="30px"
        path="grid"
        showHead={false}
        start={ref8} //can be react ref
        end={ref4} //or an id
      />
    </>
  );
};

export default Sch;
