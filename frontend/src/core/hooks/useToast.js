import { jsx } from "@emotion/react";
import { useToast as useChakraToast, Box } from "@chakra-ui/react";
import { useCallback } from "react";
import { useAnalytics } from ".";

const useToast = () => {
  const chakraToast = useChakraToast();
  const analytics = useAnalytics();

  const toast = useCallback(
    (message, type) => {
      if (analytics.isLoaded && type === "error") {
        analytics.mixpanel.track(
          `${analytics.MIXPANEL_EVENTS.TOAST_ERROR_DISPLAYED}`,
          {
            status: message?.response?.status,
            detail: message?.response?.data.detail,
          }
        );
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
    [chakraToast, analytics]
  );

  return toast;
};

export default useToast;
