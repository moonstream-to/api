const baseStyle = {
  color: "blue.400",
  thickness: "4px",
  speed: "1.5s",
  my: 8,
};
const variants = {
  basic: { thickness: "4px", speed: "1.5s" },
};

const sizes = {
  xs: {
    "--spinner-size": "0.75rem",
  },
  sm: {
    "--spinner-size": "1rem",
  },
  md: {
    "--spinner-size": "1.5rem",
  },
  lg: {
    "--spinner-size": "2rem",
  },
  xl: {
    "--spinner-size": "3rem",
  },
};

const defaultProps = {
  size: "md",
};

export default {
  baseStyle,
  sizes,
  defaultProps,
  variants,
};
