import { React, useState, useEffect } from "react";
import { Text } from "@chakra-ui/react";

const LoadingDots = (props) => {
  const [dotsNum, setDots] = useState(0);
  useEffect(() => {
    var dotInterval;
    if (props.isActive) {
      dotInterval = setInterval(() => {
        setDots(dotsNum === 3 ? 0 : dotsNum + 1);
      }, 300);
    }
    return () => clearInterval(dotInterval);
  }, [dotsNum, setDots, props.isActive]);

  let dots = dotsNum === 0 ? "" : ".".repeat(dotsNum);

  return (
    <Text
      fontSize={props.fontSize}
      textColor={props.textColor}
      py={props.py}
      px={props.px}
    >
      {props.children}
      {dots}
    </Text>
  );
};

export default LoadingDots;
