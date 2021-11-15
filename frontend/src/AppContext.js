import React, { useEffect } from "react";
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
  useEffect(() => {
    const version = process.env.NEXT_PUBLIC_FRONTEND_VERSION;
    if (version) console.log(`Frontend version: ${version}`);
    else console.error("Moonstream Frontend version variable is not exported");
  }, []);
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
