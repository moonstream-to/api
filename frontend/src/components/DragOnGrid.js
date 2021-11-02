import React from "react";
import Draggable from "react-draggable";
import { useXarrow } from "react-xarrows";
const DragOnGrid = React.forwardRef((props, ref) => {
  const updateXarrow = useXarrow();

  const handleDrag = (e) => {
    console.log(e);
    setTimeout(() => {
      updateXarrow();
    }, 50);
  };

  return (
    <Draggable
      nodeRef={ref}
      axis="both"
      handle=".handle"
      {...props}
      position={null}
      grid={[60, 60]}
      scale={1}
      onDrag={handleDrag}
      onStop={updateXarrow}
    >
      {props.children}
    </Draggable>
  );
});

export default DragOnGrid;
