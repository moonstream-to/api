import React, { useEffect } from "react";
import { chakra, Stack, Spinner } from "@chakra-ui/react";
import { useSubscription, usePresignedURL } from "../core/hooks";
import CheckboxGrouped from "./CheckboxGrouped";
import massageAbi from "../core/utils/massageAbi";

const SuggestABI = ({ subscriptionId, drawerState, setState }) => {
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

  const setFunctions = (arg) => {
    setState((currentHeadState) => {
      const newHeadState = { ...currentHeadState };
      if (typeof arg === "function") {
        newHeadState.methods = arg(newHeadState.methods);
      } else {
        newHeadState.methods = { ...arg };
      }
      return newHeadState;
    });
  };

  const setEvents = (arg) => {
    setState((currentHeadState) => {
      const newHeadState = { ...currentHeadState };
      if (typeof arg === "function") {
        newHeadState.events = arg(newHeadState.events);
      } else {
        newHeadState.events = { ...arg };
      }
      return newHeadState;
    });
  };

  useEffect(() => {
    if (data && !isLoading) {
      const { fnsObj, eventsObj } = massageAbi(data);
      setState((currentHeadState) => {
        const newHeadState = { ...currentHeadState };
        newHeadState.methods = fnsObj;
        newHeadState.events = eventsObj;
        return newHeadState;
      });
    }
    //eslint-disable-next-line
  }, [data, isLoading]);

  if (isLoading || !data) return <Spinner />;

  return (
    <>
      <Stack>
        <CheckboxGrouped
          groupName="events"
          list={Object.values(drawerState.events)}
          isItemChecked={(item) => item.checked}
          isAllChecked={Object.values(drawerState.events).every(
            (item) => !!item.checked
          )}
          isIndeterminate={
            Object.values(drawerState.events).some((item) => item.checked) &&
            !Object.values(drawerState.events).every((item) => item.checked)
          }
          setItemChecked={(item, isChecked) =>
            setEvents((currentState) => {
              const newState = { ...currentState };
              newState[item.signature].checked = isChecked;
              return newState;
            })
          }
          setAll={(isChecked) =>
            setEvents((currentEvents) => {
              const newEvents = { ...currentEvents };
              Object.keys(newEvents).forEach(
                (key) => (newEvents[key].checked = isChecked)
              );
              return newEvents;
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
          groupName="functions"
          list={Object.values(drawerState.methods)}
          isItemChecked={(item) => item.checked}
          isAllChecked={Object.values(drawerState.methods).every(
            (item) => !!item.checked
          )}
          isIndeterminate={
            Object.values(drawerState.methods).some((item) => item.checked) &&
            !Object.values(drawerState.methods).every((item) => item.checked)
          }
          setItemChecked={(item, isChecked) =>
            setFunctions((currentState) => {
              const newState = { ...currentState };
              newState[item.signature].checked = isChecked;
              return newState;
            })
          }
          setAll={(isChecked) =>
            setFunctions((currentFunctions) => {
              const newFunctions = { ...currentFunctions };
              Object.keys(newFunctions).forEach(
                (key) => (newFunctions[key].checked = isChecked)
              );
              return newFunctions;
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

{
  /* <Stack pl={6} spacing={0}>
{getEvents(pickerItems).map((event, idx) => {
  const pickedEvents = getEvents(pickedItems);
  return (
    <Stack
      px={2}
      key={v4()}
      direction="row"
      bgColor={idx % 2 == 0 ? "gray.50" : "gray.100"}
    >
      <Checkbox
        isChecked={pickedEvents.some(
          (pickedEvent) => pickedEvent.value === event.value
        )}
        onChange={() => {
          const changedIndex = pickedItems.findIndex(
            (pickedItem) =>
              event.type === "event" &&
              pickedItem.value === event.value
          );
          if (changedIndex === -1) {
            setPickedItems((currentlyPicked) => {
              const newPicked = [...currentlyPicked];
              newPicked.push(event);
              return newPicked;
            });
          } else {
            setPickedItems((currentlyPicked) => {
              const newPicked = [...currentlyPicked];
              newPicked.splice(changedIndex, 1);
              return newPicked;
            });
          }
        }}
      >
        {event.value}
      </Checkbox>
      <Spacer />
      {event.stateMutability === "view" && (
        <Badge variant="solid" colorScheme="orange" size="sm">
          View
        </Badge>
      )}
      {event.stateMutability === "payable" && (
        <Badge variant="solid" colorScheme="blue" size="sm">
          Payable
        </Badge>
      )}
      {event.stateMutability === "nonpayable" && (
        <Badge variant="solid" colorScheme="green" size="sm">
          Non-Payable
        </Badge>
      )}
    </Stack>
  );
})}
{pickerItems
  ?.filter((unfilteredItem) => unfilteredItem.type === "function")
  .map((item, idx) => {
    return (
      <Stack
        px={2}
        key={v4()}
        direction="row"
        bgColor={idx % 2 == 0 ? "gray.50" : "gray.100"}
      >
        <Checkbox
          isChecked={pickedItems.some(
            (pickedItem) =>
              item.type === "function" &&
              pickedItem.value === item.value
          )}
        >
          {item.value}
        </Checkbox>
        <Spacer />
        {item.stateMutability === "view" && (
          <Badge variant="solid" colorScheme="orange" size="sm">
            View
          </Badge>
        )}
        {item.stateMutability === "payable" && (
          <Badge variant="solid" colorScheme="blue" size="sm">
            Payable
          </Badge>
        )}
        {item.stateMutability === "nonpayable" && (
          <Badge variant="solid" colorScheme="green" size="sm">
            Non-Payable
          </Badge>
        )}
      </Stack>
    );
  })}
</Stack> */
}
