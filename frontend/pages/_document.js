import React from "react";
import Document, { Html, Head, Main, NextScript } from "next/document";
const GTAG = process.env.NEXT_PUBLIC_LANDING_PAGE_GTAG;

export default class MyDocument extends Document {
  render() {
    return (
      <Html
        lang="en"
        style={{ width: "100%", height: "100%", fontSize: "16px" }}
      >
        <Head>
          <meta name="theme-color" content="#000000" />
          <meta charSet="utf-8" />
          <link rel="icon" href="/favicon.png" />
          {/* {`<!-- robots -->`} */}
          <meta
            name="robots"
            content={
              process.env.NEXT_PUBLIC_BUILD_TARGET === "alpha"
                ? "noindex"
                : "all"
            }
          />
          <meta name="author" content="Bugout" />
          {/* {`<!-- resources -->`} */}
          <link rel="apple-touch-icon" href="/favicon.png" />
          {/* {`<!--
      manifest.json provides metadata used when your web app is installed on a
      user's mobile device or desktop. See https://developers.google.com/web/fundamentals/web-app-manifest/
    -->`} */}
          <link rel="manifest" href="/manifest.json" />

          <link rel="preconnect" href="https://s3.amazonaws.com" />
          <link
            rel="preload"
            as="style"
            href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700;800;900&display=swap"
          />
          <link
            href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700;800;900&display=swap"
            rel="stylesheet"
          />
          <link rel="preconnect" href="https://s3.amazonaws.com" />

          {/* <!-- Global site tag (gtag.js) - Google Analytics --> */}
          <script
            async
            src={`https://www.googletagmanager.com/gtag/js?id=${GTAG}`}
          ></script>
          <script
            dangerouslySetInnerHTML={{
              __html: `
              window.dataLayer = window.dataLayer || [];
              function gtag() {
                dataLayer.push(arguments);
              }
              gtag("js", new Date());
              gtag("config", "${GTAG}");`,
            }}
          />
        </Head>
        <body>
          <Main />
          <NextScript />
        </body>
      </Html>
    );
  }
}
