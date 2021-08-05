import React from "react";
import "/styles/styles.css";
import "/styles/sidebar.css";
import "highlight.js/styles/github.css";
import App from "next/app";
import dynamic from "next/dynamic";
import { QueryClient, QueryClientProvider } from "react-query";
import HeadSEO from "../src/components/HeadSEO";
import HeadLinks from "../src/components/HeadLinks";
const AppContext = dynamic(() => import("../src/AppContext"), {
  ssr: false,
});
const DefaultLayout = dynamic(() => import("../src/layouts"), {
  ssr: false,
});

export default class CachingApp extends App {
  constructor(props) {
    super(props);
    this.state = { queryClient: new QueryClient() };
  }

  render() {
    const { Component, pageProps } = this.props;
    const getLayout =
      Component.getLayout || ((page) => <DefaultLayout>{page}</DefaultLayout>);

    console.log("rendering _app");
    return (
      <>
        <style global jsx>{`
          html,
          body,
          body > div:first-child,
          div#__next,
          div#__next > div {
            height: 100% !important;
            width: 100%;
            overflow: hidden;
          }
        `}</style>
        {pageProps.metaTags && <HeadSEO {...pageProps.metaTags} />}
        {pageProps.preloads && <HeadLinks links={pageProps.preloads} />}
        <QueryClientProvider client={this.state.queryClient}>
          <AppContext>{getLayout(<Component {...pageProps} />)}</AppContext>
        </QueryClientProvider>
      </>
    );
  }
}
