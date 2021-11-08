import { React, useEffect, useState } from "react";
import "/styles/styles.css";
import "/styles/nprogress.css";
import "/styles/sidebar.css";
import "highlight.js/styles/github.css";
import "focus-visible/dist/focus-visible";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import dynamic from "next/dynamic";
import { QueryClient, QueryClientProvider } from "react-query";
import { ReactQueryDevtools } from "react-query/devtools";
import HeadLinks from "../src/components/HeadLinks";
import HeadSEO from "../src/components/HeadSEO";
const AppContext = dynamic(() => import("../src/AppContext"), {
  ssr: false,
});
const DefaultLayout = dynamic(() => import("../src/layouts"), {
  ssr: false,
});
import { useRouter } from "next/router";
import NProgress from "nprogress";
import { WHITE_LOGO_W_TEXT_URL } from "../src/core/constants";

export default function CachingApp({ Component, pageProps }) {
  const [queryClient] = useState(new QueryClient());

  const router = useRouter();

  useEffect(() => {
    if (
      router.pathname !== "/entry-point" &&
      window &&
      localStorage.getItem("entry_point")
    ) {
      localStorage.removeItem("entry_point");
    }
  }, [router]);

  useEffect(() => {
    const handleStart = () => {
      NProgress.start();
    };
    const handleStop = () => {
      NProgress.done();
    };

    router.events.on("routeChangeStart", handleStart);
    router.events.on("routeChangeComplete", handleStop);
    router.events.on("routeChangeError", handleStop);

    return () => {
      router.events.off("routeChangeStart", handleStart);
      router.events.off("routeChangeComplete", handleStop);
      router.events.off("routeChangeError", handleStop);
    };
  }, [router]);
  const getLayout =
    Component.getLayout || ((page) => <DefaultLayout>{page}</DefaultLayout>);

  const headLinks = [
    { rel: "preload", as: "image", href: WHITE_LOGO_W_TEXT_URL },
  ];
  pageProps.preloads && headLinks.push(...pageProps.preloads);
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
      <HeadLinks links={headLinks} />
      <QueryClientProvider client={queryClient}>
        <ReactQueryDevtools initialIsOpen={false} />
        <AppContext>{getLayout(<Component {...pageProps} />)}</AppContext>
      </QueryClientProvider>
    </>
  );
}
