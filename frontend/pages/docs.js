import React from "react";
import { RedocStandalone } from "redoc";
import { Box } from "@chakra-ui/react";
import { getLayout } from "../src/layouts/RootLayout";
import { DEFAULT_METATAGS } from "../src/core/constants";

const Docs = () => {
  return (
    // <Box overflowY="hidden" w="100%" maxH="100%" minH="100vh">
    <>
      <Box w="100%" maxH="100vh" overflowY="scroll" zIndex={0}>
        <RedocStandalone
          specUrl="https://api.moonstream.to/openapi.json"
          options={{
            theme: {
              colors: {
                primary: { main: "#212990" },
                success: { main: "#92D050" },
                warning: { main: "#FD5602" },
                error: { main: "#C53030" },
                gray: { 50: "#f7f8fa", 100: "#eff1f4" },
              },
              rightPanel: { backgroundColor: "#34373d" },
            },
          }}
        />
      </Box>
    </>
    // </Box>
  );
};

export async function getStaticProps() {
  const metaTags = {
    title: "Moonstream: API Documentation",
    description: "API Documentation to use moonstream.to",
    keywords: "API, docs",
    url: "https://www.moonstream.to/docs",
  };
  return { props: { metaTags: { ...DEFAULT_METATAGS, ...metaTags } } };
}

Docs.getLayout = getLayout;
export default Docs;
