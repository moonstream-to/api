import { http } from "../utils";

const BUGOUT_STATUS_URL = process.env.NEXT_PUBLIC_BUGOUT_STATUS_URL;

export const serverListStatus = () => {
  return http({
    method: "GET",
    url: `${BUGOUT_STATUS_URL}/status`,
  });
};
