import React, { useContext, useEffect, useState } from "react";
import {
  chakra,
  FormLabel,
  Stack,
  Button,
  Spinner,
  Accordion,
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  AccordionIcon,
  Box,
  IconButton,
  Text,
} from "@chakra-ui/react";
import { useSubscriptions } from "../core/hooks";
import color from "color";
import OverlayContext from "../core/providers/OverlayProvider/context";
import { MODAL_TYPES } from "../core/providers/OverlayProvider/constants";
import CheckboxABI from "./CheckboxABI";
import AutoCompleter from "./AutoCompleter";
import CheckboxGrouped from "./CheckboxGrouped";
import { GENERIC_METRICS } from "../core/constants";
import UIContext from "../core/providers/UIProvider/context";
import {
  DASHBOARD_UPDATE_ACTIONS,
  DASHBOARD_CONFIGURE_SETTING_SCOPES,
} from "../core/constants";
import { BiTrash } from "react-icons/bi";

const NewDashboardChart = () => {
  const overlay = useContext(OverlayContext);
  const ui = useContext(UIContext);

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
    !item.subscription_type_id.includes("_whalewatch") &&
    (!inputValue ||
      item.address.toUpperCase().includes(inputValue.toUpperCase()) ||
      item.label.toUpperCase().includes(inputValue.toUpperCase()));

  console.log("ui.dashboardUpdate", ui.dashboardUpdate);
  return (
    <Stack spacing="24px" pb="100px">
      {ui.dashboardUpdate.subscription_settings.length > 0 && (
        <>
          <FormLabel pb={0}>Subscriptions:</FormLabel>
          <Accordion allowToggle allowMultiple defaultIndex={[0]}>
            {ui.dashboardUpdate.subscription_settings.map(
              (subscribedItem, idx) => {
                const subscriptionItemFromCache =
                  subscriptionsCache.data.subscriptions.find(
                    (subscription) =>
                      subscription.id === subscribedItem?.subscription_id
                  );
                if (
                  !subscriptionItemFromCache &&
                  subscribedItem?.subscription_id
                ) {
                  ui.dispatchDashboardUpdate({
                    type: DASHBOARD_UPDATE_ACTIONS.DROP_SUBSCRIPTION,
                    payload: {
                      subscriptionId: subscribedItem.subscription_id,
                    },
                  });
                }
                return (
                  <AccordionItem pt="5px" key={`new-chart-component-${idx}`}>
                    {subscribedItem?.subscription_id &&
                      subscriptionItemFromCache && (
                        <>
                          <h2>
                            <AccordionButton>
                              <Box flex="1" textAlign="left">
                                <FormLabel>{`${subscriptionItemFromCache.label} (${subscriptionItemFromCache.address})`}</FormLabel>
                              </Box>
                              <AccordionIcon />
                            </AccordionButton>
                          </h2>

                          <AccordionPanel pb={4}>
                            <Stack>
                              {subscribedItem?.subscription_id && (
                                <Stack spacing={1}>
                                  <IconButton
                                    icon={<BiTrash />}
                                    variant="ghost"
                                    colorScheme="red"
                                    size="sm"
                                    onClick={() =>
                                      ui.dispatchDashboardUpdate({
                                        type: DASHBOARD_UPDATE_ACTIONS.DROP_SUBSCRIPTION,
                                        payload: {
                                          subscriptionId:
                                            subscribedItem.subscription_id,
                                        },
                                      })
                                    }
                                  />
                                  <FormLabel pb={0}>Metric:</FormLabel>
                                  <CheckboxGrouped
                                    groupName="generic metrics:"
                                    getName={(item) => item}
                                    list={GENERIC_METRICS}
                                    isItemChecked={(item) =>
                                      subscribedItem.generic.some(
                                        (subscribedGenericItem) =>
                                          subscribedGenericItem.name === item
                                      )
                                    }
                                    isAllChecked={GENERIC_METRICS.some((item) =>
                                      subscribedItem.generic.some(
                                        (subscribedGenericItem) =>
                                          subscribedGenericItem.name === item
                                      )
                                    )}
                                    isIndeterminate={GENERIC_METRICS.some(
                                      (item) =>
                                        subscribedItem.generic.some(
                                          (subscribedGenericItem) =>
                                            subscribedGenericItem.name == item
                                        )
                                    )}
                                    setItemChecked={(item, isChecked) =>
                                      ui.dispatchDashboardUpdate({
                                        type: isChecked
                                          ? DASHBOARD_UPDATE_ACTIONS.APPEND_METRIC
                                          : DASHBOARD_UPDATE_ACTIONS.DROP_METRIC,
                                        scope:
                                          DASHBOARD_CONFIGURE_SETTING_SCOPES.METRIC_NAME,
                                        payload: {
                                          subscriptionId:
                                            subscribedItem.subscription_id,
                                          data: item,
                                          propertyName: "generic",
                                        },
                                      })
                                    }
                                    setAll={(isChecked) =>
                                      ui.dispatchDashboardUpdate({
                                        type: isChecked
                                          ? DASHBOARD_UPDATE_ACTIONS.APPEND_METRIC
                                          : DASHBOARD_UPDATE_ACTIONS.DROP_METRIC,
                                        scope:
                                          DASHBOARD_CONFIGURE_SETTING_SCOPES.METRICS_ARRAY,
                                        payload: {
                                          subscriptionId:
                                            subscribedItem.subscription_id,
                                          data: GENERIC_METRICS.map(
                                            (genericMetricName) => {
                                              return {
                                                name: genericMetricName,
                                              };
                                            }
                                          ),
                                          propertyName: "generic",
                                        },
                                      })
                                    }
                                  />

                                  <CheckboxABI
                                    subscriptionId={
                                      subscribedItem.subscription_id
                                    }
                                    state={subscribedItem}
                                    idx={idx}
                                  />
                                </Stack>
                              )}
                            </Stack>
                          </AccordionPanel>
                        </>
                      )}
                    {subscribedItem?.subscription_id === undefined &&
                      !subscriptionItemFromCache && (
                        <>
                          <AutoCompleter
                            initialIsOpen={true}
                            itemIdx={
                              ui.dashboardUpdate.subscription_settings.length
                            }
                            pickerItems={pickerItems.filter(
                              (pickerItem) =>
                                !ui.dashboardUpdate.subscription_settings.some(
                                  (subscriptiponSetting) =>
                                    pickerItem.id ===
                                    subscriptiponSetting.subscription_id
                                ) && pickerItem.abi === "True"
                            )}
                            itemToString={(item) => item?.label}
                            onSelect={(selectedItem) => {
                              ui.dispatchDashboardUpdate({
                                type: DASHBOARD_UPDATE_ACTIONS.OVERRIDE_SUBSCRIPTION,
                                payload: {
                                  subscriptionId: selectedItem.id,
                                  index: idx,
                                },
                              });
                            }}
                            getLeftAddonColor={(item) =>
                              item?.color ?? "inherit"
                            }
                            getLabelColor={(item) =>
                              item?.color ? color(item.color) : undefined
                            }
                            placeholder="Select subcription"
                            getDefaultValue={(item) =>
                              item?.label ? item.label : ""
                            }
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
                              return (
                                <Stack cursor="pointer" direction="row">
                                  <chakra.span whiteSpace="nowrap">
                                    {item.label}
                                  </chakra.span>
                                  <Text
                                    fontSize="md"
                                    color={item.abi ? "white" : "gray"}
                                  >
                                    ABI
                                  </Text>
                                  <Text
                                    isTruncated
                                    fontSize="md"
                                    placeSelf="self-center"
                                  >
                                    {item.address}
                                  </Text>
                                </Stack>
                              );
                            }}
                          />
                          <Button
                            onClick={() => {
                              ui.dispatchDashboardUpdate({
                                type: DASHBOARD_UPDATE_ACTIONS.DROP_SUBSCRIPTION,
                                payload: {
                                  subscriptionId: undefined,
                                },
                              });
                            }}
                            colorScheme="blue"
                            variant="outline"
                          >
                            Remove
                          </Button>
                        </>
                      )}
                  </AccordionItem>
                );
              }
            )}
          </Accordion>
        </>
      )}

      <Button
        variant="plainOrange"
        fontSize="md"
        size="md"
        onClick={() =>
          ui.dispatchDashboardUpdate({
            type: DASHBOARD_UPDATE_ACTIONS.APPEND_SUBSCRIPTION,
            payload: {
              subscriptionId: undefined,
            },
          })
        }
      >
        Add subscription to dashboard:
      </Button>
    </Stack>
  );
};

const ChakraNewDashboardChart = chakra(NewDashboardChart);

export default ChakraNewDashboardChart;
