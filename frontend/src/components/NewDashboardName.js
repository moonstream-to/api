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

const NewDashboardName = (props) => {
  const overlay = useContext(OverlayContext);
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
  }, [createDashboard, router, overlay]);

  return (
    <>
      <Stack direction={["column", "row", null]}>
        <InputGroup>
          <InputLeftAddon>Name:</InputLeftAddon>
          <Input
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
