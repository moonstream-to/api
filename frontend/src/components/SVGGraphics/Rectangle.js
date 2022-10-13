import { React } from "react";
import { chakra } from "@chakra-ui/react";

const _RectangleSVG = (props) => {
  const _scale = props.scaling || 1.0;
  return (
    <svg
      height={265 * _scale}
      viewBox="0 0 245 265"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        d="M242 3V262H3V3H242Z"
        fill="white"
        stroke="url(#paint0_linear_293_56)"
        strokeWidth="5"
      />
      {/* <defs>
        <linearGradient
          id="paint0_linear_293_56"
          x1="242"
          y1="129.066"
          x2="3"
          y2="129.066"
          gradientUnits="userSpaceOnUse"
        >
          <stop stopColor="#212698" />
          <stop offset="1" stopColor="#FF8B73" />
        </linearGradient>
      </defs> */}
    </svg>
  );
};

const RectangleSVG = chakra(_RectangleSVG);

export default RectangleSVG;
