import React, { useContext, useEffect, useState } from "react";
import {
  chakra,
  FormLabel,
  Input,
  Stack,
  InputGroup,
  Box,
  Button,
  Table,
  Th,
  Td,
  Tr,
  Thead,
  Tbody,
  Center,
  Checkbox,
  CloseButton,
  InputRightAddon,
  Badge,
  InputLeftAddon,
  Spinner,
  Heading,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  MenuGroup,
  MenuDivider,
  ButtonGroup,
  Text,
} from "@chakra-ui/react";
import { CheckCircleIcon } from "@chakra-ui/icons";
import { useSubscription, usePresignedURL } from "../core/hooks";
import Downshift from "downshift";
import color from "color";
import OverlayContext from "../core/providers/OverlayProvider/context";
import { MODAL_TYPES } from "../core/providers/OverlayProvider/constants";
import UIContext from "../core/providers/UIProvider/context";
import { v4 } from "uuid";
import AutoCompleter from "./AutoCompleter";
import { CHART_METRICS } from "../core/constants";

const SuggestABI = ({ subscriptionId, onSelect, stateContainer }) => {
  const ui = useContext(UIContext);
  const overlay = useContext(OverlayContext);

  const { subscriptionLinksCache } = useSubscription({
    id: subscriptionId,
  });

  const { data, isLoading } = usePresignedURL({
    url: subscriptionLinksCache?.data?.data?.url,
    isEnabled: true,
    id: subscriptionId,
    cacheType: "abi",
    requestNewURLCallback: subscriptionLinksCache.refetch,
  });

  const [pickerItems, setPickerItems] = React.useState();

  // useEffect(() => {
  //   newDashboardForm.subscriptions.forEach((element, idx) => {
  //     const subscription =
  //       subscriptions.subscriptionsCache.data?.subscriptions.find(
  //         (subscription_item) =>
  //           element.subscription_id === subscription_item.id
  //       );

  //     if (
  //       element.subscription_id &&
  //       subscription &&
  //       newDashboardForm.subscriptions[idx].abi !== subscription?.abi
  //     ) {
  //       const newestDashboardForm = { ...newDashboardForm };
  //       newestDashboardForm.subscriptions[idx].abi = subscription.abi;
  //       setNewDashboardForm(newestDashboardForm);
  //     }
  //   });
  // }, [
  //   subscriptions.subscriptionsCache.data,
  //   newDashboardForm,
  //   setNewDashboardForm,
  // ]);

  useEffect(() => {
    if (!isLoading) {
      const massaged = data?.map((item) => {
        return { value: item.name ?? item.type, ...item };
      });
      setPickerItems(
        massaged?.filter((item) => item.type === stateContainer.type)
      );
    }
  }, [data, isLoading, stateContainer]);

  const filterFn = (item, inputValue) =>
    !inputValue || item.value.toUpperCase().includes(inputValue.toUpperCase());

  if (isLoading || !pickerItems) return <Spinner />;

  console.log("pickerItems", pickerItems);

  return (
    <>
      <Stack spacing={1}>
        {stateContainer.type === CHART_METRICS.EVENTS && (
          <Stack>
            <FormLabel pb={0}>Event:</FormLabel>
            <AutoCompleter
              itemIdx={""}
              pickerItems={pickerItems.filter((item) => item.type === "event")}
              initialSelectedItem={stateContainer}
              itemToString={(item) => item.name}
              onSelect={onSelect}
              getLeftAddonColor={(item) => item?.color ?? "inherit"}
              getLabelColor={() => undefined}
              placeholder="Select metric"
              getDefaultValue={(item) => (item?.value ? item.value : "")}
              filterFn={filterFn}
              empyListCTA={() => (
                <Text alignSelf="center">No Events found {`>_<`}</Text>
              )}
              dropdownItem={(item) => {
                console.log("dropdownItem,", item);
                return (
                  <>
                    <chakra.span whiteSpace="nowrap">{item.value}</chakra.span>
                    <Badge isTruncated size="sm" placeSelf="self-end">
                      {item.type}
                    </Badge>
                  </>
                );
              }}
            />
          </Stack>
        )}
        {stateContainer.type === CHART_METRICS.FUNCTIONS && (
          <Stack>
            <FormLabel pb={0}>Function:</FormLabel>
            <AutoCompleter
              itemIdx={""}
              pickerItems={pickerItems.filter(
                (item) => item.type === "function"
              )}
              initialSelectedItem={stateContainer}
              itemToString={(item) => item.name}
              onSelect={onSelect}
              getLeftAddonColor={(item) => item?.color ?? "inherit"}
              getLabelColor={() => undefined}
              placeholder="Select metric"
              getDefaultValue={(item) => (item?.value ? item.value : "")}
              filterFn={filterFn}
              empyListCTA={() => (
                <Text alignSelf="center">No Functions found {`>_<`}</Text>
              )}
              dropdownItem={(item) => {
                console.log("dropdownItem,", item);
                return (
                  <>
                    <chakra.span whiteSpace="nowrap">{item.value}</chakra.span>
                    <Badge isTruncated size="sm" placeSelf="self-end">
                      {item.type}
                    </Badge>
                  </>
                );
              }}
            />
          </Stack>
        )}
        {stateContainer.type === CHART_METRICS.GENERIC && (
          <Stack>
            <FormLabel pb={0}>Balance:</FormLabel>
            <AutoCompleter
              itemIdx={""}
              pickerItems={pickerItems}
              initialSelectedItem={stateContainer}
              itemToString={(item) => item.name}
              onSelect={onSelect}
              getLeftAddonColor={(item) => item?.color ?? "inherit"}
              getLabelColor={() => undefined}
              placeholder="Select metric"
              getDefaultValue={(item) => (item?.value ? item.value : "")}
              filterFn={filterFn}
              empyListCTA={() => ""}
              dropdownItem={(item) => {
                console.log("dropdownItem,", item);
                return (
                  <>
                    <chakra.span whiteSpace="nowrap">{item.value}</chakra.span>
                    <Badge isTruncated size="sm" placeSelf="self-end">
                      {item.type}
                    </Badge>
                  </>
                );
              }}
            />
          </Stack>
        )}
      </Stack>
    </>
  );
};

const ChakraSuggestABI = chakra(SuggestABI);

export default ChakraSuggestABI;
