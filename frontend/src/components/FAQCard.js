import { React } from "react";
import {
  chakra,
  AccordionButton,
  AccordionPanel,
  Heading,
  Box,
  AccordionItem,
} from "@chakra-ui/react";
import { AddIcon, MinusIcon } from "@chakra-ui/icons";

const _FAQCard = ({ heading, headingProps, panelContent }) => {
  const iconColor = "#F56646";

  return (
    <AccordionItem>
      {({ isExpanded }) => (
        <>
          <AccordionButton>
            <Box flex="1" textAlign="left" pr="10px">
              <Heading
                {...headingProps}
                as="h3"
                fontSize={["lg", "2xl", "3xl"]}
              >
                {heading}
              </Heading>
            </Box>
            {isExpanded ? (
              <MinusIcon color={iconColor} fontSize="12px" />
            ) : (
              <AddIcon color={iconColor} fontSize="12px" />
            )}
          </AccordionButton>
          <AccordionPanel
            pb={4}
            fontSize={["md", "lg", "xl", "2xl", "3xl", "3xl"]}
          >
            {panelContent}
          </AccordionPanel>
        </>
      )}
    </AccordionItem>
  );
};

const FAQCard = chakra(_FAQCard);

export default FAQCard;
