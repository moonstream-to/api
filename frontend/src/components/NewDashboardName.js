import React, { useContext, useEffect, useState } from "react";
import {
  chakra,
  ButtonGroup,
  Button,
  Input,
  Stack,
  InputLeftAddon,
  InputGroup,
} from "@chakra-ui/react";
import OverlayContext from "../core/providers/OverlayProvider/context";
import {
  DRAWER_TYPES,
  MODAL_TYPES,
} from "../core/providers/OverlayProvider/constants";
import { useDashboard, useRouter } from "../core/hooks";
import {
  uniqueNamesGenerator,
  adjectives,
  colors,
  animals,
} from "unique-names-generator";
import UIContext from "../core/providers/UIProvider/context";
import { DASHBOARD_UPDATE_ACTIONS } from "../core/constants";

const NewDashboardName = (props) => {
  const overlay = useContext(OverlayContext);
  const { dispatchDashboardUpdate } = useContext(UIContext);
  const { createDashboard } = useDashboard();
  const [name, setName] = useState(props.initialName);
  const [placeholder] = useState(
    uniqueNamesGenerator({
      dictionaries: [adjectives, colors, animals],
      separator: `-`,
    }).toLocaleLowerCase()
  );

  const router = useRouter();
  useEffect(() => {
    if (createDashboard.isSuccess && createDashboard.data) {
      createDashboard.reset();
      dispatchDashboardUpdate({
        type: DASHBOARD_UPDATE_ACTIONS.RESET_TO_DEFAULT,
      });
      router.push({
        pathname: "/dashboard/[dashboardId]",
        query: { dashboardId: createDashboard.data.id },
      });
      overlay.toggleModal({ type: MODAL_TYPES.OFF, props: undefined });
      overlay.toggleDrawer({
        type: DRAWER_TYPES.NEW_DASHBOARD_ITEM,
        props: createDashboard.data.resource_data,
      });
    }
  }, [createDashboard, router, overlay, dispatchDashboardUpdate]);

  return (
    <>
      <Stack direction={["column", "row", null]}>
        <InputGroup border="1px solid white" borderRadius="7px">
          <InputLeftAddon bg="black.300">Name:</InputLeftAddon>
          <Input
            borderStyle="none none none"
            borderLeft="1px solid white"
            variant="bw"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder={placeholder}
          />
        </InputGroup>
      </Stack>
      <ButtonGroup size="sm" pt={4}>
        <Button
          colorScheme="red"
          onClick={() => {
            overlay.toggleModal({ type: MODAL_TYPES.OFF, props: undefined });
          }}
          isLoading={createDashboard.isLoading}
        >
          Cancel
        </Button>
        <Button
          isLoading={createDashboard.isLoading}
          colorScheme="green"
          onClick={() => {
            createDashboard.mutate({ name: name ?? placeholder });
          }}
        >
          Submit
        </Button>
      </ButtonGroup>
    </>
  );
};

const ChakraNewDashboardName = chakra(NewDashboardName);

export default ChakraNewDashboardName;
