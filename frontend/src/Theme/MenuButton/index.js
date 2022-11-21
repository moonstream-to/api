const mobileVariant = () => {
  return {
    _active: {
      backgroundColor: "black.300",
      color: "white",
      textDecoration: "none",
    },
    _focus: {
      backgroundColor: "black.300",
      color: "white",
      textDecoration: "none",
    },
    color: "white",
    fontSize: "sm",
    margin: "0px",
    padding: "0px",
  };
};

const MenuButton = {
  variants: {
    mobile: mobileVariant,
  },
};

export default MenuButton;
