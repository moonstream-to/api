import React, { useContext, useMemo, useState, useEffect } from "react";
import { useQuery } from "react-query";
import { useToast } from "../core/hooks";
import { chakra, Stack, Spinner } from "@chakra-ui/react";
import { queryCacheProps } from "../core/hooks/hookCommon";
import { SubscriptionsService } from "../core/services";
import CheckboxGrouped from "./CheckboxGrouped";
import UIContext from "../core/providers/UIProvider/context";
import UserContext from "../core/providers/UserProvider/context";
import {
  DASHBOARD_CONFIGURE_SETTING_SCOPES,
  DASHBOARD_UPDATE_ACTIONS,
} from "../core/constants";

const SuggestABI = ({ subscriptionId, state }) => {

  const toast = useToast();
  const user = useContext(UserContext);


  const subscriptionLinksCache = useQuery(
    ["dashboardLinks", subscriptionId],
    SubscriptionsService.getSubscriptionABI(subscriptionId),
    {
      ...queryCacheProps,
      onError: (error) => {
        toast(error, "error");
      },
      enabled: !!user && !!subscriptionId,
    }
  );


  const { dispatchDashboardUpdate } = useContext(UIContext);

  const [abi, setAbi] = useState(null);

  useEffect(() => {
    if (subscriptionLinksCache?.data?.data?.abi) {
      setAbi(JSON.parse(subscriptionLinksCache?.data?.data?.abi));
    }
  }, [subscriptionLinksCache.data]);




  const abiEvents = useMemo(
    () => abi && abi.filter((abiItem) => abiItem.type === "event"),
    [abi]
  );
  const abiMethods = useMemo(
    () => abi && abi.filter((abiItem) => abiItem.type === "function"),
    [abi]
  );


  // Waiting for abi to be available
  if (!abi) return <Spinner />;

  return (
    <>
      <Stack>
        <CheckboxGrouped
          groupName="events"
          list={abiEvents}
          isItemChecked={(item) => {
            return state.events.some((event) => event.name === item.name);
          }}
          isAllChecked={abiEvents.every((abiEvent) => {
            return state.events.some((event) => abiEvent.name === event.name);
          })}
          isIndeterminate={state.events.some((event) =>
            abiEvents.some((abiEvent) => abiEvent.name === event.name)
          )}
          setItemChecked={(item, isChecked) =>
            dispatchDashboardUpdate({
              type: isChecked
                ? DASHBOARD_UPDATE_ACTIONS.APPEND_METRIC
                : DASHBOARD_UPDATE_ACTIONS.DROP_METRIC,
              scope: DASHBOARD_CONFIGURE_SETTING_SCOPES.METRIC_NAME,
              payload: {
                subscriptionId: subscriptionId,
                data: item.name,
                propertyName: "events",
              },
            })
          }
          setAll={(isChecked) =>
            dispatchDashboardUpdate({
              type: isChecked
                ? DASHBOARD_UPDATE_ACTIONS.APPEND_METRIC
                : DASHBOARD_UPDATE_ACTIONS.DROP_METRIC,
              scope: DASHBOARD_CONFIGURE_SETTING_SCOPES.METRICS_ARRAY,
              payload: {
                subscriptionId: subscriptionId,
                data: abiEvents.map((abiEvent) => {
                  return { name: abiEvent.name };
                }),
                propertyName: "events",
              },
            })
          }
          getName={(item) => {
            const args = item.inputs.map((input) => input.internalType);
            let name = item.name + ` (`;
            name += args.map((argument, idx) =>
              idx === 0 ? `${argument}` : ` ${argument}`
            );
            name += `)`;
            return name;
          }}
        />
        <CheckboxGrouped
          groupName="methods"
          list={abiMethods}
          isItemChecked={(item) =>
            state.methods.some((fn) => fn.name === item.name)
          }
          isAllChecked={abiMethods.every((abiMethod) => {
            return state.methods.some((fn) => abiMethod.name === fn.name);
          })}
          isIndeterminate={state.methods.some((fn) =>
            abiMethods.some((abiMethod) => abiMethod.name === fn.name)
          )}
          setItemChecked={(item, isChecked) =>
            dispatchDashboardUpdate({
              type: isChecked
                ? DASHBOARD_UPDATE_ACTIONS.APPEND_METRIC
                : DASHBOARD_UPDATE_ACTIONS.DROP_METRIC,
              scope: DASHBOARD_CONFIGURE_SETTING_SCOPES.METRIC_NAME,
              payload: {
                subscriptionId: subscriptionId,
                data: item.name,
                propertyName: "methods",
              },
            })
          }
          setAll={(isChecked) =>
            dispatchDashboardUpdate({
              type: isChecked
                ? DASHBOARD_UPDATE_ACTIONS.APPEND_METRIC
                : DASHBOARD_UPDATE_ACTIONS.DROP_METRIC,
              scope: DASHBOARD_CONFIGURE_SETTING_SCOPES.METRICS_ARRAY,
              payload: {
                subscriptionId: subscriptionId,
                data: abiMethods.map((abiMethod) => {
                  return { name: abiMethod.name };
                }),
                propertyName: "methods",
              },
            })
          }
          getName={(item) => {
            const args = item.inputs.map((input) => input.internalType);
            let name = item.name + ` (`;
            name += args.map((argument, idx) =>
              idx === 0 ? `${argument}` : ` ${argument}`
            );
            name += `)`;
            return name;
          }}
        />
      </Stack>
    </>
  );
};

const ChakraSuggestABI = chakra(SuggestABI);

export default ChakraSuggestABI;
