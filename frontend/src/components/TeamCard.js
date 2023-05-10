import React from "react";
import {
  Heading,
  Avatar,
  Box,
  Center,
  Text,
  Stack,
  Badge,
  useColorModeValue,
} from "@chakra-ui/react";

export default function SocialProfileSimple({
  avatarURL,
  avatarAlt,
  name,
  atName,
  content,
  badges,
  isOnline,
  buttons,
}) {
  const badgeBg = useColorModeValue("gray.50", "gray.800");
  return (
    <Center py={6}>
      <Box
        maxW={"320px"}
        h="420px"
        w={"full"}
        borderRadius="20px"
        border="1px solid white"
        p={6}
        textAlign={"center"}
      >
        <Avatar
          size={"xl"}
          src={avatarURL}
          alt={avatarAlt}
          mb={4}
          pos={"relative"}
          bg="white"
          _after={
            isOnline && {
              content: '""',
              w: 4,
              h: 4,
              bg: "green.300",
              border: "2px solid white",
              rounded: "full",
              pos: "absolute",
              bottom: 0,
              right: 3,
            }
          }
        />
        <Heading fontSize={"2xl"} fontFamily={"body"}>
          {name}
        </Heading>
        <Text fontWeight={600} color={"blue.850"} mb={4}>
          {atName}
        </Text>
        <Text textAlign={"center"} px={3}>
          {content}
        </Text>

        <Stack align={"center"} justify={"center"} direction={"row"} mt={6}>
          {badges &&
            badges.map((badgeContent, idx) => (
              <Badge
                key={`badge-card-${name}-${idx}`}
                px={2}
                py={1}
                bg={badgeBg}
                fontWeight={"400"}
              >
                {badgeContent}
              </Badge>
            ))}
        </Stack>

        <Stack mt={8} direction={"row"} spacing={4}>
          {buttons}
        </Stack>
      </Box>
    </Center>
  );
}
