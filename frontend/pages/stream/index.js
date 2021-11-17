import React, { useContext, useEffect } from "react";
import { getLayout } from "../../src/layouts/EntriesLayout";
import StreamEntryDetails from "../../src/components/SteamEntryDetails";
import UIContext from "../../src/core/providers/UIProvider/context";
import {
  Box,
  Heading,
  Text,
  Stack,
  UnorderedList,
  ListItem,
} from "@chakra-ui/react";
import RouteButton from "../../src/components/RouteButton";
const Entry = () => {
  console.count("render stream!");
  const ui = useContext(UIContext);

  useEffect(() => {
    if (typeof window !== "undefined") {
      if (ui?.currentTransaction) {
        document.title = `Stream details: ${ui.currentTransaction.hash}`;
      } else {
        document.title = `Stream`;
      }
    }
  }, [ui?.currentTransaction]);

  if (ui?.currentTransaction) {
    return <StreamEntryDetails />;
  } else
    return (
      <Box px="7%" pt={12}>
        <>
          <Stack direction="column">
            <Heading>Stream view</Heading>
            <Text>
              In this view you can follow events that happen on your subscribed
              addresses
            </Text>
            <UnorderedList pl={4}>
              <ListItem>
                Click filter icon on right top corner to filter by specific
                address across your subscriptions
              </ListItem>
              <ListItem>
                On event cards you can click at right corner to see detailed
                view!
              </ListItem>
              <ListItem>
                For any adress of interest here you can copy it and subscribe at
                subscription screen
              </ListItem>
            </UnorderedList>
            <RouteButton
              variant="solid"
              size="md"
              colorScheme="green"
              href="/welcome"
            >
              Learn how to use moonstream
            </RouteButton>
          </Stack>
        </>
      </Box>
    );
};
Entry.getLayout = getLayout;
export default Entry;
