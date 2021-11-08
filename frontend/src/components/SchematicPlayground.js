import React, { useRef } from "react";
import { Box, Button, useBreakpointValue } from "@chakra-ui/react";
import DragOnGrid from "./DragOnGrid";
import Xarrow from "react-xarrows";

const SchematicPlayground = () => {
  const gridCellSize = useBreakpointValue({
    base: 24,
    sm: 32,
    md: 64,
    lg: 64,
    xl: 64,
    "2xl": 64,
  });
  const ref1 = useRef(null);
  const ref2 = useRef(null);
  const ref3 = useRef(null);
  const ref4 = useRef(null);
  const ref5 = useRef(null);
  const ref6 = useRef(null);
  const ref7 = useRef(null);
  const ref8 = useRef(null);
  if (!gridCellSize) return "";
  return (
    <>
      <Box
        h={`${(gridCellSize * 5 + 1).toString()}` + `px`}
        // h={`301px`}
        w="100%"
        bgColor="white"
        bgSize={`${(gridCellSize / 6).toString() + "px"}  ${
          (gridCellSize / 6).toString() + "px"
        }, ${gridCellSize.toString() + "px"} ${gridCellSize.toString() + "px"}`}
        bgImage={`linear-gradient(to bottom, transparent ${
          (gridCellSize / 10).toString() + "px"
        }, white ${(gridCellSize / 10).toString() + "px"}),
          linear-gradient(to right, #dee3ea 1px, transparent 1px),
          linear-gradient(to right, transparent ${
            (gridCellSize / 10).toString() + "px"
          }, white ${(gridCellSize / 10).toString() + "px"}),
          linear-gradient(to bottom, #dee3ea 1px, transparent 1px)`}
        maxW={`${(gridCellSize * 11 + 1).toString()}` + `px`}
        placeSelf="center"
      >
        <DragOnGrid
          ref={ref4}
          gridStep={gridCellSize}
          defaultPosition={{ x: 5, y: 2 }}
        >
          <Button
            m={0}
            p={0}
            borderRadius="sm"
            ref={ref4}
            className="handle"
            minW={`${gridCellSize.toString}` + `px`}
            fontSize={(gridCellSize / 4).toString() + `px`}
            boxSize={`${gridCellSize.toString()}` + "px"}
            borderStyle="inset"
            bg="green.900"
            color="white"
            textAlign="center"
            zIndex={10}
          >
            MSTR
          </Button>
        </DragOnGrid>
        <DragOnGrid
          ref={ref2}
          gridStep={gridCellSize}
          defaultPosition={{ x: 4, y: 0 }}
        >
          <Button
            m={0}
            ref={ref2}
            p={0}
            borderRadius="sm"
            className="handle"
            minW={`${gridCellSize.toString}` + `px`}
            minH={`${gridCellSize.toString}` + `px`}
            fontSize={(gridCellSize / 4).toString() + `px`}
            boxSize={`${gridCellSize.toString()}` + "px"}
            bg="blue.900"
            color="white"
            textAlign="center"
            zIndex={10}
          >
            DEX
          </Button>
        </DragOnGrid>
        <DragOnGrid
          ref={ref3}
          gridStep={gridCellSize}
          defaultPosition={{ x: 3, y: 4 }}
        >
          <Button
            m={0}
            ref={ref3}
            p={0}
            borderRadius="sm"
            className="handle"
            minW={`${gridCellSize.toString}` + `px`}
            fontSize={(gridCellSize / 4).toString() + `px`}
            boxSize={`${gridCellSize.toString()}` + "px"}
            bg="orange.900"
            color="white"
            textAlign="center"
            zIndex={10}
          >
            NFT
          </Button>
        </DragOnGrid>
        <DragOnGrid
          ref={ref1}
          gridStep={gridCellSize}
          defaultPosition={{ x: -2, y: 1 }}
        >
          <Button
            m={0}
            ref={ref1}
            p={0}
            borderRadius="sm"
            className="handle"
            minW={`${gridCellSize.toString}` + `px`}
            fontSize={(gridCellSize / 4).toString() + `px`}
            boxSize={`${gridCellSize.toString()}` + "px"}
            bg="red.900"
            color="white"
            textAlign="center"
            zIndex={10}
          >
            ERC20
          </Button>
        </DragOnGrid>
        <DragOnGrid
          ref={ref4}
          gridStep={gridCellSize}
          defaultPosition={{ x: -3, y: 4 }}
        >
          <Button
            m={0}
            ref={ref5}
            p={0}
            borderRadius="sm"
            className="handle"
            minW={`${gridCellSize.toString}` + `px`}
            fontSize={(gridCellSize / 4).toString() + `px`}
            boxSize={`${gridCellSize.toString()}` + "px"}
            bg="red.900"
            color="white"
            textAlign="center"
            zIndex={10}
          >
            EIP1155
          </Button>
        </DragOnGrid>
        <DragOnGrid
          ref={ref4}
          gridStep={gridCellSize}
          defaultPosition={{ x: 3, y: 3 }}
        >
          <Button
            m={0}
            ref={ref6}
            p={0}
            borderRadius="sm"
            className="handle"
            minW={`${gridCellSize.toString}` + `px`}
            fontSize={(gridCellSize / 4).toString() + `px`}
            boxSize={`${gridCellSize.toString()}` + "px"}
            bg="blue.900"
            color="white"
            textAlign="center"
            zIndex={10}
          >
            ERC721
          </Button>
        </DragOnGrid>
        <DragOnGrid
          ref={ref4}
          gridStep={gridCellSize}
          defaultPosition={{ x: 4, y: 4 }}
        >
          <Button
            m={0}
            ref={ref7}
            p={0}
            borderRadius="sm"
            className="handle"
            minW={`${gridCellSize.toString}` + `px`}
            fontSize={(gridCellSize / 4).toString() + `px`}
            boxSize={`${gridCellSize.toString()}` + "px"}
            bg="green.900"
            color="white"
            textAlign="center"
            zIndex={10}
          >
            DAO
          </Button>
        </DragOnGrid>
        <DragOnGrid
          ref={ref4}
          gridStep={gridCellSize}
          defaultPosition={{ x: 2, y: 0 }}
        >
          <Button
            m={0}
            ref={ref8}
            p={0}
            borderRadius="sm"
            className="handle"
            minW={`${gridCellSize.toString}` + `px`}
            fontSize={(gridCellSize / 4).toString() + `px`}
            boxSize={`${gridCellSize.toString()}` + "px"}
            bg="orange.900"
            color="white"
            textAlign="center"
            zIndex={10}
          >
            Oracle
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
        gridBreak={(gridCellSize * 0.5).toString() + "px"}
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
        gridBreak={(gridCellSize * 0.5).toString() + "px"}
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
        gridBreak={(gridCellSize * 0.5).toString() + "px"}
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
        gridBreak={(gridCellSize * 0.5).toString() + "px"}
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
        gridBreak={(gridCellSize * 0.5).toString() + "px"}
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
        gridBreak={(gridCellSize * 0.5).toString() + "px"}
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
        gridBreak={(gridCellSize * 0.5).toString() + "px"}
        path="grid"
        showHead={false}
        start={ref8} //can be react ref
        end={ref4} //or an id
      />
    </>
  );
};

export default SchematicPlayground;
