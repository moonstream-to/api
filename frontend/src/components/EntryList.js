
import { jsx } from "@emotion/react";
import { Fragment, useContext } from "react";
import { Flex, Heading, Text, LinkBox } from "@chakra-ui/react";
import moment from "moment";
import { EntryCard, TagsList, DeleteEntryButton, CopyEntryButton } from ".";
import { useRouter } from "../core/hooks";
import RouterLink from "next/link";
import UIContext from "../core/providers/UIProvider/context";

const EntryList = ({ entry, disableDelete, disableCopy }) => {
  const ui = useContext(UIContext);
  const router = useRouter();
  const { id: journalId, entryId, appScope } = router.params;

  return (
    <RouterLink
      href={{
        pathname: `/app/${appScope}/${journalId}/entries/${entry.id}`,
        query: router.query,
      }}
      passHref
    >
      <LinkBox
        onClick={() =>
          ui.setEntriesViewMode(ui.isMobileView ? "entry" : "split")
        }
      >
        <EntryCard isActive={entryId === entry.id ? true : false}>
          <Heading as="h3" fontWeight="500" fontSize="md">
            {entry.title}
          </Heading>
          <Flex alignItems="baseline">
            <Text opacity="0.5" fontSize="xs">
              {moment(entry.created_at).format("DD MMM, YYYY")}{" "}
            </Text>
            {entryId === entry.id && (
              <Fragment>
                {!disableDelete && (
                  <DeleteEntryButton
                    id={entryId}
                    journalId={journalId}
                    appScope={appScope}
                  />
                )}
                {!disableCopy && (
                  <CopyEntryButton id={entryId} journalId={journalId} />
                )}
              </Fragment>
            )}
          </Flex>
          <Flex align="start">
            <Flex
              width="100%"
              mt={2}
              align="center"
              justifyContent="space-between"
            >
              <TagsList tags={entry.tags} />
            </Flex>
          </Flex>
        </EntryCard>
      </LinkBox>
    </RouterLink>
  );
};

export default EntryList;
