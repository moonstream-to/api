import React, { useEffect, useState, useRef } from "react";
import { Stack, Container, chakra } from "@chakra-ui/react";

const RangeSelector_ = ({
  className,
  ranges,
  onChange,
  initialRange,
  size,
}) => {
  const [range, setRange] = useState(initialRange ?? ranges[0]);
  const isFirstRun = useRef(true);

  useEffect(() => {
    if (isFirstRun.current) {
      isFirstRun.current = false;
    } else {
      onChange(range);
    }
  }, [range, onChange]);

  return (
    <Stack direction="row" className={className} h="min-content">
      {ranges.map((item, idx) => {
        const isActive = item === range ? true : false;
        return (
          <Container
            key={`date-range-${className}-${idx}`}
            bgColor={isActive ? "orange.900" : "blue.50"}
            color={!isActive ? "blue.900" : "blue.50"}
            boxShadow="sm"
            borderRadius="md"
            fontSize={size}
            fontWeight="600"
            onClick={() => setRange(item)}
            _hover={{
              bgColor: isActive ? "orange.900" : "orange.50",
            }}
            cursor="pointer"
            py="2px"
          >
            {item}
          </Container>
        );
      })}
    </Stack>
  );
};

const RangeSelector = chakra(RangeSelector_);

export default RangeSelector;
