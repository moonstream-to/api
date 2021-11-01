import React, { useRef } from "react";
import { Box } from "@chakra-ui/react";
import Schematic from "../src/components/schematic";
import Xarrow, { Xwrapper, useXarrow } from "react-xarrows";

const Sch = () => {
  const updateXarrow = useXarrow();
  const ref1 = useRef(null);
  const ref2 = useRef(null);
  const ref3 = useRef(null);
  const ref4 = useRef(null);
  return (
    <Box minH="100vh" w="100%" overflow="scroll">
      <Xwrapper>
        <Schematic ref={ref1} def={{ x: 0, y: 0 }} />
        <Schematic ref={ref2} def={{ x: 60, y: 0 }} />
        <Schematic ref={ref3} def={{ x: 120, y: 0 }} />
        <Schematic ref={ref4} def={{ x: 180, y: 0 }} />
        <Xarrow
          // showXarrow={!!box0Ref.current && !!box1Ref.current}
          dashness={{
            strokeLen: 10,
            nonStrokeLen: 15,
            animation: 1 * 1,
          }}
          // animateDrawing={true}
          color="#920050"
          path="grid"
          gridBreak="30px"
          //   startAnchor={"top"}
          showHead={false}
          start={ref1} //can be react ref
          end={ref2} //or an id
        />
        <Xarrow
          // showXarrow={!!box0Ref.current && !!box1Ref.current}
          dashness={{
            strokeLen: 10,
            nonStrokeLen: 15,
            animation: 1 * 1,
          }}
          // animateDrawing={true}
          color="#113350"
          path="grid"
          gridBreak="30px"
          //   startAnchor={"auto"}
          showHead={false}
          start={ref2} //can be react ref
          end={ref3} //or an id
        />
        <Xarrow
          // showXarrow={!!box0Ref.current && !!box1Ref.current}
          dashness={{
            strokeLen: 10,
            nonStrokeLen: 15,
            animation: 1 * 1,
          }}
          // animateDrawing={true}
          color="#92D0F0"
          gridBreak="30px"
          path="grid"
          //   startAnchor={"top"}
          showHead={false}
          start={ref4} //can be react ref
          end={ref1} //or an id
        />
      </Xwrapper>
    </Box>
  );
};

export default Sch;
