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
import DefaultLayout from "../src/layouts";

export default class CachingApp extends App {
  constructor(props) {
    super(props);
    this.state = { queryClient: new QueryClient() };
  }

  render() {
    const { Component, pageProps } = this.props;
    const getLayout =
      Component.getLayout || ((page) => <DefaultLayout>{page}</DefaultLayout>);

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
