import Input from "../Input";

const filledVariant = (props) => {
  const input = Input.variants.filled(props);
  return {
    ...input,
    stepper: {
      border: "none",
    },
  };
};

const NumberInput = {
  parts: ["field", "stepper", "stepperGroup"],

  baseStyle: {
    field: {
      borderRadius: "sm",
    },
  },
  variants: {
    outline: Input.variants.outline,
    filled: filledVariant,
    flushed: Input.variants.flushed,
  },

  defaultProps: Input.defaultProps,
};

export default NumberInput;
