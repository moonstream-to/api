import { useContext } from "react";
import { useMutation, useQueryClient } from "react-query";
import { useUser, useRouter } from ".";
import UIContext from "../providers/UIProvider/context";
import { AuthService } from "../services";

const useLogout = () => {
  const { setLoggingOut } = useContext(UIContext);
  const router = useRouter();
  const cache = useQueryClient();
  const { mutate: logout } = useMutation(AuthService.revoke, {
    onMutate: () => {
      setLoggingOut(true);
    },
    onSuccess: () => {
      router.push("/");
      setUser(null);
      localStorage.removeItem("MOONSTREAM_ACCESS_TOKEN");
      cache.clear();
    },
  });
  const { setUser } = useUser();

  return {
    logout,
  };
};

export default useLogout;
