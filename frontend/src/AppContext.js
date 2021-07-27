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
        <AnalyticsProvider>
          <StripeProvider>
            <ChakraProvider theme={theme}>
              <UIProvider>{props.children}</UIProvider>
            </ChakraProvider>
          </StripeProvider>
        </AnalyticsProvider>
      </ModalProvider>
    </UserProvider>
  );
};

export default AppContext;
