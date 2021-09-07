import React from "react";
import { ChakraProvider } from "@chakra-ui/react";
import theme from "./Theme/theme";
import {
  AnalyticsProvider,
  UserProvider,
  ModalProvider,
  UIProvider,
} from "./core/providers";
import { StripeProvider } from "./core/providers/StripeProvider";

const AppContext = (props) => {
  return (
    <UserProvider>
      <ModalProvider>
        <StripeProvider>
          <ChakraProvider theme={theme}>
            <UIProvider>
              <AnalyticsProvider>{props.children}</AnalyticsProvider>
            </UIProvider>
          </ChakraProvider>
        </StripeProvider>
      </ModalProvider>
    </UserProvider>
  );
};

export default AppContext;
