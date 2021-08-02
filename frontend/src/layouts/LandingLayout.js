import { jsx } from "@emotion/react";
import { Scrollable, Footer } from "../components";
import { getLayout as getSiteLayout } from "./index";

const DefaultLayout = (props) => {
  return (
    <Scrollable>
      {props.children}
      <Footer />
    </Scrollable>
  );
};

export const getLayout = (page) =>
  getSiteLayout(<DefaultLayout>{page}</DefaultLayout>);

export default DefaultLayout;
