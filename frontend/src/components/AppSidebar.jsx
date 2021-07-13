import { jsx } from "@emotion/react";
import { Box, Flex} from "@chakra-ui/react";
import React, { Fragment } from "react";

import LoadingDots from "./LoadingDots"

const AppSidebar = () => {
  if (false) {
    return (
      <LoadingDots
        fontSize="md"
        textColor="white"
        py={4}
        px={4}
        isActive={true}
      >
        Reticulating splines
      </LoadingDots>
    );
  }

  return (
    <Fragment>


      <Flex
        className="ScrollableWrapper"
        flexGrow={1}
        overflow="hidden"
        direction="column"
        pb={8}
      >
        <Box className="Scrollable" id="JournalList" overflowY="scroll">
        </Box>
      </Flex>
    </Fragment>
  );
};

export default AppSidebar;
