// import { mode, whiten } from "@chakra-ui/theme-tools"

const Menu = {
  parts: ["list", "item"],
  baseStyle: (props) => {
    const { colorScheme: c } = props;
    return {
      item: {
        fontWeight: "medium",
        lineHeight: "normal",
        textColor: `${c}.900`,

        _hover: {
          bg: `orange.800`,
          textColor: "white.100",
        },
        _focus: {
          bg: `orange.700`,
          textColor: "white.100",
        },
      },
      list: {
        bg: "white.200",
        borderWidth: 0,
      },
    };
  },
};

export default Menu;
