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
};
export default Badge;
