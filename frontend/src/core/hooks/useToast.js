import { useToast as useChakraToast } from "@chakra-ui/react";
import { useCallback } from "react";
import mixpanel from "mixpanel-browser";
import { MIXPANEL_EVENTS } from "../providers/AnalyticsProvider/constants";

const useToast = () => {
  const chakraToast = useChakraToast();

  const toast = useCallback(
    (message, type, title) => {
      const userTitle = title ?? message?.response?.statusText ?? type;

      const userMessage =
        message?.response?.data?.detail ?? typeof message === "string"
          ? message
          : userTitle === type
          ? ""
          : type;

      if (mixpanel.get_distinct_id() && type === "error") {
        mixpanel.track(`${MIXPANEL_EVENTS.TOAST_ERROR_DISPLAYED}`, {
          status: message?.response?.status,
          title: userTitle,
          detail: userMessage,
        });
      }

      chakraToast({
        id: `${userTitle}${userMessage}${type}`,
        position: "bottom",
        title: userTitle,
        description: userMessage,
        status: type,
        // duration: 3000,
      });
    },
    [chakraToast]
  );

  return toast;
};

export default useToast;
