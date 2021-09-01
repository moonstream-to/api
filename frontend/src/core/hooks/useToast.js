import { useToast as useChakraToast, Box } from "@chakra-ui/react";
import React, { useCallback } from "react";
import mixpanel from "mixpanel-browser";
import { MIXPANEL_EVENTS } from "../providers/AnalyticsProvider/constants";

const useToast = () => {
  const chakraToast = useChakraToast();

  const toast = useCallback(
    (message, type) => {
      if (mixpanel.get_distinct_id() && type === "error") {
        mixpanel.track(`${MIXPANEL_EVENTS.TOAST_ERROR_DISPLAYED}`, {
          status: message?.response?.status,
          detail: message?.response?.data.detail,
        });
      }
      const background = type === "error" ? "unsafe.500" : "suggested.500";
      const userMessage =
        type === "error"
          ? message?.response
            ? `${message.response.data.detail}..`
            : message
            ? `Error:${message}`
            : "Something is very wrong"
          : message;

      chakraToast({
        position: "bottom",
        duration: 3000,
        render: () => (
          <Box
            shadow="rgba(0, 0, 0, 0.1) 0px 10px 15px -3px, rgba(0, 0, 0, 0.05) 0px 4px 6px -2px;"
            m={3}
            p={3}
            color="white.100"
            bg={background}
          >
            {userMessage}
          </Box>
        ),
      });
    },
    [chakraToast]
  );

  return toast;
};

export default useToast;
