import { React, useEffect, useState } from "react";
import "/styles/styles.css";
import "/styles/nprogress.css";
import "/styles/sidebar.css";
import "highlight.js/styles/github.css";
import "focus-visible/dist/focus-visible";
import dynamic from "next/dynamic";
import { QueryClient, QueryClientProvider } from "react-query";

const HeadSEO = dynamic(() => import("../src/components/HeadSEO"), {
  ssr: false,
});
const HeadLinks = dynamic(() => import("../src/components/HeadLinks"), {
  ssr: false,
});
const AppContext = dynamic(() => import("../src/AppContext"), {
  ssr: false,
});
const DefaultLayout = dynamic(() => import("../src/layouts"), {
  ssr: false,
});
import { useRouter } from "next/router";
import NProgress from "nprogress";

export default function CachingApp({ Component, pageProps }) {
  const [queryClient] = useState(new QueryClient());

  const router = useRouter();

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
      <QueryClientProvider client={queryClient}>
        <AppContext>{getLayout(<Component {...pageProps} />)}</AppContext>
      </QueryClientProvider>
    </>
  );
}
