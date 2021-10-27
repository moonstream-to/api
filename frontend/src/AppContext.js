import React from "react";
import { ChakraProvider } from "@chakra-ui/react";
import theme from "./Theme/theme";
import {
  AnalyticsProvider,
  UserProvider,
  UIProvider,
  DataProvider,
  OverlayProvider,
} from "./core/providers";
import { StripeProvider } from "./core/providers/StripeProvider";

const AppContext = (props) => {
  return (
    <UserProvider>
      <StripeProvider>
        <ChakraProvider theme={theme}>
          <DataProvider>
            <UIProvider>
              <OverlayProvider>
                <AnalyticsProvider>{props.children}</AnalyticsProvider>
              </OverlayProvider>
            </UIProvider>
          </DataProvider>
        </ChakraProvider>
      </StripeProvider>
    </UserProvider>
  );
};

export default AppContext;
