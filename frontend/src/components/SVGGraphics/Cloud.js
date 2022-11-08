import { React } from "react";
import { chakra } from "@chakra-ui/react";

const _CloudSVG = (props) => {
  const _scale = props.scaling || 1.0;
  return (
    <svg
      height={250 * _scale}
      viewBox="0 0 407 250"
      fill="white"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        d="M67.6021 247H314.166C447.987 247 425.603 40.5319 291.381 86.3142C291.381 -28.3364 89.9964 -28.3364 89.9964 109.274C-21.9547 86.3142 -21.9547 246.989 67.6021 246.989V247Z"
        stroke="url(#paint0_linear_293_70)"
        strokeWidth="5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      {/* <defs>
        <linearGradient
          id="paint0_linear_293_70"
          x1="203.5"
          y1="3"
          x2="203.5"
          y2="247"
          gradientUnits="userSpaceOnUse"
        >
          <stop stopColor="#212698" />
          <stop offset="0.932309" stopColor="#FF9473" />
        </linearGradient>
      </defs> */}
    </svg>
  );
};

const CloudSVG = chakra(_CloudSVG);

export default CloudSVG;
