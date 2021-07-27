const subtleVariant = () => {
  return {
    bg: `white.200`,
    boxShadow: "sm",
    transition: "0.1s",
    _hover: {
      bg: `white.300`,
    },
  };
};

const Tag = {
  parts: ["container", "label", "closeButton"],
  baseStyle: {
    container: {
      m: 1,
    },
  },

  variants: {
    subtle: (props) => ({
      container: subtleVariant(props),
    }),
  },
};

export default Tag;
