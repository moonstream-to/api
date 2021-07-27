// TODO: rename to icon, gigignored from parent .gitignore file
import React from "react";

const Icon = ({ className, style, icon, width, height, onClick }) => (
  <img
    onClick={onClick ? onClick : () => {}}
    style={{ style, width: width, height: height }}
    src={`/icons/${icon}.svg`}
    alt={`icon-${icon}-${height}`}
    className={className}
  />
);

export default Icon;
