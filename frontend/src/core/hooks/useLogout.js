import { useCallback, useContext } from "react";
import { useMutation, useQueryClient } from "react-query";
import { useUser, useRouter } from ".";
import UIContext from "../providers/UIProvider/context";
import { AuthService } from "../services";

const useLogout = () => {
  const { setLoggingOut } = useContext(UIContext);
  const router = useRouter();
  const { mutate: revoke } = useMutation(AuthService.revoke, {
    onSuccess: () => {
      localStorage.removeItem("MOONSTREAM_ACCESS_TOKEN");
      cache.clear();
      setUser(null);
      router.push("/");
    },
  });
  const { setUser } = useUser();
  const cache = useQueryClient();

  const logout = useCallback(() => {
    setLoggingOut(true);
    revoke();
  }, [revoke, setLoggingOut]);

  return {
    logout,
  };
};

export default useLogout;
