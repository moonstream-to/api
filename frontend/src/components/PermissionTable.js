
import { jsx } from "@emotion/react";
import { useState } from "react";
import {
  Checkbox,
  VStack,
  Table,
  Tr,
  Td,
  Th,
  Tbody,
  Thead,
  HStack,
  Select,
  FormControl,
  FormErrorMessage,
  Button,
  Box,
  Text,
  Flex,
  Link,
} from "@chakra-ui/react";
import { IconButton } from ".";
import { CloseIcon, DeleteIcon } from "@chakra-ui/icons";
import { useForm } from "react-hook-form";
import { TiGroupOutline } from "react-icons/ti";
import { IoIosJournal } from "react-icons/io";
import { useRouter, useGroups, useJournalPermissions } from "../core/hooks";
import RouterLink from "next/link";

const PermissionTable = ({ id, user, LoadingSpinner, setDeleteAlert }) => {
  const router = useRouter();
  const { handleSubmit, errors, register } = useForm();
  const [showNewHolderForm, toggleNewHolder] = useState(false);
  const { data: groups } = useGroups();
  const { appScope } = router.params;

  const {
    holders,
    error,
    setJournalPermissionMutation,
    removeJournalPermissionMutation,
    currentUserPermissions,
  } = useJournalPermissions(id, "personal");

  const checkboxToggled = (holder, value) => {
    return holder.permissions.includes(value)
      ? removePermissions({
          holder_id: holder.holder_id,
          holder_type: holder.holder_type,
          permission_list: [value],
        })
      : addPermissions({
          holder_id: holder.holder_id,
          holder_type: holder.holder_type,
          permission_list: [value],
        });
  };

  if (error) {
    return (
      <Box>
        It seems you have no permissions to open this page
        <RouterLink
          href={{
            pathname: `/app/${appScope}/${id}`,
            query: router.query,
          }}
          passHref
        >
          <Button
            as={Link}
            m={8}
            variant="solid"
            colorScheme="primary"
            leftIcon={<IoIosJournal />}
          >
            Back to the journal
          </Button>
        </RouterLink>
      </Box>
    );
  }

  if (!currentUserPermissions || !holders || !groups) return <LoadingSpinner />;

  const removePermissions = (formData) => {
    formData.permission_list = formData.permission_list.filter(Boolean);
    removeJournalPermissionMutation.removeJournalPermission({
      holder_type: "group",
      ...formData,
    });
  };

  const addPermissions = (formData) => {
    formData.permission_list = formData.permission_list.filter(Boolean);
    toggleNewHolder(false);

    setJournalPermissionMutation.setJournalPermission({
      holder_type: "group",
      ...formData,
    });
  };

  if (
    !currentUserPermissions.includes("journals.update") &&
    showNewHolderForm
  ) {
    toggleNewHolder(false);
  }

  return (
    <VStack>
      <form onSubmit={handleSubmit(addPermissions)}>
        <Table
          width="100%"
          variant="simple"
          colorScheme="primary"
          p={0}
          m={0}
          textColor="inherit"
        >
          <Thead>
            <Tr>
              <Th
                textColor="inherit"
                borderRightWidth="1px"
                textAlign="center"
                colSpan="2"
              >
                Holder
              </Th>
              <Th borderRightWidth="1px" textAlign="center" colSpan="3">
                Journals
              </Th>
              <Th borderRightWidth="1px" textAlign="center" colSpan="4">
                Entries
              </Th>
              <Th>Actions</Th>
            </Tr>
            <Tr>
              <Th textAlign="center" width="200px" px={1}>
                name
              </Th>
              <Th textAlign="center" px={1} borderRightWidth="1px">
                type
              </Th>
              <Th textAlign="center" px={1}>
                Read
              </Th>
              <Th textAlign="center" px={1}>
                Update
              </Th>
              <Th textAlign="center" px={1} borderRightWidth="1px">
                Delete
              </Th>
              <Th textAlign="center" px={1}>
                Read
              </Th>
              <Th textAlign="center" px={1}>
                Create
              </Th>
              <Th textAlign="center" px={1}>
                Update
              </Th>
              <Th textAlign="center" px={1}>
                Delete
              </Th>
              <Th textAlign="center" width="140px" px={1}></Th>
            </Tr>
          </Thead>
          <Tbody>
            {holders.map((holder, idx) => {
              const index = groups.findIndex(
                (item) => item.group_id === holder.holder_id
              );
              const name =
                index !== -1
                  ? groups[index]?.group_name
                  : holder.holder_id === user?.user_id
                  ? user?.username
                  : null;
              return (
                <Tr
                  bgColor={name ? "white.100" : "gray.50"}
                  key={`row-${idx}`}
                  borderColor="white.200"
                >
                  <Td textAlign="center">
                    {name ? (
                      name
                    ) : (
                      <Text fontSize="xx-small">{holder.holder_id}</Text>
                    )}
                  </Td>
                  <Td textAlign="center">{holder.holder_type}</Td>
                  <Td>
                    <Checkbox
                      isDisabled={
                        !name ||
                        !currentUserPermissions.includes("journals.update")
                      }
                      onChange={() => checkboxToggled(holder, "journals.read")}
                      isChecked={holder.permissions.includes("journals.read")}
                    ></Checkbox>
                  </Td>
                  <Td>
                    <Checkbox
                      isDisabled={
                        !name ||
                        !currentUserPermissions.includes("journals.update")
                      }
                      isChecked={holder.permissions.includes("journals.update")}
                      onChange={() =>
                        checkboxToggled(holder, "journals.update")
                      }
                    ></Checkbox>
                  </Td>
                  <Td>
                    <Checkbox
                      isDisabled={
                        !name ||
                        !currentUserPermissions.includes("journals.update")
                      }
                      isChecked={holder.permissions.includes("journals.delete")}
                      onChange={() =>
                        checkboxToggled(holder, "journals.delete")
                      }
                    ></Checkbox>
                  </Td>
                  <Td>
                    <Checkbox
                      isDisabled={
                        !name ||
                        !currentUserPermissions.includes("journals.update")
                      }
                      isChecked={holder.permissions.includes(
                        "journals.entries.read"
                      )}
                      onChange={() =>
                        checkboxToggled(holder, "journals.entries.read")
                      }
                    ></Checkbox>
                  </Td>
                  <Td>
                    <Checkbox
                      isDisabled={
                        !name ||
                        !currentUserPermissions.includes("journals.update")
                      }
                      isChecked={holder.permissions.includes(
                        "journals.entries.create"
                      )}
                      onChange={() =>
                        checkboxToggled(holder, "journals.entries.create")
                      }
                    ></Checkbox>
                  </Td>
                  <Td>
                    <Checkbox
                      isDisabled={
                        !name ||
                        !currentUserPermissions.includes("journals.update")
                      }
                      isChecked={holder.permissions.includes(
                        "journals.entries.update"
                      )}
                      onChange={() =>
                        checkboxToggled(holder, "journals.entries.update")
                      }
                    ></Checkbox>
                  </Td>
                  <Td>
                    <Checkbox
                      isDisabled={
                        !name ||
                        !currentUserPermissions.includes("journals.update")
                      }
                      isChecked={holder.permissions.includes(
                        "journals.entries.delete"
                      )}
                      onChange={() =>
                        checkboxToggled(holder, "journals.entries.delete")
                      }
                    ></Checkbox>
                  </Td>
                  <Td>
                    <IconButton
                      hidden={
                        !name ||
                        !currentUserPermissions.includes("journals.update")
                      }
                      onClick={() =>
                        removePermissions({
                          holder_id: holder.holder_id,
                          holder_typ: holder.holder_type,
                          permission_list: [
                            "journals.read",
                            "journals.delete",
                            "journals.entries.read",
                            "journals.entries.create",
                            "journals.entries.update",
                            "journals.entries.delete",
                            "journals.update",
                          ],
                        })
                      }
                      icon={<CloseIcon />}
                    />
                  </Td>
                </Tr>
              );
            })}
            {showNewHolderForm && (
              <Tr width="100%">
                <Td>
                  <FormControl isInvalid={errors.groupName}>
                    <Select
                      _focus={{
                        outline: "solid 1px",
                        outlineColor: "primary.500",
                      }}
                      fontSize="sm"
                      border="none"
                      placeholder="Select a team"
                      name="holder_id"
                      // width="200px"
                      height="fit-content"
                      bgColor="white.200"
                      ref={(e) => {
                        register(e, {
                          required: "Please select a group",
                        });
                      }}
                    >
                      {groups.map((group, idx) => {
                        if (
                          !holders.some((i) => i.holder_id === group.group_id)
                        ) {
                          return (
                            <option key={idx} value={group.group_id}>
                              {group.group_name}
                            </option>
                          );
                        }
                        return null;
                      })}
                    </Select>
                    <FormErrorMessage color="unsafe.400" pl="1">
                      {errors.groupName && errors.groupName.message}
                    </FormErrorMessage>
                  </FormControl>
                </Td>
                <Td>{/* <Checkbox /> */}</Td>
                <Td>
                  <Checkbox
                    type="checkbox"
                    name="permission_list[0]"
                    value="journals.read"
                    defaultValue={null}
                    defaultChecked={false}
                    ref={register}
                  />
                </Td>
                <Td>
                  <Checkbox
                    type="checkbox"
                    name="permission_list[1]"
                    value="journals.update"
                    defaultChecked={false}
                    ref={register}
                  />
                </Td>
                <Td>
                  <Checkbox
                    type="checkbox"
                    name="permission_list[2]"
                    value="journals.delete"
                    defaultChecked={false}
                    ref={register}
                  />
                </Td>
                <Td>
                  <Checkbox
                    type="checkbox"
                    name="permission_list[3]"
                    value="journals.entries.read"
                    defaultChecked={false}
                    ref={register}
                  />
                </Td>
                <Td>
                  <Checkbox
                    type="checkbox"
                    name="permission_list[4]"
                    value="journals.entries.create"
                    defaultChecked={false}
                    ref={register}
                  />
                </Td>
                <Td>
                  <Checkbox
                    type="checkbox"
                    name="permission_list[5]"
                    value="journals.entries.update"
                    defaultChecked={false}
                    ref={register}
                  />
                </Td>
                <Td>
                  <Checkbox
                    type="checkbox"
                    name="permission_list[6]"
                    value="journals.entries.delete"
                    defaultChecked={false}
                    ref={register}
                  />
                </Td>
                <Td>
                  <HStack>
                    <IconButton
                      onClick={() => toggleNewHolder(false)}
                      icon={<CloseIcon />}
                    />
                    <IconButton type="submit" />
                  </HStack>
                </Td>
              </Tr>
            )}
          </Tbody>
        </Table>
      </form>
      <Flex
        direction="row"
        py={4}
        alignContent="baseline"
        width="100%"
        justifyContent="center"
      >
        <RouterLink
          href={{
            pathname: `/app/${appScope}/${id}`,
            query: router.query,
          }}
          passHref
        >
          <Button
            as={Link}
            variant="solid"
            colorScheme="primary"
            leftIcon={<IoIosJournal />}
          >
            Back to the journal
          </Button>
        </RouterLink>
        {currentUserPermissions.includes("journals.update") && (
          <Button
            variant="solid"
            colorScheme="primary"
            disabled={showNewHolderForm}
            hidden={!currentUserPermissions.includes("journals.update")}
            onClick={() => toggleNewHolder(true)}
            leftIcon={<TiGroupOutline />}
          >
            Add a team
          </Button>
        )}
        {currentUserPermissions.includes("journals.delete") && (
          <Button
            variant="solid"
            colorScheme="unsafe"
            hidden={!currentUserPermissions.includes("journals.delete")}
            onClick={() => setDeleteAlert(true)}
            leftIcon={<DeleteIcon />}
          >
            Delete this journal
          </Button>
        )}
      </Flex>
    </VStack>
  );
};
export default PermissionTable;
