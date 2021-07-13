/** @jsxRuntime classic */
/** @jsx jsx */
import { jsx } from "@emotion/react";
import { useState, useEffect } from "react";
import {
  HStack,
  Editable,
  EditablePreview,
  EditableInput,
} from "@chakra-ui/react";
const NameEditable = ({ team, rename }) => {
  const [name, setName] = useState(team.group_name);

  useEffect(() => {
    setName(team.group_name);
  }, [team.group_name]);

  const handleSubmit = () => {
    rename.renameGroup({ name, groupId: team.group_id });
  };

  return (
    <Editable
      selectAllOnFocus={true}
      overflow="hidden"
      maxWidth="100%"
      width="100%"
      height="auto"
      minH="36px"
      style={{ marginLeft: "0" }}
      m={0}
      p={0}
      fontWeight="600"
      fontSize="md"
      textAlign="left"
      isPreviewFocusable={true}
      submitOnBlur={true}
      onSubmit={() => handleSubmit()}
      value={name}
      onChange={(value) => setName(value)}
    >
      {() => (
        <HStack
          width="auto"
          maxWidth="calc(100%)"
          textOverflow="ellipsis"
          overflow="hidden"
        >
          <EditablePreview
            wordBreak="break-all"
            maxWidth="fit-content"
            width="fit-content"
            flex="auto"
            textOverflow="ellipsis"
            p={0}
            m={0}
          />
          <EditableInput
            wordBreak="break-all"
            maxWidth="calc(100% - 48px)"
            width="calc(100% - 48px)"
            flex="auto"
            textOverflow="ellipsis"
            p={0}
            _focus={{ outline: "none" }}
          />
        </HStack>
      )}
    </Editable>
  );
};

export default NameEditable;
