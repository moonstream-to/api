import React from "react";
import { Box } from "@chakra-ui/react";
import { getLayout as getSiteLayout } from "./AppLayout";

const AccountLayout = (props) => {
  return (
    <Box h="100%" className="ScrollableWrapper" width="100%">
      <Box h="100%" className="Scrollable">
        <Box w="100%" px="7%" pb="10rem">
          {props.children}
        </Box>
      </Box>
    </Box>
  );
};

export const getLayout = (page) =>
  getSiteLayout(<AccountLayout>{page}</AccountLayout>);

export default AccountLayout;
