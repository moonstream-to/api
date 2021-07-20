import { Flex, Box } from "@chakra-ui/react";
import React, { useEffect, useRef, useState } from "react";
import { useRouter } from "../core/hooks";
const Scrollable = (props) => {
  const scrollerRef = useRef();
  const router = useRouter();
  const [path, setPath] = useState();
  useEffect(() => {
    setPath(router.nextRouter.pathname);
  }, [router.nextRouter.pathname]);

  scrollerRef?.current?.scrollTo({
    top: 0,
    left: 0,
    behavior: path === router.nextRouter.pathname ? "smooth" : "auto",
  });

  return (
    <Flex className="ScrollableWrapper" direction="column" w="100%" overflowY="hidden" maxH="100%">
      <Box className="Scrollable" direction="column" ref={scrollerRef} overflowY="scroll">
        {props.children}
      </Box>
    </Flex>
  );
};

export default Scrollable;
