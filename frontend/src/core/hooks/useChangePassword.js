import { useMutation } from "react-query";
import { useToast } from "./";
import { AuthService } from "../../core/services";

const useChangePassword = () => {
  const toast = useToast();

  const {
    mutate: changePassword,
    isLoading,
    data,
  } = useMutation(AuthService.changePassword, {
    onError: (error) => {
      toast(error, "error");
    },
    onSuccess: () => {
      toast("Your password has been successfully changed", "success");
    },
  });

  return { changePassword, isLoading, data };
};

export default useChangePassword;
