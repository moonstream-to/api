import { useEffect } from "react";
import { useToast } from "./";

const useAuthResultHandler = (data, error, success, rejection) => {
  const toast = useToast();

  useEffect(() => {
    if (error && rejection) return toast(rejection, "error");
    if (error?.response?.data?.detail)
      return toast(error.response.data.detail, "error");
    if (data && success) return toast(success, "success");
    // eslint-disable-next-line
  }, [error, toast, data]);
};

export default useAuthResultHandler;
