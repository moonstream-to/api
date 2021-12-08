import React from "react";
import { Stack, Checkbox } from "@chakra-ui/react";
import { v4 } from "uuid";

const CheckboxGroupped = ({
  groupName,
  list,
  isItemChecked,
  setItemChecked,
  isAllChecked,
  setAll,
  isIndeterminate,
}) => {
  return (
    <Stack>
      <Checkbox
        isChecked={isAllChecked}
        isIndeterminate={isIndeterminate}
        onChange={() => setAll(!isAllChecked)}
      >
        {groupName}
      </Checkbox>
      <Stack pl={6} spacing={0}>
        {list.map((listItem, idx) => {
          return (
            <Stack
              px={2}
              key={v4()}
              direction="row"
              bgColor={idx % 2 == 0 ? "gray.50" : "gray.100"}
            >
              <Checkbox
                isChecked={isItemChecked(listItem)}
                onChange={(e) => setItemChecked(listItem, e.target.checked)}
              >
                {listItem.name}
              </Checkbox>
            </Stack>
          );
        })}
      </Stack>
    </Stack>
  );
};

export default CheckboxGroupped;
