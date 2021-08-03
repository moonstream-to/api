import React from "react";
import Footer from "../components/Footer";
import Scrollable from "../components/Scrollable";
import RootLayout from "./RootLayout";

const LayoutWrapper = ({ children }) => {
  return (
    <RootLayout>
      <Scrollable>
        {children}
        <Footer />
      </Scrollable>
    </RootLayout>
  );
};

export const getLayout = (page) => <LayoutWrapper>{page}</LayoutWrapper>;

export default LayoutWrapper;
