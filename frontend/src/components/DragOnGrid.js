import React, { useEffect, useState } from "react";
import Draggable from "react-draggable";
import { useXarrow } from "react-xarrows";
const DragOnGrid = React.forwardRef((props, ref) => {
  const updateXarrow = useXarrow();

  const [position, setPosition] = useState({
    x: props.defaultPosition.x * props.gridStep,
    y: props.defaultPosition.y * props.gridStep,
  });
  const [cellSize, setCellSize] = useState(props.gridStep);

  useEffect(() => {
    setPosition({
      x: (position.x * props.gridStep) / cellSize,
      y: (position.y * props.gridStep) / cellSize,
    });
    setCellSize(props.gridStep);
    //eslint-disable-next-line
  }, [props.gridStep]);

  const handleDrag = (e, eData) => {
    setTimeout(() => {
      updateXarrow();
    }, 50);
    setPosition({ x: position.x + eData.deltaX, y: position.y + eData.deltaY });
  };

  return (
    <Draggable
      nodeRef={ref}
      axis="both"
      handle=".handle"
      position={{ ...position }}
      grid={[props.gridStep, props.gridStep]}
      scale={1}
      onDrag={handleDrag}
    >
      {props.children}
    </Draggable>
  );
});

export default DragOnGrid;
