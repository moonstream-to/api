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
      gap="20px"
      {...props}
    >
      <Image
        src={img}
        w={["290px", "290px", "200px"]}
        h={["290px", "290px", "200px"]}
        borderRadius={["10px", "10px", "20px"]}
        cursor="pointer"
        onClick={() => {
          window.open(href);
        }}
      />
      <Flex direction="column" gap="20px">
        <Text
          fontSize={["24px", "24px", "24px"]}
          fontWeight="700"
          maxW="500px"
          lineHeight="120%"
        >
          {title}
        </Text>
        <Flex direction="column" gap={["5px", "5px", "10px"]}>
          {date && (
            <Text fontSize={["14px", "14px", "16px"]} lineHeight="20px">
              {date}
            </Text>
          )}
          <Text fontSize={["16px", "16px", "18px"]} lineHeight="23px">
            {text}
          </Text>
          <Text
            href={href}
            maxW="fit-content"
            color="orange.1000"
            cursor="pointer"
            fontSize={["16px", "16px", "18px"]}
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
    </Flex>
  );
};

export default WhitepaperCard;
