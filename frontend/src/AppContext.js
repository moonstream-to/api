import React from "react";
import { ChakraProvider } from "@chakra-ui/react";
import theme from "./Theme/theme";
import {
  AnalyticsProvider,
  UserProvider,
  ModalProvider,
  UIProvider,
  DataProvider,
} from "./core/providers";
import { StripeProvider } from "./core/providers/StripeProvider";

const AppContext = (props) => {
  return (
    <UserProvider>
      <StripeProvider>
        <ChakraProvider theme={theme}>
          <DataProvider>
            <UIProvider>
              <ModalProvider>
                <AnalyticsProvider>{props.children}</AnalyticsProvider>
              </ModalProvider>
            </UIProvider>
          </DataProvider>
        </ChakraProvider>
      </StripeProvider>
    </UserProvider>
  );
};

export default AppContext;
