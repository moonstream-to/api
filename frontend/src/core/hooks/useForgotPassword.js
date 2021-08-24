import { useEffect } from "react";
import { useMutation } from "react-query";
import { AuthService } from "../../core/services";
import { useAuthResultHandler } from "./";
import { useToast } from ".";

const useForgotPassword = () => {
  const toast = useToast();
  const {
    mutate: forgotPassword,
    isLoading,
    error,
    data,
  } = useMutation(AuthService.forgotPassword);
  useAuthResultHandler(
    data,
    error,
    "Please check your inbox for verification URL."
  );
  useEffect(() => {
    if (error?.response?.data?.detail) {
      toast(error.response.data.detail, "error");
    }
  }, [error, toast, data]);

  return { forgotPassword, isLoading, data };
};

export default useForgotPassword;
