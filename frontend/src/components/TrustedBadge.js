import { React } from "react";
import { Flex, Image, Link, LinkBox, LinkOverlay } from "@chakra-ui/react";

const TrustedBadge = ({
  name,
  caseURL,
  ImgURL,
  scale,
  isGrayScale,
  boxURL,
}) => {
  const _scale = scale ?? 1;
  return (
    <LinkBox m={2} bgColor="blue.300" borderRadius="md">
      <LinkOverlay href={boxURL} isExternal>
        <Flex
          m={1}
          justifyContent="center"
          alignItems="center"
          alignSelf="center"
          wrap="nowrap"
          p={8}
          direction="column"
        >
          <Image
            sx={isGrayScale && { filter: "grayscale(100%)" }}
            h={[
              `${2.25 * _scale}rem`,
              null,
              `${3 * _scale}rem`,
              `${3 * _scale}rem`,
              `${4 * _scale}rem`,
              `${6 * _scale}rem`,
            ]}
            src={ImgURL}
            alt={name}
          ></Image>
          {caseURL && (
            // <RouterLink href={caseURL} passHref scroll={true}>
            <Link
              fontSize={["sm", null, "md", "lg"]}
              textColor="orange.900"
              href={caseURL}
            >
              {`Read more >`}
            </Link>
            // </RouterLink>
          )}
        </Flex>
      </LinkOverlay>
    </LinkBox>
  );
};
export default TrustedBadge;
