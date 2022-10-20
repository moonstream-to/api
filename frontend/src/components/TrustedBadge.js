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
  scaling,
  isGrayScale,
  boxURL,
  invertColors,
  ...props
}) => {
  const _scale = scaling ?? 1.0;
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
          p={[2, 3]}
          direction="column"
        >
          <Image
            sx={{ filter: filterStr }}
            h={[`${2.25 * _scale}rem`, `${3 * _scale}rem`, null]}
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
