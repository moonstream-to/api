import React, { useContext, useEffect } from "react";
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
} from "@chakra-ui/react";
import { CheckCircleIcon } from "@chakra-ui/icons";
import { useStorage, useSubscriptions } from "../core/hooks";
import Downshift from "downshift";
import color from "color";
import OverlayContext from "../core/providers/OverlayProvider/context";
import { MODAL_TYPES } from "../core/providers/OverlayProvider/constants";
import UIContext from "../core/providers/UIProvider/context";

const NewDashboardElement = (props) => {
  const ui = useContext(UIContext);
  const overlay = useContext(OverlayContext);
  const [newDashboardForm, setNewDashboardForm] = useStorage(
    sessionStorage,
    "new_dashboard",
    {
      name: "",
      subscriptions: [
        {
          label: "",
          abi: false,
          subscription_id: null,
          isMethods: false,
          isEvents: false,
          generic: {
            transactions: {
              in: false,
              out: false,
            },
            value: {
              in: false,
              out: false,
              balance: false,
            },
          },
        },
      ],
    }
  );

  const subscriptions = useSubscriptions();

  const [pickerItems, setPickerItems] = React.useState(
    subscriptions.subscriptionsCache.data?.subscriptions
  );

  useEffect(() => {
    newDashboardForm.subscriptions.forEach((element, idx) => {
      const subscription =
        subscriptions.subscriptionsCache.data?.subscriptions.find(
          (subscription_item) =>
            element.subscription_id === subscription_item.id
        );

      if (
        element.subscription_id &&
        subscription &&
        newDashboardForm.subscriptions[idx].abi !== subscription?.abi
      ) {
        const newestDashboardForm = { ...newDashboardForm };
        newestDashboardForm.subscriptions[idx].abi = subscription.abi;
        setNewDashboardForm(newestDashboardForm);
      }
    });
  }, [
    subscriptions.subscriptionsCache.data,
    newDashboardForm,
    setNewDashboardForm,
  ]);

  useEffect(() => {
    if (!subscriptions.subscriptionsCache.isLoading) {
      const massaged = subscriptions.subscriptionsCache.data?.subscriptions.map(
        (item) => {
          return { value: item.address, ...item };
        }
      );
      setPickerItems(massaged);
    }
  }, [
    subscriptions.subscriptionsCache.data,
    subscriptions.subscriptionsCache.isLoading,
  ]);

  const filterFn = (item, inputValue) =>
    (item.subscription_type_id === "ethereum_blockchain" ||
      item.subscription_type_id === "polygon_blockchain") &&
    (!inputValue ||
      item.address.toUpperCase().includes(inputValue.toUpperCase()) ||
      item.label.toUpperCase().includes(inputValue.toUpperCase()));

  return (
    <>
      <Stack spacing="24px"></Stack>
    </>
  );
};

const ChakraNewDashboard = chakra(NewDashboardElement);

export default ChakraNewDashboard;
