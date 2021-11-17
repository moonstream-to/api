import React from "react";
import { useBreakpointValue, Flex } from "@chakra-ui/react";
import SplitPane, { Pane } from "react-split-pane";
import { getLayout as getSiteLayout } from "./AppLayout";
import EntriesNavigation from "../components/EntriesNavigation";
import { useContext } from "react";
import UIContext from "../core/providers/UIProvider/context";
const EntriesLayout = (props) => {
  const ui = useContext(UIContext);
  const defaultWidth = useBreakpointValue({
    base: "14rem",
    sm: "16rem",
    md: "18rem",
    lg: "20rem",
    xl: "22rem",
    "2xl": "24rem",
  });

  return (
    <>
      <Flex id="Entries" flexGrow={1} maxW="100%">
        <SplitPane
          allowResize={false}
          split="vertical"
          defaultSize={defaultWidth}
          primary="first"
          minSize={defaultWidth}
          pane1Style={
            ui.entriesViewMode === "list"
              ? { transition: "1s", width: "100%" }
              : ui.entriesViewMode === "entry"
              ? { transition: "1s", width: "0%" }
              : {
                  overflowX: "hidden",
                  height: "100%",
                  width: ui.isMobileView ? "100%" : "55%",
                }
          }
          pane2Style={
            ui.entriesViewMode === "entry"
              ? { transition: "1s", width: "0%" }
              : ui.entriesViewMode === "list"
              ? {
                  transition: "1s",
                  width: "100%",
                }
              : { overflowX: "hidden", height: "100%" }
          }
          style={{
            position: "relative",
            height: "100%",
            flexBasis: "100px",
            overflowX: "hidden",
          }}
        >
          <Pane
            className="EntriesNavigation"
            style={{
              height: "100%",
            }}
          >
            <EntriesNavigation />
          </Pane>

          <Pane
            className="EntryScreen"
            style={{
              height: "100%",
            }}
          >
            {props.children}
          </Pane>
        </SplitPane>
      </Flex>
    </>
  );
};

export const getLayout = (page) =>
  getSiteLayout(<EntriesLayout>{page}</EntriesLayout>);

export default EntriesLayout;
