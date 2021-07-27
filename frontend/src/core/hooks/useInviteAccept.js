import { InvitesService } from "../services";
import { useToast } from ".";

const useInviteAccept = () => {
  const toast = useToast();

  const inviteAccept = (invite_code) => {
    InvitesService.accept(invite_code)
      .then(
        () => toast("You were successfully added to the team", "success"),
        (reason) => {
          toast(reason, "error");
        }
      )
      .finally(window.sessionStorage.clear("invite_code"))
      .catch((error) => {
        console.error("Error during sending an invite link:", error);
      });
  };

  return { inviteAccept };
};

export default useInviteAccept;
