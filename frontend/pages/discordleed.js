import React from "react";
import { useRouter } from "../src/core/hooks";

const DiscordLeed = () => {
  const router = useRouter();

  React.useLayoutEffect(() => {
    router.push("https://discord.gg/K56VNUQGvA");
  }, [router]);

  return <></>;
};

export default DiscordLeed;
