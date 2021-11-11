import { useRouter } from "next/router";
import { useContext, useLayoutEffect } from "react";

import UserContext from "../src/core/providers/UserProvider/context";
import { getLayout } from "../src/layouts/EntryPointLayout";

const EntryPoint = () => {
  const router = useRouter();
  const { isInit } = useContext(UserContext);

  useLayoutEffect(() => {
    if (router.isReady && isInit && router.asPath !== router.pathname + `/`) {
      if (localStorage.getItem("entry_point")) {
        router.replace("/404", router.asPath);
      } else {
        localStorage.setItem("entry_point", 1);
        router.replace(router.asPath, undefined, {
          shallow: true,
        });
      }
    }
  }, [router, isInit]);

  return "";
};

EntryPoint.getLayout = getLayout;

export default EntryPoint;
