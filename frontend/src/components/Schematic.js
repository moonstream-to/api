import React from "react";
import Draggable from "react-draggable";
import { Box, Container } from "@chakra-ui/react";
import { useXarrow } from "react-xarrows";
const Schematic = React.forwardRef(({ def }, ref) => {
  const updateXarrow = useXarrow();
  const eventLogger = (e, data) => {
    console.log("Event: ", e);
    console.log("Data: ", data);
  };

  const handleStart = (e) => {
    console.log(e);
  };

  const handleDrag = (e) => {
    console.log(e);
  };

  const handleStop = (e) => {
    console.log(e);
  };

  console.log("def", def);

  return (
    <Draggable
      nodeRef={ref}
      axis="both"
      handle=".handle"
      defaultPosition={{ ...def }}
      position={null}
      grid={[60, 60]}
      scale={1}
      onStart={updateXarrow}
      onDrag={updateXarrow}
      onStop={updateXarrow}
    >
      <Box ref={ref} className="handle" boxSize="60px" bg="red.900">
        hmm?
      </Box>
    </Draggable>
    // <Box ref={ref} className="handle" boxSize="60px" bg="red.900">
    //   hmm?
    // </Box>
  );
});

export default Schematic;
