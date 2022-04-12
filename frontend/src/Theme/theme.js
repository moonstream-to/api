import { extendTheme } from "@chakra-ui/react";
import Button from "./Button";
import Tag from "./Tag";
import Menu from "./Menu";
import Input from "./Input";
// import Spinner from "./Spinner";
import NumberInput from "./NumberInput";
import Badge from "./Badge";
import Checkbox from "./Checkbox";
import Table from "./Table";
import Tooltip from "./Tooltip";
import Spinner from "./Spinner";
import Heading from "./Heading";
import { createBreakpoints } from "@chakra-ui/theme-tools";

const breakpointsCustom = createBreakpoints({
  sm: "24em", //Mobile phone
  md: "64.01em", //Tablet or rotated phone
  lg: "89.9em", //QHD
  xl: "160em", //4k monitor
  "2xl": "192em", // Mac Book 16" and above
});

const Accordion = {
  parts: ["container", "panel", "button"],
  baseStyle: {
    container: { borderColor: "white.300" },
    panel: { pb: 4 },
  },
  // defaultProps: {
  //   size: "xl",
  //   item: { borderColor: "white.300" },
  // },
};

const theme = extendTheme({
  breakpoints: breakpointsCustom,
  config: {
    initialColorMode: "light",
  },
  styles: {
    global: {
      body: {
        color: "blue.1200",
      },
    },
  },

  components: {
    Button,
    Accordion,
    Menu,
    Input,
    Tag,
    NumberInput,
    Badge,
    Checkbox,
    Table,
    Spinner,
    Tooltip,
    Heading,
  },

  fonts: {
    heading: '"Work Sans", sans-serif',
    body: '"Work Sans", sans-serif',
    mono: '"Work Sans", monospace',
  },
  fontSizes: {
    xs: "0.625rem", //10px
    sm: "0.875rem", //14px
    md: "1rem", //16px
    lg: "1.25rem", //20px
    xl: "1.375rem", //22
    "2xl": "1.5rem", //24px
    "3xl": "1.625rem", //26
    "4xl": "1.875rem", //30px
    "5xl": "2.625rem", //42px
    "6xl": "3.75rem", //60px
    "7xl": "4.5rem", //72px
  },

  colors: {
    brand: {
      100: "#212C8A",
      200: "#111442",
      300: "#53B9D1",
      400: "#4579D8",
      500: "##F29C38",
    },

    blue: {
      0: "#FFFFFFFF",
      50: "#e9eaf4",
      100: "#d3d4e9",
      200: "#bcbfde",
      300: "#a6a9d3",
      400: "#9094c8",
      500: "#7a7fbc",
      600: "#6469b1",
      700: "#4d54a6",
      800: "#373e9b",
      900: "#212990",
      1000: "#1e2582",
      1100: "#1a2173",
      1200: "#171d65",
      1300: "#141956",
      1400: "#111548",
      1500: "#0d103a",
      1600: "#0a0c2b",
      1700: "#07081d",
      1800: "#03040e",
      1900: "#0d103a",
      2000: "#000000",
    },

    gray: {
      0: "#FFFFFFFF",
      50: "#f7f8fa",
      100: "#eff1f4",
      200: "#e6eaef",
      300: "#dee3ea",
      400: "#d6dce5",
      500: "#ced5df",
      600: "#c6ceda",
      700: "#bdc7d5",
      800: "#b5c0cf",
      900: "#adb9ca",
      1000: "##9ca7b6",
      1100: "#8a94a2",
      1200: "#79828d",
      1300: "#686f79",
      1400: "#575d65",
      1500: "#454a51",
      1600: "#34373d",
    },
    white: {
      100: "#FFFFFF",
      200: "#F7F8FB",
      300: "#EAEBF7",
    },
    red: {
      0: "#FFFFFFFF",
      50: "#f9eaea",
      100: "#f3d6d6",
      200: "#eec1c1",
      300: "#e8acac",
      400: "#e29898",
      500: "#dc8383",
      600: "#d66e6e",
      700: "#d15959",
      800: "#cb4545",
      900: "#C53030",
    },

    orange: {
      0: "#FFFFFFFF",
      50: "#ffeee6",
      100: "#ffddcc",
      200: "#feccb3",
      300: "#febb9a",
      400: "#feab81",
      500: "#fe9a67",
      600: "#fe894e",
      700: "#fd7835",
      800: "#fd671b",
      900: "#FD5602",
    },

    green: {
      0: "#FFFFFFFF",
      50: "#e9f6dc",
      100: "#e9f6dc", //Duplicates 50!!!!
      200: "#def1cb",
      300: "#d3ecb9",
      400: "#c9e8a8",
      500: "#bee396",
      600: "#b3de85",
      700: "#a8d973",
      800: "#9dd562",
      900: "#92D050",
    },

    black: {
      100: "#333399",
      200: "#111442",
    },
  },
});

export default theme;
