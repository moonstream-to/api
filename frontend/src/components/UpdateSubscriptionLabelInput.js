import React, { useContext, useState, useEffect, useRef } from "react";
import { Button, Input } from "@chakra-ui/react";
import OverlayContext from "../core/providers/OverlayProvider/context";
import { MODAL_TYPES } from "../core/providers/OverlayProvider/constants";
import { useSubscriptions } from "../core/hooks";

const MobileFiledInput = ({
  onChange,
  initialValue,
  cancelText,
  submitText,
  id,
}) => {
  const { updateSubscription } = useSubscriptions();
  const isLoading = updateSubscription.isLoading;
  const [value, setValue] = useState(initialValue);
  const updateCallback = () => {
    const data = { id: id };
    value && (data.label = value);
    updateSubscription.mutate(data);
  };
  const [wasSubmitted, setWasSubmitted] = useState(false);
  console.log("MobileFiledInput", isLoading, wasSubmitted);
  const inputRef = useRef();
  const handleChange = (e) => {
    setValue(e.target.value);
    onChange && onChange(e);
  };

  const overlay = useContext(OverlayContext);
  const handleSubmit = (e) => {
    e.preventDefault();
    updateCallback({});
  };

  useEffect(() => {
    if (isLoading) {
      setWasSubmitted(true);
    }
  }, [isLoading]);

  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, []);

  useEffect(() => {
    if (!isLoading && wasSubmitted) {
      overlay.toggleModal({ type: MODAL_TYPES.OFF });
      setWasSubmitted(false);
    }
  }, [isLoading, overlay, wasSubmitted]);

  return (
    <>
      <Input
        variant="bw"
        ref={inputRef}
        type="text"
        value={value}
        onChange={handleChange}
        placeholder="Enter a value"
      />
      <Button
        colorScheme="green"
        onClick={(e) => handleSubmit(e)}
        isLoading={isLoading}
      >
        {submitText}
      </Button>
      <Button
        isDisabled={isLoading}
        onClick={() => overlay.toggleModal({ type: MODAL_TYPES.OFF })}
        colorScheme="blue"
      >
        {cancelText}
      </Button>
    </>
  );
};

export default MobileFiledInput;
