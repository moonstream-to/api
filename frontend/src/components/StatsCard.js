import React, { useEffect, useState } from "react";
import { Stack, Text, chakra, Box, SimpleGrid } from "@chakra-ui/react";
import { TriangleDownIcon, TriangleUpIcon } from "@chakra-ui/icons";

const StatsCard_ = ({
  className,
  value,
  valueChange,
  label,
  netLabel,
  dimension,
  share,
  shareChange,
}) => {
  const [isValueIncrease, setIsValueIncrease] = useState(
    Number(valueChange) > 0 ? true : false
  );
  const [isShareIncrease, setIsShareIncrease] = useState(
    Number(shareChange) > 0 ? true : false
  );

  useEffect(() => {
    setIsValueIncrease(Number(valueChange) > 0 ? true : false);
  }, [valueChange]);

  useEffect(() => {
    setIsShareIncrease(Number(shareChange) > 0 ? true : false);
  }, [shareChange]);


  return (
    <Stack className={className}>
      <Box
        w="full"
        borderTopRadius="inherit"
        fontWeight="600"
        autoCapitalize
        bgColor="gray.200"
        px={4}
        textAlign="center"
      >
        {label}
      </Box>
      <SimpleGrid
        columns={2}
        justifyItems="center"
        textAlign="center"
        h="100%"
        alignContent="center"
      >
        <Box
          w="100%"
          fontSize="1.125rem"
          borderStyle="dashed"
          borderRightWidth="3px"
          borderRightColor="gray.300"
          //   alignItems="center"
          h="100%"
        >
          <Text>
            {dimension} {value}
          </Text>
        </Box>
        <Stack
          w="100%"
          direction="row"
          fontSize="1.125rem"
          placeContent="center"
          alignItems="center"
        >
          {isValueIncrease && <TriangleUpIcon color="suggested.900" />}
          {!isValueIncrease && <TriangleDownIcon color="unsafe.900" />}
          <Text textColor={isValueIncrease ? "suggested.900" : "unsafe.900"}>
            {Math.abs(valueChange) > 9999
              ? valueChange.toExponential(2)
              : Math.round((valueChange + Number.EPSILON) * 100) / 100}
            %
          </Text>
        </Stack>
        {share && shareChange && (
          <>
            <Text
              w="100%"
              borderTopWidth="3px"
              borderTopStyle="dashed"
              borderTopColor="gray.300"
              gridColumn="span 2"
              fontSize="0.825rem"
            >
              Total share in {netLabel}
            </Text>
            <Text>
              {(Math.round((share + Number.EPSILON) * 100) / 100).toFixed(2)}%
            </Text>
            <Stack direction="row" placeContent="center" alignItems="center">
              {isShareIncrease && <TriangleUpIcon color="suggested.900" />}
              {!isShareIncrease && <TriangleDownIcon color="unsafe.900" />}
              <Text
                textColor={isShareIncrease ? "suggested.900" : "unsafe.900"}
              >
                {(
                  Math.round((shareChange + Number.EPSILON) * 100) / 100
                ).toFixed(2)}
                %
              </Text>
            </Stack>
          </>
        )}
      </SimpleGrid>
    </Stack>
  );
};

const StatsCard = chakra(StatsCard_, {
  baseStyle: {
    boxShadow: "md",
    borderRadius: "lg",
    bgColor: "gray.100",
    w: "240px",
    minW: "240px",
  },
});

export default StatsCard;
