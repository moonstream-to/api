import React, { useContext } from "react";
import { Box, Button, Progress, ButtonGroup } from "@chakra-ui/react";
import _ from "lodash";
import UIContext from "../core/providers/UIProvider/context";
const StepProgress = ({
  numSteps,
  currentStep,
  colorScheme,
  buttonCallback,
  buttonTitles,
}) => {
  const ui = useContext(UIContext);
  return (
    <Box w="100%" h="auto" pos="relative">
      <ButtonGroup
        display="inline-flex"
        flexDirection="row"
        justifyContent="space-between"
        w="100%"
        m={0}
        p={0}
        spacing={0}
      >
        {_.times(numSteps, (i) => {
          const setActive = i === parseInt(currentStep) ? true : false;
          return (
            <Button
              key={`${i}-progress-steps`}
              size={ui.isMobileView ? "md" : "sm"}
              borderRadius={ui.isMobileView ? "full" : "md"}
              // size="sm"
              //   bgColor={`${colorScheme}.200`}
              _active={{ bgColor: `${colorScheme}.1200` }}
              zIndex={1}
              m={0}
              colorScheme={colorScheme}
              isActive={setActive}
              onClick={() => buttonCallback(i)}
            >
              {ui.isMobileView && i + 1}
              {!ui.isMobileView && buttonTitles[i]}
            </Button>
          );
        })}
      </ButtonGroup>
      <Progress
        position="absolute"
        top="50%"
        transform="translateY(-50%)"
        h={2}
        w="full"
        // hasStripe
        // isAnimated
        max={numSteps - 1}
        min={0}
        value={currentStep}
      />
      {/* <Flex
        h="1rem"
        flexGrow={1}
        flexBasis="10px"
        backgroundColor={`${colorScheme}.300`}
      /> */}
    </Box>
  );
};

export default StepProgress;
