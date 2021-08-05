import { React, useEffect, useState } from "react";
import "/styles/styles.css";
import "/styles/nprogress.css";
import "/styles/sidebar.css";
import "highlight.js/styles/github.css";
import "react-mde/lib/styles/css/react-mde-all.css";
import "focus-visible/dist/focus-visible";
import dynamic from "next/dynamic";
import { ReactQueryCacheProvider, QueryCache } from "react-query";
import { ReactQueryDevtools } from "react-query-devtools";
import HeadLinks from "../src/components/HeadLinks";
import HeadSEO from "../src/components/HeadSEO";
const AppContext = dynamic(() => import("../src/AppContext"), {
  ssr: false,
});
import DefaultLayout from "../src/layouts";
import { useRouter } from "next/router";
import NProgress from "nprogress";

export default function CachingApp({ Component, pageProps }) {
  const [queryCache] = useState(new QueryCache());

  const router = useRouter();

  useEffect(() => {
    const handleStart = (url) => {
      NProgress.start();
    };
    const handleStop = () => {
      NProgress.done();
    };

    router.events.on("routeChangeStart", handleStart);
    router.events.on("routeChangeComplete", handleStop);
    router.events.on("routeChangeError", handleStop);

    console.log("_app", router.asPath);
    return () => {
      router.events.off("routeChangeStart", handleStart);
      router.events.off("routeChangeComplete", handleStop);
      router.events.off("routeChangeError", handleStop);
    };
  }, [router]);
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
      <ReactQueryCacheProvider queryCache={queryCache}>
        <ReactQueryDevtools initialIsOpen={false} />
        <AppContext>{getLayout(<Component {...pageProps} />)}</AppContext>
      </ReactQueryCacheProvider>
    </>
  );
}
