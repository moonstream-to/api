import React, { useEffect } from "react";
import { Spinner } from "@chakra-ui/react";
import { useToast } from "../core/hooks";
import HubspotForm from "react-hubspot-form";
import { MODAL_TYPES } from "../core/providers/OverlayProvider/constants";

const RequestIntegration = ({ toggleModal, formId }) => {
  const toast = useToast();

  useEffect(() => {
    function handler(event) {
      if (
        event.data.type === "hsFormCallback" &&
        event.data.eventName === "onFormSubmitted"
      ) {
        if (event.data.id === formId) {
          toggleModal({ type: MODAL_TYPES.OFF });
          toast("Request sent", "success");
        }
      }
    }

    window.addEventListener("message", handler);
    return () => {
      window.removeEventListener("message", handler);
    };
    // eslint-disable-next-line
  }, [toast, toggleModal]);

  return (
    <HubspotForm
      region="na1"
      portalId="8018701"
      formId={formId}
      loading={<Spinner colorScheme="blue" speed="1s" />}
    />
  );
};

export default RequestIntegration;
