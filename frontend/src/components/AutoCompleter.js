import React, { useContext } from "react";
import Downshift from "downshift";
import { v4 } from "uuid";
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
              <InputGroup>
                <InputLeftAddon
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
                  placeholder={placeholder}
                  isTruncated
                  fontSize="sm"
                  {...getInputProps({
                    // defaultValue: getDefaultValue(selectedItem),
                  })}
                ></Input>
                <InputRightAddon>
                  {" "}
                  <button
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
                bgColor="gray.300"
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
                          key={v4()}
                          {...getItemProps({
                            index,
                            item,
                          })}
                          direction="row"
                          w="100%"
                          bgColor={
                            index === highlightedIndex
                              ? "orange.900"
                              : "inherit"
                          }
                          color={
                            index === highlightedIndex ? "gray.100" : "inherit"
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
