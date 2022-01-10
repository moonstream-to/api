import React, { useContext, useMemo } from "react";
import { chakra, Stack, Spinner } from "@chakra-ui/react";
import { useSubscription, usePresignedURL } from "../core/hooks";
import CheckboxGrouped from "./CheckboxGrouped";
import UIContext from "../core/providers/UIProvider/context";
import {
  DASHBOARD_CONFIGURE_SETTING_SCOPES,
  DASHBOARD_UPDATE_ACTIONS,
} from "../core/constants";

const SuggestABI = ({ subscriptionId, state }) => {
  const { subscriptionLinksCache } = useSubscription({
    id: subscriptionId,
  });

  const { dispatchDashboardUpdate } = useContext(UIContext);

  const { data, isLoading } = usePresignedURL({
    url: subscriptionLinksCache?.data?.data?.url,
    isEnabled: true,
    id: subscriptionId,
    cacheType: "abi",
    requestNewURLCallback: subscriptionLinksCache.refetch,
  });

  const abiEvents = useMemo(
    () => data && data.filter((abiItem) => abiItem.type === "event"),
    [data]
  );
  const abiMethods = useMemo(
    () => data && data.filter((abiItem) => abiItem.type === "function"),
    [data]
  );
  if (isLoading) return <Spinner />;
  if (!data) return "";

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
