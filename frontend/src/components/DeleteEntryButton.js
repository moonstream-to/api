
import { jsx } from "@emotion/react";
import { Fragment, useCallback } from "react";
import {
  Popover,
  PopoverTrigger,
  PopoverContent,
  PopoverCloseButton,
  PopoverHeader,
  PopoverFooter,
  PopoverBody,
  Button,
} from "@chakra-ui/react";
import { useDeleteEntry, useRouter } from "../core/hooks";

const DeleteEntryButton = ({ id, journalId, appScope }) => {
  const router = useRouter();
  const deleteEntry = useDeleteEntry({
    entryId: id,
    journalId,
  });

  const onConfirm = useCallback(
    (onClose) => () => {
      deleteEntry();
      onClose();

      setTimeout(() => {
        router.push({
          pathname: `/app/${appScope}/${journalId}/entries`,
          query: router.query,
        });
      }, 1000);
    },
    [deleteEntry, journalId, appScope, router]
  );

  return (
    <Popover usePortal>
      {({ onClose }) => (
        <Fragment>
          <PopoverTrigger>
            <Button size="xs" variant="link" colorScheme="primary" ml={1}>
              Delete
            </Button>
          </PopoverTrigger>
          <PopoverContent zIndex={100} bg="White">
            <PopoverCloseButton />
            <PopoverHeader fontWeight="bold">Please confirm!</PopoverHeader>
            <PopoverBody fontSize="md">
              Are you sure you want to delete the entry ?
            </PopoverBody>
            <PopoverFooter>
              <Button
                onClick={onClose}
                colorScheme="primary"
                variant="outline"
                size="sm"
              >
                No
              </Button>
              <Button
                onClick={onConfirm(onClose)}
                colorScheme="unsafe"
                variant="solid"
                size="sm"
              >
                Yes
              </Button>
            </PopoverFooter>
          </PopoverContent>
        </Fragment>
      )}
    </Popover>
  );
};

export default DeleteEntryButton;
