
import { jsx } from "@emotion/react";
import { GridItem } from "@chakra-ui/react";
import { Heading, Text, Image } from "@chakra-ui/react";
import { Fragment } from "react";

const Block = (content) => {
  const TitleRef = content.PrevTitle
    ? `#${content.PrevTitle}-${content.title}`
    : `#${content.title}`;

  var HeaderStyle = content.PrevTitle
    ? { as: "h2", fontSize: "3xl" }
    : { as: "h1", fontSize: "4xl" };

  return (
    <Fragment>
      {content.title && (
        <GridItem colSpan="12" px="8.3%" py={1} textAlign="center">
          <Heading
            id={TitleRef}
            pt={16}
            pb={4}
            fontWeight="200"
            {...HeaderStyle}
          >
            {content.title}
          </Heading>
        </GridItem>
      )}
      {content.body.map((element, idx) => {
        if ("text" in element) {
          return (
            <GridItem key={idx} colSpan="10" px="8.3%" py={1}>
              {element.text.map((paragraph, idx) => {
                return (
                  <Text key={idx} py={2} fontSize="xl">
                    {paragraph}
                  </Text>
                );
              })}
            </GridItem>
          );
        }
        if ("image" in element) {
          return (
            <GridItem key={idx} colSpan="10" py={1} justifySelf="center">
              <Image
                justifySelf="center"
                key={idx}
                maxHeight="48rem"
                src={element.image.path}
                alt={element.image.annotation}
              />
            </GridItem>
          );
        }
        if ("title" in element) {
          element.PrevTitle = content.title;
          return <Block key={idx} {...element} />;
        }
        return "";
      })}
    </Fragment>
  );
};
export default Block;
