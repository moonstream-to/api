import { mode } from "@chakra-ui/theme-tools";

const baseStyle = (props) => {
  const bg = mode("gray.700", "gray.300")(props);
  return {
    "--tooltip-bg": `colors.${bg}`,
    px: "8px",
    py: "2px",
    bg: "var(--tooltip-bg)",
    "--popper-arrow-bg": "var(--tooltip-bg)",
    color: mode("whiteAlpha.900", "gray.900")(props),
    borderRadius: "sm",
    fontWeight: "medium",
    fontSize: "sm",
    boxShadow: "md",
    maxW: "320px",
    zIndex: "tooltip",
  };
};

const variantSuggestion = (props) => {
  const bg = mode("primary.700", "primary.300")(props);
  return {
    "--tooltip-bg": `colors.${bg}`,
    px: "8px",
    py: "2px",
    bg: "var(--tooltip-bg)",
    "--popper-arrow-bg": "var(--tooltip-bg)",
    color: mode("whiteAlpha.900", "gray.900")(props),
    borderRadius: "md",
    fontWeight: "medium",
    fontSize: "sm",
    boxShadow: "md",
    maxW: "320px",
    zIndex: "tooltip",
  };
};

const variantOnboarding = (props) => {
  const bg = mode("secondary.700", "secondary.300")(props);
  return {
    "--tooltip-bg": `colors.${bg}`,
    px: "8px",
    py: "2px",
    bg: "var(--tooltip-bg)",
    "--popper-arrow-bg": "var(--tooltip-bg)",
    color: mode("whiteAlpha.900", "gray.900")(props),
    borderRadius: "md",
    fontWeight: "medium",
    fontSize: "sm",
    boxShadow: "md",
    maxW: "320px",
    zIndex: "tooltip",
  };
};

const variants = {
  onboarding: variantOnboarding,
  suggestion: variantSuggestion,
};

export default {
  baseStyle,
  variants,
};
