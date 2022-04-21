import { React } from "react";
import {
  Flex,
  Image,
  Link,
  LinkBox,
  LinkOverlay,
  chakra,
} from "@chakra-ui/react";

const TrustedBadge = ({
  name,
  caseURL,
  ImgURL,
  scale,
  isGrayScale,
  boxURL,
  invertColors,
  ...props
}) => {
  const _scale = scale ?? 1;
  const _isGrayScale = isGrayScale ? "grayscale(100%)" : "";
  const _invert = invertColors ? "invert(100%)" : "";
  const filterStr = _isGrayScale + " " + _invert;
  return (
    <LinkBox m={2} borderRadius="md" {...props}>
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
            sx={{ filter: filterStr }}
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
export default chakra(TrustedBadge);
