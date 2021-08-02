import React from "react";
import Head from "next/head";
import propTypes from "prop-types";

const PRELOADS = {
  links: propTypes.arrayOf(
    propTypes.shape({
      as: propTypes.string,
      href: propTypes.string.isRequired,
      rel: propTypes.oneOf(["preconnect", "preload"]),
    })
  ),
};

export const PreloadHead = ({ links }) => {
  return (
    <Head>
      {links.map((link, idx) => {
        if (link.rel === "preload") {
          return (
            <link
              key={`preload-${idx}`}
              rel={link.rel}
              as={link.as}
              href={link.href}
            />
          );
        } else {
          return (
            <link key={`preconnect-${idx}`} rel={link.rel} href={link.href} />
          );
        }
      })}
    </Head>
  );
};

PreloadHead.propTypes = { ...PRELOADS };

export default PreloadHead;
