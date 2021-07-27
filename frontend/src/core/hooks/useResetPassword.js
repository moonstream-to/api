import { useMutation } from "react-query";
import { AuthService } from "../../core/services";
import { useAuthResultHandler, useLogin } from "./";

const useResetPassword = () => {
  const { login, isLoading: loginLoading, data: loginData } = useLogin();
  // const toast = useToast()

  const [reset, { isLoading: resetLoading, error, data }] = useMutation(
    AuthService.resetPassword,
    {
      onSuccess: (userInfo, variables) => {
        login({
          username: userInfo.data.username,
          password: variables.newPassword,
        });
      },
      onError: () => {},
    }
  );

  useAuthResultHandler(
    data,
    error,
    "Your password has been successfully changed"
  );

  const isLoading = loginLoading || resetLoading;
  return { reset, isLoading, data, loginData };
};

export default useResetPassword;
