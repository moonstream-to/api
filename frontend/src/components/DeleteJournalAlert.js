
import { jsx } from "@emotion/react";
import {
  Button,
  AlertDialog,
  AlertDialogBody,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogContent,
  AlertDialogOverlay,
} from "@chakra-ui/react";
import { useRouter, useDeleteJournal } from "../core/hooks";

const DeleteJournalAlert = ({ isOpen, toggleSelf, cancelRef }) => {
  const router = useRouter();
  const { id } = router.params;
  const { deleteJournal } = useDeleteJournal(id);

  const deleteJournalConfirm = () => {
    deleteJournal(id);
    toggleSelf(false);
    router.replace("/app/personal/");
  };

  return (
    <AlertDialog
      isOpen={isOpen}
      leastDestructiveRef={cancelRef}
      onClose={() => toggleSelf(false)}
    >
      <AlertDialogOverlay backgroundColor="white.50">
        <AlertDialogContent bg="solid" backgroundColor="white.100">
          <AlertDialogHeader fontSize="lg" fontWeight="bold">
            Delete this journal
          </AlertDialogHeader>

          <AlertDialogBody>
            {`Are you sure? You can't undo this action afterwards.`}
          </AlertDialogBody>

          <AlertDialogFooter>
            <Button
              ref={cancelRef}
              onClick={() => toggleSelf(false)}
              variant="outline"
              colorScheme="primary"
            >
              Cancel
            </Button>
            <Button
              variant="solid"
              colorScheme="unsafe"
              onClick={() => deleteJournalConfirm()}
              ml={3}
            >
              Delete
            </Button>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialogOverlay>
    </AlertDialog>
  );
};

export default DeleteJournalAlert;
