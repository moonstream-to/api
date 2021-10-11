import { transparentize } from "@chakra-ui/theme-tools";

const flushedVariant = (props) => {
  const { colorScheme: c } = props;
  return {
    field: {
      bg: `${c}.700`,
      borderBottom: "0px solid",
      borderColor: `none`,
      outline: 0,
      borderRadius: "md",
      color: `${c}.50`,
      _hover: {
        // borderColor: `${c}.50`,
        bg: `${c}.500`,
        borderWidth: 0,
        outline: 0,
      },
      _placeholder: { color: `${c}.1200` },
    },
  };
};

const outlineVariant = (props) => {
  const { colorScheme: c, theme } = props;
  const bgColor = transparentize(`${c}.50`, 0.8)(theme);
  const bgColorHover = transparentize(`${c}.50`, 0.7)(theme);
  return {
    field: {
      bg: bgColor,
      borderColor: `${c}.50`,
      _hover: {
        borderColor: `${c}.100`,
        bg: bgColorHover,
        borderWidth: 0,
      },
    },
  };
};

const newTagVariant = () => {
  return {
    field: {
      maxW: "150px",
      fontWidth: 800,
    },
  };
};

const filledVariant = () => {
  return {
    field: {
      bg: `white.200`,
      _hover: {
        bg: `white.300`,
      },
    },
  };
};

const Input = {
  parts: ["field", "addon"],
  baseStyle: () => {
    return {
      // bg: `${c}.100`,
      addon: {
        bg: `inherit`,
        border: "0px solid",
        borderColor: "inherit",
        // bg: `${c}.100`,
      },
      field: {
        _placeholder: { textColor: "gray.1100" },
      },
    };
  },
  variants: {
    outline: outlineVariant,
    flushed: flushedVariant,
    newTag: newTagVariant,
    filled: filledVariant,
  },

  defaultProps: {
    colorScheme: "blue",
    size: "md",
    variant: "filled",
  },
};

export default Input;
