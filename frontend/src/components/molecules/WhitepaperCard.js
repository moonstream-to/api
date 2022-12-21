import React from "react";
import { Flex, Image, Text } from "@chakra-ui/react";

const WhitepaperCard = ({ img, title, date = "", text, href, ...props }) => {
  return (
    <Flex
      direction={["column", "column", "row"]}
      alignItems={["center", "center", "start"]}
      p="20px"
      bg="#353535"
      borderRadius="20px"
      {...props}
    >
      <Image
        src={img}
        w={["150px", "150px", "200px"]}
        h={["150px", "150px", "200px"]}
        borderRadius={["10px", "10px", "20px"]}
        cursor="pointer"
        pb={["10px", "10px", "0px"]}
        onClick={() => {
          window.open(href);
        }}
      />
      <Flex direction="column" ml="20px">
        <Text
          fontSize={["18px", "18px", "24px"]}
          fontWeight="700"
          maxW="500px"
          lineHeight="120%"
          mb="10px"
        >
          {title}
        </Text>
        {date && (
          <Text fontSize={["12px", "12px", "16px"]} lineHeight="20px">
            {date}
          </Text>
        )}
        <Text fontSize={["14px", "14px", "18px"]} my="5px" lineHeight="23px">
          {text}
        </Text>
        <Text
          href={href}
          maxW="fit-content"
          color="orange.1000"
          cursor="pointer"
          fontSize={["14px", "14px", "18px"]}
          fontWeight="700"
          _hover={{ color: "#F4532F" }}
          onClick={() => {
            window.open(href);
          }}
        >
          Read more
        </Text>
      </Flex>
    </Flex>
  );
};

export default WhitepaperCard;
