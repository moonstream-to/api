import { React } from "react";
import { chakra } from "@chakra-ui/react";

const _RoundedRectSVG = (props) => {
  const _scale = props.scaling || 1.0;
  return (
    <svg
      height={134 * _scale}
      viewBox="0 0 472 134"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        d="M3 33C3 16.4315 16.4315 3 33 3H439C455.569 3 469 16.4315 469 33V101C469 117.569 455.569 131 439 131H33C16.4314 131 3 117.569 3 101V33Z"
        fill="white"
        stroke="url(#paint0_linear_291_337)"
        strokeWidth="5"
      />
      {/* <defs>
        <linearGradient
          id="paint0_linear_291_337"
          x1="229.821"
          y1="3"
          x2="229.821"
          y2="131"
          gradientUnits="userSpaceOnUse"
        >
          <stop stopColor="#212698" />
          <stop offset="1" stopColor="#FF8B73" />
        </linearGradient>
      </defs> */}
    </svg>
  );
};

const RoundedRectSVG = chakra(_RoundedRectSVG);

export default RoundedRectSVG;
