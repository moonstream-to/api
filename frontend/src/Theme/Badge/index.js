const variantOutline = () => {
  return {
    container: {
      bg: "black",
      color: "yellow",
    },
  };
};

const Badge = {
  parts: ["container", "label", "closeButton"],
  variants: {
    outline: variantOutline,
  },
  sizes: {
    xxl: {
      fontSize: "4xl",
      borderWidth: "xl",
      borderRadius: "lg",
    },
  },
};
export default Badge;
