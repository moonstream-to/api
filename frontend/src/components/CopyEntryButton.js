
import { jsx } from "@emotion/react";
import {
  Button,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  MenuGroup,
  MenuDivider,
} from "@chakra-ui/react";
import {
  useJournalEntry,
  useJournals,
  useRouter,
  useToast,
} from "../core/hooks";
import { EntryService } from "../core/services";
import { useQueryCache } from "react-query";

const CopyEntryButton = ({ id, journalId }) => {
  const router = useRouter();
  const cache = useQueryCache();
  const { appScope } = router.params;
  const { data: entryToCopy, isLoading: sourceIsLoading } = useJournalEntry(
    journalId,
    id,
    appScope
  );
  const toast = useToast();
  const { journalsCache } = useJournals();
  const copyEntry = async (targetJournalId) => {
    try {
      const newEntry = { ...entryToCopy };
      newEntry.title = "Copy of " + newEntry.title;
      await EntryService.create(targetJournalId)(newEntry).then((response) => {
        journalsCache.refetch();
        setTimeout(
          () => cache.refetchQueries(["journal-entries", { journalId }]),
          500
        );
        if (response.status === 200) {
          toast("Copied!", "success");
        }
      });
    } catch (e) {
      console.error(
        "Error copying entry. Please email engineering@bugout.dev if you encounter this issue.",
        e
      );
    }
  };

  if (journalsCache.isLoading || sourceIsLoading) return "";

  return (
    <Menu>
      <MenuButton
        as={Button}
        size="xs"
        variant="link"
        colorScheme="primary"
        ml={1}
      >
        Copy
      </MenuButton>
      <MenuList maxH="sm" overflow="scroll">
        <MenuGroup title="Destination:">
          <MenuItem value={journalId} onClick={() => copyEntry(journalId)}>
            {
              journalsCache?.data?.data?.journals?.filter(
                (journal) => journal.id === journalId
              )[0]?.name
            }
          </MenuItem>
          <MenuDivider />
          {journalsCache?.data?.data?.journals?.map((journal) => {
            if (journal.id === journalId) return "";
            return (
              <MenuItem
                key={`option-${journal.id}`}
                value={journal.id}
                onClick={() => copyEntry(journal.id)}
              >
                {journal.name}
              </MenuItem>
            );
          })}
        </MenuGroup>
      </MenuList>
    </Menu>
  );
};

export default CopyEntryButton;
