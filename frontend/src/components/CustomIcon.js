// TODO: rename to icon, gigignored from parent .gitignore file
import React from "react";

const Icon = ({ className, style, icon, width, height, onClick }) => {
  const iconSrc =
    icon === "logo"
      ? "https://s3.amazonaws.com/static.simiotics.com/moonstream/assets/White+logo.svg"
      : `/icons/${icon}.svg`;
  return (
    <img
      onClick={onClick ? onClick : () => {}}
      style={{ style, width: width, height: height }}
      src={iconSrc}
      alt={`icon-${icon}-${height}`}
      className={className}
    />
  );
};

export default Icon;
