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
import { BsFillPersonFill, BsFillFileEarmarkCodeFill } from "react-icons/bs";
import Xarrow from "react-xarrows";
import ExampleCode from "./ExampleCode";

const _EngineOverviewDiagram = (props) => {
  const smartContract = useRef(null);
  const gameClient = useRef(null);
  const adminDashboard = useRef(null);
  const gameServer = useRef(null);
  const user = useRef(null);

  const xarrowStyle = {
    color: "#FF8B73",
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

  return (
    <>
      <Grid
        templateRows={["repeat(7)", "repeat(7)", "repeat(2, 1fr)"]}
        templateColumns={["repeat(1, 1fr)", "repeat(1, 1fr)", "repeat(3, 1fr)"]}
        rowGap={[10, 10, 20]}
        columnGap={4}
      >
        <GridItem
          h={["80px", "80px", "auto"]}
          order={[2, 2, 0]}
          display="inline-grid"
          justifyItems="center"
          alignItems="center"
        >
          <Flex
            ref={smartContract}
            w={["260px", "260px", "400px"]}
            h={["73", "73", "130px"]}
            position="relative"
          >
            <RoundedRectSVG scaling={1.0} />
            <Center
              position="absolute"
              left="0"
              top="0"
              w={["260px", "260px", "400px"]}
              h="130px"
            >
              <VStack justifyContent="center" py="10px">
                <Text fontSize={["md", "md", "xl"]} fontWeight="semibold">
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
        <GridItem h={0} order={[6, 6, 4]}></GridItem>
        <GridItem
          h={["160px", "160px", "auto"]}
          order={[4, 4, 2]}
          display="inline-grid"
          justifyItems="center"
          alignItems="center"
        >
          <Flex
            ref={gameClient}
            w={["155px", "155px", "189px"]}
            h={["160px", "160px", "205px"]}
            position="relative"
          >
            <RectangleSVG></RectangleSVG>
            <Center
              position="absolute"
              left="0"
              top={["50px", "50px", "30px", null]}
              w={["155px", "155px", "189px"]}
              h={["160px", "160px", "205px"]}
            >
              <Text fontSize={["md", "md", "xl"]} fontWeight="semibold">
                Game Client
              </Text>
            </Center>
          </Flex>
        </GridItem>
        <GridItem
          h={["160px", "160px", "auto"]}
          order={[1, 1, 3]}
          display="inline-grid"
          justifyItems="center"
          alignItems="center"
        >
          <Center
            ref={adminDashboard}
            w={["155px", "155px", "220px"]}
            h={["160px", "160px", "240px"]}
            position="relative"
          >
            <RectangleSVG scaling={1.2}></RectangleSVG>
            <Center
              position="absolute"
              w={["155px", "155px", "220px"]}
              h={["160px", "160px", "240px"]}
            >
              <VStack
                w={["155px", "155px", "220px"]}
                h={["160px", "160px", "240px"]}
                justifyContent="center"
              >
                <Text fontSize={["md", "md", "lg"]} fontWeight="semibold">
                  Admin Dashboard
                </Text>
                {!smallDiagram && (
                  <Text pt="10px" pl={[0, 0, "20px"]} fontSize="md">
                    Choose mechanics at engine.moonstream.to
                  </Text>
                )}
              </VStack>
            </Center>
          </Center>
        </GridItem>
        <GridItem
          order={[3, 3, 1]}
          display="inline-grid"
          justifyItems="center"
          alignItems="center"
          marginTop={10}
        >
          <Center>
            <Flex
              w={["155px", "155px", "189px"]}
              h={[null, null, "205px"]}
              justifyContent="center"
              position="relative"
            >
              <Popover>
                <PopoverTrigger placement="top">
                  <Flex>
                    <Icon
                      as={BsFillFileEarmarkCodeFill}
                      w={50}
                      h={50}
                      onClick={() => {
                        props.buttonReport(
                          "Example Code",
                          "engine-overview-diagram",
                          "landing"
                        );
                      }}
                    ></Icon>{" "}
                  </Flex>
                </PopoverTrigger>
                <PopoverContent w={["300px", "400px", "850px"]}>
                  <PopoverBody>
                    <ExampleCode />
                  </PopoverBody>
                </PopoverContent>
              </Popover>
            </Flex>
          </Center>
        </GridItem>
        <GridItem
          h={["120px", "120px", "auto"]}
          order={[5, 5, 5]}
          display="inline-grid"
          justifyItems="center"
          alignItems="center"
        >
          <Flex
            ref={gameServer}
            w={["200px", "200px", "305px"]}
            h={["120px", "120px", "188px"]}
            position="relative"
          >
            <CloudSVG scaling={0.8}></CloudSVG>
            <Center
              position="absolute"
              pt={["80px", "80px", "30px", null]}
              w={["200px", "200px", "305px"]}
              h={["120px", "120px", "188px"]}
            >
              <Text fontSize={["md", "md", "lg"]} fontWeight="semibold">
                Game Server
              </Text>
            </Center>
          </Flex>
        </GridItem>
        <GridItem
          order={[0, 0, 6]}
          display="inline-grid"
          justifyItems="center"
          alignItems="center"
        >
          <Center
            ref={user}
            w={[160, 200, 200]}
            h={[160, 200, 200]}
            flexDir="column"
            position="relative"
          >
            <Icon
              as={BsFillPersonFill}
              w={[120, 120, 160]}
              h={[120, 120, 160]}
            ></Icon>
            <Text fontSize={["md", "md", "lg"]} fontWeight="semibold">
              Game Designer
            </Text>
          </Center>
        </GridItem>
      </Grid>
      {!smallDiagram && (
        <>
          <Xarrow
            start={smartContract}
            end={gameClient}
            startAnchor="right"
            endAnchor="left"
            path="straight"
            gridBreak="50%"
            dashness={true}
            {...xarrowStyle}
          />
          <Xarrow
            start={smartContract}
            end={adminDashboard}
            startAnchor="bottom"
            endAnchor="top"
            path="straight"
            {...xarrowStyle}
          />
          <Xarrow
            start={smartContract}
            end={gameServer}
            startAnchor={{ position: "bottom", offset: { x: 150 } }}
            endAnchor={{ position: "left", offset: { y: 40 } }}
            path="straight"
            {...xarrowStyle}
          />
          <Xarrow
            start={adminDashboard}
            end={user}
            startAnchor="bottom"
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
            startAnchor="top"
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
