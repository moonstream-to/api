import React from "react";
import Head from "next/head";
import propTypes from "prop-types";

const METATAGS = {
  title: propTypes.string.isRequired,
  keywords: propTypes.string.isRequired,
  description: propTypes.string.isRequired,
  url: propTypes.string.isRequired,
  image: propTypes.string.isRequired,

  ogType: propTypes.string,
  ogURL: propTypes.string,
  ogTitle: propTypes.string,
  ogDescription: propTypes.string,
  ogImage: propTypes.string,

  twitterCard: propTypes.oneOf([
    "Summary",
    "summary_large_image",
    "app",
    "player",
  ]),
  twitterURL: propTypes.string,
  twitterTitle: propTypes.string,
  twitterDescription: propTypes.string,
  twitterCreator: propTypes.string,
  twitterImageAlt: propTypes.string,
};

export const SEOHead = ({
  title,
  keywords,
  description,
  url,
  image,
  ogType,
  ogURL,
  ogTitle,
  ogDescription,
  ogImage,
  twitterCard,
  twitterURL,
  twitterTitle,
  twitterDescription,
  twitterCreator,
  twitterImageAlt,
  twitterImage,
}) => {
  return (
    <Head>
      <meta
        name="viewport"
        content="minimum-scale=1, initial-scale=1, width=device-width"
      />

      <title>{title}</title>
      <meta key="meta-title" name="title" content={title} />
      <meta key="meta-keywords" name="keywords" content={keywords} />
      <meta key="meta-description" name="description" content={description} />

      {/* <!-- Open Graph / Facebook --> */}
      <meta
        key="meta-og-type"
        property="og:type"
        content={ogType ?? "website"}
      />
      <meta key="meta-og-url" property="og:url" content={ogURL ?? url} />
      <meta
        key="meta-og-title"
        property="og:title"
        content={ogTitle ?? title}
      />
      <meta
        key="meta-og-description"
        property="og:description"
        content={ogDescription ?? description}
      />
      <meta
        key="meta-og-image"
        property="og:image"
        content={ogImage ?? image}
      />

      {/* <!-- Twitter --> */}
      <meta
        key="meta-twitter-card"
        property="twitter:card"
        content={twitterCard ?? "summary_large_image"}
      />
      <meta
        key="meta-twitter-url"
        property="twitter:url"
        content={twitterURL ?? url}
      />
      <meta
        key="meta-twitter-title"
        property="twitter:title"
        content={twitterTitle ?? title}
      />
      <meta
        key="meta-twitter-description"
        property="twitter:description"
        content={twitterDescription ?? description}
      />
      <meta
        key="meta-twitter-image"
        property="twitter:image"
        content={twitterImage ?? image}
      />

      {twitterImageAlt && (
        <meta
          key="meta-twitter-image-alt"
          property="twitter:image:alt"
          content={twitterImageAlt}
        />
      )}

      {twitterCreator && (
        <meta
          key="meta-twitter-image-alt"
          property="twitter:image:alt"
          content={twitterCreator}
        />
      )}
    </Head>
  );
};

SEOHead.propTypes = { ...METATAGS };

export default SEOHead;
