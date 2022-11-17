import React from "react";
import { Stack, Checkbox } from "@chakra-ui/react";

const CheckboxGroupped = ({
  groupName,
  list,
  isItemChecked,
  setItemChecked,
  isAllChecked,
  setAll,
  isIndeterminate,
  getName,
}) => {
  return (
    <Stack>
      <Checkbox
        isChecked={isAllChecked}
        isIndeterminate={isIndeterminate}
        onChange={() => setAll(!isAllChecked)}
        borderColor="gray.500"
      >
        {groupName}
      </Checkbox>
      <Stack pl={6} spacing={0}>
        {list.map((listItem, idx) => {
          return (
            <Stack
              px={2}
              key={`list-item-checkbox-${idx}`}
              direction="row"
              bgColor={idx % 2 == 0 ? "black.400" : "black.300"}
            >
              <Checkbox
                isChecked={isItemChecked(listItem)}
                onChange={(e) => setItemChecked(listItem, e.target.checked)}
                colorScheme="blue"
                borderColor="gray.500"
              >
                {getName(listItem)}
              </Checkbox>
            </Stack>
          );
        })}
      </Stack>
    </Stack>
  );
};

export default CheckboxGroupped;
