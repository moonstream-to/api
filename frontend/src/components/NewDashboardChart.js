import React, { useContext, useEffect, useState } from "react";
import {
  chakra,
  FormLabel,
  Stack,
  Button,
  Badge,
  Spinner,
} from "@chakra-ui/react";
import { useSubscriptions } from "../core/hooks";
import color from "color";
import OverlayContext from "../core/providers/OverlayProvider/context";
import { MODAL_TYPES } from "../core/providers/OverlayProvider/constants";
import CheckboxABI from "./CheckboxABI";
import AutoCompleter from "./AutoCompleter";
import CheckboxGrouped from "./CheckboxGrouped";

const NewDashboardChart = ({ drawerState, setDrawerState }) => {
  const overlay = useContext(OverlayContext);

  const [pickerItems, setPickerItems] = useState();

  const { subscriptionsCache } = useSubscriptions();
  useEffect(() => {
    if (!subscriptionsCache.isLoading && subscriptionsCache.data) {
      const massaged = subscriptionsCache.data?.subscriptions.map((item) => {
        return { value: item.address, ...item };
      });
      setPickerItems(massaged);
    }
  }, [subscriptionsCache.isLoading, subscriptionsCache.data]);

  if (subscriptionsCache.isLoading || !pickerItems) return <Spinner />;

  const filterFn = (item, inputValue) =>
    (item.subscription_type_id === "ethereum_blockchain" ||
      item.subscription_type_id === "polygon_blockchain") &&
    (!inputValue ||
      item.address.toUpperCase().includes(inputValue.toUpperCase()) ||
      item.label.toUpperCase().includes(inputValue.toUpperCase()));

  return (
    <>
      <Stack spacing="24px">
        {drawerState.map((subscribedItem, idx) => {
          const setGeneric = (callbackFn) => {
            setDrawerState((currentDrawerState) => {
              const newDrawerState = [...currentDrawerState];
              newDrawerState[idx].generic = callbackFn(
                newDrawerState[idx].generic
              );
              return newDrawerState;
            });
          };
          const setDrawerAtHead = (arg) => {
            let newDrawerState = [...drawerState];
            if (typeof arg === "function") {
              newDrawerState[idx] = arg(newDrawerState[idx]);
            } else {
              newDrawerState[idx] = [...arg];
            }
            setDrawerState(newDrawerState);
          };
          return (
            <Stack key={`new-chart-component-${idx}`}>
              <FormLabel pb={0}>Subscription:</FormLabel>
              <AutoCompleter
                itemIdx={idx}
                pickerItems={pickerItems}
                initialSelectedItem={undefined}
                itemToString={(item) => item?.label}
                onSelect={(selectedItem) =>
                  setDrawerState((currentValue) => {
                    const newValue = [...currentValue];
                    newValue[idx] = {
                      subscription: selectedItem,
                      generic: {
                        transactions_in: {
                          value: "transactions_in",
                          name: "transactions in",
                          checked: false,
                        },
                        transactions_out: {
                          value: "transactions_out",
                          name: "transactions out",
                          checked: false,
                        },
                        value_in: {
                          value: "value_in",
                          name: "value in",
                          checked: false,
                        },
                        value_out: {
                          value: "value_out",
                          name: "value out",
                          checked: false,
                        },
                        balance: {
                          value: "balance",
                          name: "balance",
                          checked: false,
                        },
                      },
                      events: {},
                      methods: {},
                    };

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
              {subscribedItem?.subscription?.id && (
                <Stack spacing={1}>
                  <FormLabel pb={0}>Metric:</FormLabel>
                  <CheckboxGrouped
                    groupName="generic metrics:"
                    getName={(item) => item.name}
                    list={Object.values(drawerState[idx].generic)}
                    isItemChecked={(item) => item.checked}
                    isAllChecked={Object.values(drawerState[idx].generic).every(
                      (item) => !!item.checked
                    )}
                    isIndeterminate={
                      Object.values(drawerState[idx].generic).some(
                        (item) => item.checked
                      ) &&
                      !Object.values(drawerState[idx].generic).every(
                        (item) => item.checked
                      )
                    }
                    setItemChecked={(item, isChecked) =>
                      setGeneric((currentState) => {
                        const newState = { ...currentState };
                        newState[item.value].checked = isChecked;
                        return newState;
                      })
                    }
                    setAll={(isChecked) =>
                      setGeneric((currentState) => {
                        const newState = { ...currentState };
                        Object.keys(newState).forEach(
                          (key) => (newState[key].checked = isChecked)
                        );
                        return newState;
                      })
                    }
                  />

                  <CheckboxABI
                    subscriptionId={subscribedItem.subscription.id}
                    drawerState={drawerState[idx]}
                    setState={setDrawerAtHead}
                    idx={idx}
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
