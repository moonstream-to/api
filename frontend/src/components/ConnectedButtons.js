import React, { useEffect, useRef, useContext } from "react";
import {
  Flex,
  Heading,
  Button,
  Link,
  SimpleGrid,
  useBreakpointValue,
} from "@chakra-ui/react";
import Xarrow, { useXarrow } from "react-xarrows";
import UIContext from "../core/providers/UIProvider/context";

const ArrowCTA = (props) => {
  const ui = useContext(UIContext);
  const box0Ref = useRef(null);
  const box1Ref = useRef(null);
  const box2Ref = useRef(null);
  const box3Ref = useRef(null);

  const gridSetup = useBreakpointValue({
    base: "column",
    sm: "horizontal",
    md: "grid",
    lg: "grid",
    xl: "grid",
    "2xl": "grid",
  });

  const updateXarrow = useXarrow();

  useEffect(() => {
    updateXarrow();
  }, [ui.isMobileView]);

  return (
    <SimpleGrid
      columns={[1, 2, 3, null, 3]}
      spacing={[10, 0, 10, null, 10]}
      placeItems="center"
      w="100%"
      _after={{}}
    >
      <Flex
        gridColumn={[1, 1, 2, null, 2]}
        gridRow={[1, 2, 1, null, 1]}
        // mb={14}
        w={["180px", "180px", "250px", null, "250px"]}
        // ml="16px"
        placeSelf="center"
        placeContent="center"
      >
        <Heading m={0} ref={box0Ref} fontSize={["lg", "lg", "lg", null, "lg"]}>
          {props.title}
        </Heading>
      </Flex>

      <Button
        as={props.button1.link && Link}
        href={props.button1.link ?? null}
        gridColumn={[1, 2, 1, null, 1]}
        gridRow={[2, 1, 2, null, 2]}
        zIndex={10}
        ref={box1Ref}
        boxShadow="md"
        variant="solid"
        colorScheme="suggested"
        className="MoonStockSpeciality element1"
        w={["180px", "180px", "250px", null, "250px"]}
        onClick={props.button1.onClick}
      >
        {props.button1.label}
      </Button>

      <Button
        as={props.button2.link && Link}
        href={props.button2.link ?? null}
        gridColumn={[1, 2, 2, null, 2]}
        gridRow={[3, 2, 2, null, 2]}
        zIndex={10}
        ref={box2Ref}
        boxShadow="md"
        variant="solid"
        colorScheme="secondary"
        className="MoonStockSpeciality element2"
        w={["180px", "180px", "250px", null, "250px"]}
        onClick={props.button2.onClick}
      >
        {props.button2.label}
      </Button>

      <Button
        as={props.button3.link && Link}
        href={props.button3.link ?? null}
        gridColumn={[1, 2, 3, null, 3]}
        gridRow={[4, 3, 2, null, 2]}
        zIndex={10}
        ref={box3Ref}
        boxShadow="md"
        variant="solid"
        colorScheme="primary"
        w={["180px", "180px", "250px", null, "250px"]}
        onClick={props.button3.onClick}
      >
        {props.button3.label}
      </Button>
      <Xarrow
        // showXarrow={!!box0Ref.current && !!box1Ref.current}
        dashness={{
          strokeLen: 10,
          nonStrokeLen: 15,
          animation: -2,
        }}
        // animateDrawing={true}
        color="#92D050"
        showHead={false}
        start={box0Ref} //can be react ref
        end={box1Ref} //or an id
      />
      <Xarrow
        dashness={{
          strokeLen: 10,
          nonStrokeLen: 15,
          animation: -1,
        }}
        color="#FD5602"
        showHead={false}
        start={box0Ref} //can be react ref
        end={box2Ref} //or an id
      />
      <Xarrow
        dashness={{
          strokeLen: 10,
          nonStrokeLen: 15,
          animation: -4,
        }}
        color="#212990"
        showHead={false}
        start={box0Ref} //can be react ref
        end={box3Ref} //or an id
      />
    </SimpleGrid>
  );
};

export default ArrowCTA;
