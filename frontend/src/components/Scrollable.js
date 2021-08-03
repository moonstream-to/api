import { Flex, Box } from "@chakra-ui/react";
import React, { useEffect, useRef, useState } from "react";
import { useRouter, useAnalytics } from "../core/hooks";
const Scrollable = (props) => {
  const scrollerRef = useRef();
  const router = useRouter();
  const [path, setPath] = useState();

  const [scrollDepth, setScrollDepth] = useState(0);
  const { mixpanel, isLoaded } = useAnalytics();

  const getScrollPrecent = ({ currentTarget }) => {
    const scroll_level =
      (100 * (currentTarget.scrollTop + currentTarget.clientHeight)) /
      currentTarget.scrollHeight;
    return scroll_level;
  };

  const handleScroll = (e) => {
    const currentScroll = Math.ceil(getScrollPrecent(e) / 10);
    if (currentScroll > scrollDepth) {
      setScrollDepth(currentScroll);
      isLoaded &&
        mixpanel.people.increment({
          [`Scroll depth at: ${router.nextRouter.pathname}`]: currentScroll,
        });
    }
  };

  useEffect(() => {
    setPath(router.nextRouter.pathname);
  }, [router.nextRouter.pathname]);

  useEffect(() => {
    scrollerRef?.current?.scrollTo({
      top: 0,
      left: 0,
      behavior: path === router.nextRouter.pathname ? "smooth" : "auto",
    });
    // eslint-disable-next-line
  }, [path]);

  return (
    <Flex
      className="ScrollableWrapper"
      direction="column"
      w="100%"
      overflowY="hidden"
      maxH="100%"
    >
      <Box
        className="Scrollable"
        direction="column"
        ref={scrollerRef}
        overflowY="scroll"
        onScroll={(e) => handleScroll(e)}
      >
        {props.children}
      </Box>
    </Flex>
  );
};

export default Scrollable;
