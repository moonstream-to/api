import { React, useRef } from "react";
import {
  chakra,
  Grid,
  GridItem,
  Flex,
  Center,
  VStack,
  Text,
  Icon,
  Popover,
  PopoverTrigger,
  PopoverBody,
  PopoverContent,
  useBreakpointValue,
} from "@chakra-ui/react";
import CloudSVG from "./SVGGraphics/Cloud";
import RectangleSVG from "./SVGGraphics/Rectangle";
import RoundedRectSVG from "./SVGGraphics/RoundedRect";
// import { AiFillFile } from "react-icons/ai";
import { BsFillPersonFill } from "react-icons/bs";
import { BsFillFileEarmarkCodeFill } from "react-icons/bs";
// import { MODAL_TYPES } from "../core/providers/OverlayProvider/constants";
import Xarrow from "react-xarrows";
import ExampleCode from "./ExampleCode";

const _EngineOverviewDiagram = () => {
  // const scaleWidth = (width) => {
  //   return [width * 0.65, width, width, width, width, width * 1.2].map(
  //     (val) => {
  //       return val + "px";
  //     }
  //   );
  // };

  const smartContract = useRef(null);
  const gameClient = useRef(null);
  const adminDashboard = useRef(null);
  const gameServer = useRef(null);
  const user = useRef(null);

  // const { toggleModal } = useModals();

  const xarrowStyle = {
    color: "#212990",
    showHead: true,
    headSize: 6,
  };

  const smallDiagram = useBreakpointValue({
    base: true,
    sm: true,
    md: false,
    lg: false,
    xl: false,
    "2xl": false,
  });

  // const collapseLayout = useBreakpointValue({
  //   base: true,
  //   sm: true,
  //   md: false,
  //   lg: false,
  //   xl: false,
  //   "2xl": false,
  // });

  return (
    <>
      {/* <Grid
        templateRows="repeat(2, 1fr)"
        templateColumns="repeat(3, 1fr)"
        gap={4}
      >
        <GridItem w="100px" h="100px" bgColor="red.200"></GridItem>
        <GridItem w="100px" h="100px" bgColor="red.200"></GridItem>
        <GridItem w="100px" h="100px" bgColor="red.200"></GridItem>
        <GridItem w="100px" h="100px" bgColor="red.200"></GridItem>
        <GridItem w="100px" h="100px" bgColor="red.200"></GridItem>
        <GridItem w="100px" h="100px" bgColor="red.200"></GridItem>
      </Grid> */}
      <Grid
        templateRows={["repeat(7)", "repeat(7)", "repeat(2)"]}
        templateColumns={["repeat(1, 1fr)", "repeat(1, 1fr)", "repeat(3, 1fr)"]}
        // gap={4}
        rowGap={[10, 10, 20]}
        columnGap={4}
      >
        <GridItem h={["80px", "80px", "auto"]} order={[2, 2, 0]}>
          <Flex
            ref={smartContract}
            w={["260px", "260px", "400px"]}
            h={["73", "73", "114px"]}
            position="relative"
            marginLeft="20px"
          >
            <RoundedRectSVG scale={1} />
            <Center
              position="absolute"
              left="0"
              top="0"
              w={["260px", "260px", "400px"]}
              h={["73", "73", "114px"]}
            >
              <VStack justifyContent="center" py="10px">
                <Text fontSize={["md", "md", "xl"]}>
                  Moonstream Smart Contracts
                </Text>
                {!smallDiagram && (
                  <Text pl={[0, 0, "30px"]} fontSize="md">
                    Your backend for lootboxes, crafting recipes, items,
                    minigames
                  </Text>
                )}
              </VStack>
            </Center>
          </Flex>
        </GridItem>
        <GridItem h={0} order={[6, 6, 1]}></GridItem>
        <GridItem h={["160px", "160px", "auto"]} order={[4, 4, 2]}>
          <Flex
            ref={gameClient}
            w={["155px", "155px", "189px"]}
            h={["160px", "160px", "205px"]}
            marginLeft={["80px", "80px", 0]}
            position="relative"
          >
            <RectangleSVG></RectangleSVG>
            <Center
              position="absolute"
              left="0"
              top="0"
              w={["155px", "155px", "189px"]}
              h={["160px", "160px", "205px"]}
            >
              <Text fontSize={["md", "md", "xl"]}>Game Client</Text>
            </Center>
          </Flex>
        </GridItem>
        <GridItem h={["160px", "160px", "auto"]} order={[1, 1, 3]}>
          <Flex
            ref={adminDashboard}
            w={["155px", "155px", "189px"]}
            h={["160px", "160px", "205px"]}
            marginLeft={["80px", "80px", 0]}
            position="relative"
          >
            <RectangleSVG scale={0.8}></RectangleSVG>
            <Center
              position="absolute"
              w={["155px", "155px", "189px"]}
              h={["160px", "160px", "205px"]}
            >
              <VStack
                w={["155px", "155px", "189px"]}
                h={["160px", "160px", "205px"]}
                justifyContent="center"
              >
                <Text fontSize={["md", "md", "lg"]}>Admin Dashboard</Text>
                {!smallDiagram && (
                  <Text pt="10px" pl={[0, 0, "8px"]} fontSize="md">
                    Choose mechanics at engine.moonstream.to
                  </Text>
                )}
              </VStack>
            </Center>
          </Flex>
        </GridItem>
        <GridItem h={["160px", "160px", "auto"]} order={[3, 3, 4]}>
          <Center>
            <Flex
              w={["155px", "155px", "189px"]}
              h={["160px", "160px", "205px"]}
              justifyContent="center"
              position="relative"
            >
              {/* <Icon
              as={BsFillFileEarmarkCodeFill}
              w={100}
              h={100}
              onClick={() => toggleModal({ type: MODAL_TYPES.EXAMPLE_CODE })}
            ></Icon> */}
              <Popover>
                <PopoverTrigger placement="top">
                  <Flex>
                    <Icon as={BsFillFileEarmarkCodeFill} w={100} h={100}></Icon>
                  </Flex>
                </PopoverTrigger>
                <PopoverContent w={["300px", "300px", "850px"]}>
                  <PopoverBody>
                    <ExampleCode />
                  </PopoverBody>
                </PopoverContent>
              </Popover>
            </Flex>
          </Center>
        </GridItem>
        <GridItem h={["120px", "120px", "auto"]} order={[5, 5, 5]}>
          <Flex
            ref={gameServer}
            w={["200px", "200px", "305px"]}
            h={["120px", "120px", "188px"]}
            marginLeft={["60px", "60px", "20px"]}
            position="relative"
          >
            <CloudSVG scale={0.5}></CloudSVG>
            <Center
              position="absolute"
              paddingTop="30px"
              w={["200px", "200px", "305px"]}
              h={["120px", "120px", "188px"]}
            >
              <Text fontSize={["md", "md", "lg"]}>Game Server</Text>
            </Center>
          </Flex>
        </GridItem>
        <GridItem order={[0, 0, 6]}>
          <Center
            ref={user}
            w={[160, 200, 200]}
            h={[160, 200, 200]}
            flexDir="column"
            position="relative"
            marginLeft={["50px", "50px", 0]}
          >
            <Icon
              as={BsFillPersonFill}
              w={[120, 120, 160]}
              h={[120, 120, 160]}
            ></Icon>
            <Text fontSize={["md", "md", "lg"]}>Game Designer</Text>
          </Center>
        </GridItem>
      </Grid>
      {!smallDiagram && (
        <>
          <Xarrow
            start={smartContract}
            end={gameClient}
            startAnchor="right"
            endAnchor={{ position: "left", offset: { y: 30 } }}
            path="grid"
            gridBreak="50%"
            dashness={true}
            {...xarrowStyle}
          />
          <Xarrow
            start={smartContract}
            end={adminDashboard}
            startAnchor={{ position: "bottom", offset: { x: -125 } }}
            endAnchor="top"
            path="straight"
            {...xarrowStyle}
          />
          <Xarrow
            start={smartContract}
            end={gameServer}
            startAnchor={{ position: "bottom", offset: { x: 100 } }}
            endAnchor={{ position: "left", offset: { y: 40 } }}
            path="grid"
            gridBreak="100%"
            {...xarrowStyle}
          />
          <Xarrow
            start={adminDashboard}
            end={user}
            startAnchor={{ position: "bottom", offset: { x: 5 } }}
            endAnchor="top"
            path="straight"
            {...xarrowStyle}
          />
        </>
      )}
      {smallDiagram && (
        <>
          <Xarrow
            start={smartContract}
            end={gameClient}
            startAnchor={{ position: "right", offset: { y: 10 } }}
            endAnchor="right"
            path="grid"
            gridBreak="0%"
            dashness={true}
            {...xarrowStyle}
          />
          <Xarrow
            start={smartContract}
            end={gameServer}
            startAnchor="left"
            endAnchor={{ position: "left", offset: { y: 10 } }}
            path="grid"
            gridBreak="0%"
            {...xarrowStyle}
          />
          <Xarrow
            start={smartContract}
            end={adminDashboard}
            startAnchor={{ position: "right", offset: { y: -10 } }}
            endAnchor="right"
            path="grid"
            gridBreak="0%"
            {...xarrowStyle}
          />
          <Xarrow
            start={adminDashboard}
            end={user}
            startAnchor={{ position: "top", offset: { x: -7 } }}
            endAnchor="bottom"
            path="straight"
            {...xarrowStyle}
          />
        </>
      )}
    </>
  );
};

const EngineOverviewDiagram = chakra(_EngineOverviewDiagram);

export default EngineOverviewDiagram;
