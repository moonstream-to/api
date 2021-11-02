import React, { useEffect, useRef, useContext } from "react";
import {
  Flex,
  Heading,
  Button,
  Link,
  SimpleGrid,
  useBreakpointValue,
  useMediaQuery,
} from "@chakra-ui/react";
import Xarrow, { useXarrow } from "react-xarrows";
import UIContext from "../core/providers/UIProvider/context";

const ArrowCTA = (props) => {
  const ui = useContext(UIContext);
  const box0Ref = useRef(null);
  const box1Ref = useRef(null);
  const box2Ref = useRef(null);
  const box3Ref = useRef(null);
  const box4Ref = useRef(null);

  const updateXarrow = useXarrow();

  useEffect(() => {
    updateXarrow();
    // eslint-disable-next-line
  }, [ui.isMobileView]);

  const xarrowEntrySide = useBreakpointValue({
    base: "top",
    sm: "left",
    md: "top",
    lg: "top",
    xl: "top",
    "2xl": "top",
  });

  const [isLargerThan580px] = useMediaQuery(["(min-width: 580px)"]);

  const buttonWidth = [
    "190px",
    isLargerThan580px ? "200px" : "140px",
    "230px",
    null,
    "280px",
  ];

  const fontSize = [
    undefined,
    isLargerThan580px ? undefined : "12px",
    undefined,
    null,
  ];

  return (
    <SimpleGrid
      columns={props.button4 ? [1, 2, 4, null, 4] : [1, 2, 3, null, 3]}
      spacing={[10, 0, 10, null, 10]}
      placeItems="center"
      w="100%"
      _after={{}}
    >
      <Flex
        gridColumn={
          props.button4
            ? [1, 1, `2 / span 2`, null, "2 / span 2"]
            : [1, 1, 2, null, 2]
        }
        // gridColumnStart={props.button4 ? [1, 2] : [0, 1]}
        // gridColumnEnd={props.button4 ? [1, 4] : [0, 3]}
        gridRow={
          props.button4 ? [1, `2 / span 2`, 1, null, 1] : [1, 2, 1, null, 1]
        }
        // mb={14}
        // w={["180px", "180px", "250px", null, "250px"]}
        w="100%"
        // ml="16px"
        placeSelf="center"
        placeContent="center"
      >
        <Heading
          m={0}
          ref={box0Ref}
          fontSize={["lg", isLargerThan580px ? "lg" : "sm", "lg", null, "lg"]}
        >
          {props.title}
        </Heading>
      </Flex>

      <Button
        as={props.button1.link && Link}
        _hover={!props.button1.link && { cursor: "unset" }}
        href={props.button1.link ?? null}
        gridColumn={[1, 2, 1, null, 1]}
        gridRow={[2, 1, 2, null, 2]}
        zIndex={10}
        ref={box1Ref}
        boxShadow="md"
        variant="solid"
        colorScheme="green"
        className="MoonStockSpeciality element1"
        w={buttonWidth}
        onClick={props.button1.onClick}
        fontSize={fontSize}
      >
        {props.button1.label}
      </Button>

      <Button
        as={props.button2.link && Link}
        href={props.button2.link ?? null}
        _hover={!props.button1.link && { cursor: "unset" }}
        gridColumn={[1, 2, 2, null, 2]}
        gridRow={[3, 2, 2, null, 2]}
        zIndex={10}
        ref={box2Ref}
        boxShadow="md"
        variant="solid"
        colorScheme="orange"
        className="MoonStockSpeciality element2"
        w={buttonWidth}
        fontSize={fontSize}
        onClick={props.button2.onClick}
      >
        {props.button2.label}
      </Button>

      <Button
        as={props.button3.link && Link}
        href={props.button3.link ?? null}
        _hover={!props.button1.link && { cursor: "unset" }}
        gridColumn={[1, 2, 3, null, 3]}
        gridRow={[4, 3, 2, null, 2]}
        zIndex={10}
        ref={box3Ref}
        boxShadow="md"
        variant="solid"
        colorScheme="blue"
        w={buttonWidth}
        fontSize={fontSize}
        onClick={props.button3.onClick}
      >
        {props.button3.label}
      </Button>
      {props.button4 && (
        <Button
          as={props.button4.link && Link}
          href={props.button4.link ?? null}
          _hover={!props.button1.link && { cursor: "unset" }}
          gridColumn={[1, 2, 4, null, 4]}
          gridRow={[5, 4, 2, null, 2]}
          zIndex={10}
          ref={box4Ref}
          boxShadow="md"
          variant="solid"
          colorScheme="red"
          w={buttonWidth}
          fontSize={fontSize}
          onClick={props.button4.onClick}
        >
          {props.button4.label}
        </Button>
      )}
      <Xarrow
        // showXarrow={!!box0Ref.current && !!box1Ref.current}
        dashness={{
          strokeLen: 10,
          nonStrokeLen: 15,
          animation: props.speedBase * props.button1.speed,
        }}
        // animateDrawing={true}
        color="#92D050"
        startAnchor={xarrowEntrySide ?? "top"}
        showHead={false}
        start={box1Ref} //can be react ref
        end={box0Ref} //or an id
      />
      <Xarrow
        dashness={{
          strokeLen: 10,
          nonStrokeLen: 15,
          animation: props.speedBase * props.button2.speed,
        }}
        color="#FD5602"
        startAnchor={xarrowEntrySide ?? "top"}
        showHead={false}
        start={box2Ref} //can be react ref
        end={box0Ref} //or an id
      />
      <Xarrow
        dashness={{
          strokeLen: 10,
          nonStrokeLen: 15,
          animation: props.speedBase * props.button3.speed,
        }}
        color="#212990"
        startAnchor={xarrowEntrySide ?? "top"}
        showHead={false}
        start={box3Ref} //can be react ref
        end={box0Ref} //or an id
      />
      {props.button4 && (
        <Xarrow
          dashness={{
            strokeLen: 10,
            nonStrokeLen: 15,
            animation: props.speedBase * props.button4.speed,
          }}
          color="#C53030"
          startAnchor={xarrowEntrySide ?? "top"}
          showHead={false}
          start={box4Ref} //can be react ref
          end={box0Ref} //or an id
        />
      )}
    </SimpleGrid>
  );
};

export default ArrowCTA;
