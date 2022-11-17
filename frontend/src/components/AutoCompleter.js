import React, { useContext } from "react";
import Downshift from "downshift";
import {
  Stack,
  Box,
  InputGroup,
  InputLeftAddon,
  Input,
  InputRightAddon,
  FormLabel,
} from "@chakra-ui/react";
import UIContext from "../core/providers/UIProvider/context";

const AutoCompleter = ({
  pickerItems,
  initialSelectedItem,
  itemToString,
  onSelect,
  getLabelColor,
  placeholder,
  filterFn,
  empyListCTA,
  dropdownItem,
  getLeftAddonColor,
  itemIdx,
  selectedItem,
  initialIsOpen,
}) => {
  const ui = useContext(UIContext);

  return (
    <Downshift
      onSelect={onSelect}
      itemToString={itemToString}
      initialInputValue={itemToString(initialSelectedItem)}
      selectedItem={selectedItem}
      initialIsOpen={initialIsOpen}
    >
      {({
        getInputProps,
        getItemProps,
        getLabelProps,
        getMenuProps,
        getToggleButtonProps,
        isOpen,
        inputValue,
        highlightedIndex,
        getRootProps,
        selectedItem,
      }) => {
        const labelColor = getLabelColor(selectedItem);
        const inputLeftBgColor = getLeftAddonColor(selectedItem);
        return (
          <Box pos="relative">
            <Box {...getRootProps({}, { suppressRefError: true })}>
              <InputGroup
                border="1px solid white"
                bg="black.300"
                borderRadius="7px"
              >
                <InputLeftAddon
                  borderStyle="none"
                  isTruncated
                  maxW="60px"
                  fontSize={ui.isMobileView ? "xs" : "sm"}
                  bgColor={inputLeftBgColor ?? "gray.100"}
                >
                  <FormLabel
                    alignContent="center"
                    my={2}
                    {...getLabelProps()}
                    color={
                      labelColor
                        ? labelColor?.isDark()
                          ? "white"
                          : labelColor.darken(0.6).hex()
                        : "inherit"
                    }
                  >{`#${itemIdx}:`}</FormLabel>
                </InputLeftAddon>

                <Input
                  variant="bw"
                  borderStyle="none none none"
                  borderLeft="1px solid white"
                  placeholder={placeholder}
                  isTruncated
                  fontSize="sm"
                  {...getInputProps({
                    // defaultValue: getDefaultValue(selectedItem),
                  })}
                ></Input>
                <InputRightAddon bg="black.300">
                  {" "}
                  <button
                    style={{ backgroundColor: "black.300" }}
                    {...getToggleButtonProps()}
                    aria-label={"toggle menu"}
                  >
                    &#8595;
                  </button>
                </InputRightAddon>
              </InputGroup>
            </Box>
            {isOpen ? (
              <Stack
                // display="flex"
                direction="column"
                className="menuListTim"
                {...getMenuProps()}
                bgColor="black.300"
                borderRadius="md"
                boxShadow="lg"
                pos="absolute"
                overflow="scroll"
                left={0}
                right={0}
                spacing={2}
                zIndex={1000}
                py={2}
              >
                {pickerItems &&
                  pickerItems.filter((item) => filterFn(item, inputValue))
                    .length === 0 &&
                  empyListCTA(inputValue)}
                {pickerItems &&
                  pickerItems
                    .filter((item) => filterFn(item, inputValue))
                    .map((item, index) => {
                      return (
                        <Stack
                          px={4}
                          py={1}
                          alignItems="center"
                          border="1px solid white"
                          key={`autocomplete-item-${index}`}
                          {...getItemProps({
                            index,
                            item,
                          })}
                          direction="row"
                          w="100%"
                          fontWeight={
                            index === highlightedIndex ? "600" : "inherit"
                          }
                        >
                          {dropdownItem(item)}
                        </Stack>
                      );
                    })}
              </Stack>
            ) : null}
            {/* </Menu> */}
          </Box>
        );
      }}
    </Downshift>
  );
};

export default AutoCompleter;
