// import { mode, transparentize } from "@chakra-ui/theme-tools"

const variantAccountMenu = (props) => {
  const { colorScheme: c } = props;

  return {
    width: "100%",
    w: "100%",
    borderRadius: "0px",
    borderStyle: "solid",
    borderTopWidth: "1px",
    bgColor: `white.200`,
    borderColor: `gray.100`,
    color: `black.100`,
    m: 0,
    _hover: {
      bg: `white.300`,
      // color: `white.100`,
    },
    _focus: {
      textDecoration: "underline",
      outline: "none",
      // color: `white.100`,
    },
    _active: {
      textDecoration: "none",
      // bg: `${c}.200`,
      // color: `white.100`,
      _before: {
        position: "absolute",
        content: "''",
        top: "0",
        bottom: "0",
        left: "0",
        width: "0.5rem",
        backgroundColor: `${c}.400`,
      },
      _last: {
        _before: {
          borderBottomLeftRadius: "md",
        },
      },
    },
    _last: {
      my: "-1px",
      borderBottomWidth: "1px",
      boxSizing: "border-box",
      borderBottomRadius: "md",
    },
  };
};

const variantLink = () => {
  // const { colorScheme: c } = props;
  return {
    _focus: {
      textDecoration: "underline",
    },
  };
};

const variantOutline = (props) => {
  const { colorScheme: c } = props;
  return {
    borderColor: `${c}.900`,
    borderWidth: `0.125rem`,
    boxSizing: "border-box",
    color: `${c}.900`,
    _hover: {
      boxShadow: "md",
    },
    _focus: {
      textDecoration: "underline",
    },
  };
};
const variantSolid = (props) => {
  const { colorScheme: c } = props;
  return {
    bg: `${c}.900`,
    _focus: {
      textDecoration: "underline",
    },
    _disabled: {
      bg: `${c}.200`,
    },
    _hover: {
      bg: `${c}.500`,
      // color: `${c}.100`,
      _disabled: {
        bg: `${c}.100`,
      },
    },
  };
};

const variantGhost = (props) => {
  const { colorScheme: c } = props;

  return {
    // color: `white.100`,
    _focus: {
      textDecoration: "underline",
    },
    _disabled: {
      bg: `${c}.50`,
    },
    _hover: {
      // bg: `${c}.600`,
      _disabled: {
        bg: `${c}.100`,
      },
    },
  };
};

const variantOrangeAndBlue = () => {
  return {
    alignItems: "center",
    justifyContent: "center",
    border: "solid transparent",
    borderRadius: "70px",
    variant: "solid",
    fontSize: ["md", "md", "lg", "lg", "xl", "xl"],
    textColor: "white",
    bg: "#FF8B73",
    py: 3,
    px: 5,
  };
};

const variantWhiteOnOrange = () => {
  return {
    alignItems: "center",
    justifyContent: "center",
    border: "solid transparent",
    borderRadius: "70px",
    variant: "solid",
    fontSize: ["md", "md", "lg", "lg", "xl", "xl"],
    textColor: "white",
    bg: "#FF8B73",
    py: 3,
    px: 5,
  };
};

const variantOrangeGradient = () => {
  return {
    border: "none",
    borderRadius: "30px",
    fontSize: ["md", "md", "lg", "lg", "xl", "xl"],
    textColor: "white",
    bg: "linear-gradient(92.26deg, #F56646 8.41%, #FFFFFF 255.37%)",
    fontWeight: "700",
    padding: "10px 30px",
    _hover: {
      bg: "linear-gradient(264.06deg, #F56646 -6.89%, #FFFFFF 335.28%)",
    },
  };
};

const variantSolidWhite = () => {
  return {
    bg: "white",
    textColor: "black",
    border: "none",
    borderRadius: "30px",
    p: "10px 30px",
    fontSize: ["md", "md", "lg", "lg", "xl", "xl"],
    _hover: {
      bg: "#E6E6E6",
    },
  };
};

const variantPlainOrange = () => {
  return {
    alignItems: "center",
    justifyContent: "center",
    border: "solid transparent",
    borderRadius: "30px",
    // variant: "solid",
    fontSize: ["md", "md", "lg", "lg", "xl", "xl"],
    textColor: "white",
    bg: "#F56646",
    fontWeight: "700",
    padding: "10px 30px",
    _hover: {
      backgroundColor: "#F4532F",
      textDecoration: "none",
    },
    _focus: {
      backgroundColor: "#F4532F",
    },
    _active: {
      backgroundColor: "#F4532F",
    },
  };
};

const variantWhiteOutline = () => {
  return {
    color: "white",
    border: "2px solid white",
    borderRadius: "30px",
    bg: "transparent",
    p: "10px 30px",
    fontSize: "20px",
    textDecoration: "none",
    _hover: {
      backgroundColor: "transparent",
      borderWidth: "3px",
      p: "9px 29px",
    },
    _focus: {
      backgroundColor: "transparent",
    },
    _active: {
      backgroundColor: "transparent",
    },
  };
};

const Button = {
  // 1. We can update the base styles
  baseStyle: () => ({
    px: "1rem",
    py: "1rem",
    transition: "0.1s",
    width: "fit-content",
    borderRadius: "md",
    borderStyle: "solid",
    fontWeight: "600",
    m: 1,

    // _active: {
    //   bg: `${props.colorScheme}.${props.colorMode}.200`,
    //   color: `${props.colorScheme}.${props.colorMode}.50`,
    // },
    // _focus: {
    //   bg: `${props.colorScheme}.${props.colorMode}.400`,
    //   color: `${props.colorScheme}.${props.colorMode}.50`,
    // },
  }),
  // 2. We can add a new button size or extend existing
  sizes: {
    xl: {
      h: 16,
      minW: 16,
      fontSize: "4xl",
      px: 8,
    },
  },
  // 3. We can add a new visual variant
  variants: {
    accountMenu: variantAccountMenu,
    solid: variantSolid,
    ghost: variantGhost,
    outline: variantOutline,
    link: variantLink,
    orangeAndBlue: variantOrangeAndBlue,
    whiteOnOrange: variantWhiteOnOrange,
    plainOrange: variantPlainOrange,
    whiteOutline: variantWhiteOutline,
    orangeGradient: variantOrangeGradient,
    solidWhite: variantSolidWhite,
  },
};
export default Button;
