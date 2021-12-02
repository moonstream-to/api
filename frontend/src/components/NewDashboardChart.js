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
  Heading,
  Spinner,
  Text,
  ButtonGroup,
} from "@chakra-ui/react";
import { CheckCircleIcon } from "@chakra-ui/icons";
import { useSubscriptions } from "../core/hooks";
import Downshift from "downshift";
import color from "color";
import OverlayContext from "../core/providers/OverlayProvider/context";
import { MODAL_TYPES } from "../core/providers/OverlayProvider/constants";
import UIContext from "../core/providers/UIProvider/context";
import SuggestABI from "./SuggestABI";
import { v4 } from "uuid";
import AutoCompleter from "./AutoCompleter";
import { CHART_METRICS } from "../core/constants";

const NewDashboardChart = (props) => {
  const [metric, setMetric] = useState();
  const ui = useContext(UIContext);
  const overlay = useContext(OverlayContext);
  const [newChartForm, setNewChartForm] = useState([
    {
      subscription: undefined, //subscription
      type: undefined, // generic | events | transactions
      name: undefined, // transactions_in | transactions_out | value_in | value_out | balance | abi.events.some() | abi.methods.some()
    },
  ]);

  const [pickerItems, setPickerItems] = useState();

  useEffect(() => {
    if (!subscriptionsCache.isLoading) {
      const massaged = subscriptionsCache.data?.subscriptions.map((item) => {
        return { value: item.address, ...item };
      });
      setPickerItems(massaged);
    }
  }, [subscriptionsCache]);

  const { subscriptionsCache } = useSubscriptions();

  if (subscriptionsCache.isLoading) return <Spinner />;
  console.log("newChartForm:", newChartForm);

  const filterFn = (item, inputValue) =>
    (item.subscription_type_id === "ethereum_blockchain" ||
      item.subscription_type_id === "polygon_blockchain") &&
    (!inputValue ||
      item.address.toUpperCase().includes(inputValue.toUpperCase()) ||
      item.label.toUpperCase().includes(inputValue.toUpperCase()));

  return (
    <>
      <Stack spacing="24px">
        {newChartForm.map((subscibedItem, idx) => {
          const onAbiSuggestionSelect = ({ type, value }) => {
            setNewChartForm((currentValue) => {
              const newValue = [...currentValue];
              newValue[idx].type = type;
              newValue[idx].name = value;
              return newValue;
            });
          };
          const onMetricSelect = ({ type, value }) => {
            setNewChartForm((currentValue) => {
              const newValue = [...currentValue];
              newValue[idx].type = type;
              newValue[idx].name = "";
              return newValue;
            });
          };
          return (
            <Stack key={v4()}>
              <FormLabel pb={0}>Subscription:</FormLabel>
              <AutoCompleter
                itemIdx={idx}
                pickerItems={pickerItems}
                initialSelectedItem={newChartForm[idx].subscription}
                itemToString={(item) => item.label}
                onSelect={(selectedItem) =>
                  setNewChartForm((currentValue) => {
                    const newValue = [...currentValue];
                    newValue[idx].subscription = selectedItem;
                    return newValue;
                  })
                }
                getLeftAddonColor={(item) => item?.color ?? "inherit"}
                getLabelColor={(item) =>
                  item?.color ? color(item.color) : undefined
                }
                placeholder="Select subcription"
                getDefaultValue={(item) => (item?.label ? item.label : "")}
                filterFn={filterFn}
                empyListCTA={(inputValue) => (
                  <Button
                    colorScheme="orange"
                    variant="outline"
                    size="sm"
                    fontSize="sm"
                    w="100%"
                    m={0}
                    isTruncated
                    onClick={() => {
                      overlay.toggleModal({
                        type: MODAL_TYPES.NEW_SUBSCRIPTON,
                        props: {
                          initialValue: inputValue,
                        },
                      });
                    }}
                  >
                    Subscribe to: {inputValue}{" "}
                  </Button>
                )}
                dropdownItem={(item) => {
                  console.log("dropdownItem,", item);
                  const badgeColor = color(`${item.color}`);
                  return (
                    <>
                      <chakra.span whiteSpace="nowrap">
                        {item.label}
                      </chakra.span>
                      <Badge
                        size="sm"
                        placeSelf="self-end"
                        colorScheme={item.abi ? "green" : "gray"}
                      >
                        ABI
                      </Badge>
                      <Badge
                        isTruncated
                        size="sm"
                        placeSelf="self-end"
                        bgColor={item.color}
                        color={
                          badgeColor.isDark()
                            ? badgeColor.lighten(100).hex()
                            : badgeColor.darken(0.6).hex()
                        }
                      >
                        {item.address}
                      </Badge>
                    </>
                  );
                }}
              />
              {subscibedItem?.subscription?.id && (
                <Stack spacing={1}>
                  <FormLabel pb={0}>Metric:</FormLabel>
                  <ButtonGroup spacing={0} display="flex">
                    <Button
                      flexGrow="1"
                      flexBasis="50px"
                      m={0}
                      colorScheme="orange"
                      bgColor="orange.600"
                      _active={{ bgColor: "orange.900" }}
                      borderRightRadius={0}
                      onClick={() =>
                        onMetricSelect({ type: CHART_METRICS.GENERIC })
                      }
                      isActive={
                        newChartForm[idx].type === CHART_METRICS.GENERIC
                      }
                    >
                      Balance
                    </Button>
                    <Button
                      m={0}
                      flexGrow="1"
                      flexBasis="50px"
                      borderRadius={0}
                      colorScheme="orange"
                      bgColor="orange.600"
                      _active={{ bgColor: "orange.900" }}
                      onClick={() =>
                        onMetricSelect({ type: CHART_METRICS.EVENTS })
                      }
                      isActive={newChartForm[idx].type === CHART_METRICS.EVENTS}
                    >
                      Events
                    </Button>
                    <Button
                      flexGrow="1"
                      flexBasis="50px"
                      m={0}
                      borderLeftRadius={0}
                      colorScheme="orange"
                      bgColor="orange.600"
                      _active={{ bgColor: "orange.900" }}
                      onClick={() =>
                        onMetricSelect({ type: CHART_METRICS.FUNCTIONS })
                      }
                      isActive={
                        newChartForm[idx].type === CHART_METRICS.FUNCTIONS
                      }
                    >
                      Functions
                    </Button>
                  </ButtonGroup>
                  <SuggestABI
                    stateContainer={newChartForm[idx]}
                    subscriptionId={subscibedItem.subscription.id}
                    onSelect={onAbiSuggestionSelect}
                  />
                </Stack>
              )}
            </Stack>
          );
        })}
      </Stack>
    </>
  );
};

const ChakraNewDashboardChart = chakra(NewDashboardChart);

export default ChakraNewDashboardChart;
