import React, { useEffect } from "react";
import { Heading, Spinner } from "@chakra-ui/react";
import Modal from "./Modal";
import { useToast } from "../core/hooks";
import HubspotForm from "react-hubspot-form";

const RequestIntegration = ({ toggleModal, title, formId }) => {
  const toast = useToast();

  useEffect(() => {
    function handler(event) {
      if (
        event.data.type === "hsFormCallback" &&
        event.data.eventName === "onFormSubmitted"
      ) {
        if (event.data.id === formId) {
          toggleModal(null);
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
    <Modal onClose={() => toggleModal(null)}>
      <Heading my={2} as="h2" fontSize={["xl", "3xl"]}>
        {title}
      </Heading>
      <HubspotForm
        region="na1"
        portalId="8018701"
        formId={formId}
        loading={<Spinner colorScheme="blue" speed="1s" />}
      />
    </Modal>
  );
};

export default RequestIntegration;
