import { http } from "../utils";

const AUTH_URL = process.env.NEXT_PUBLIC_SIMIOTICS_AUTH_URL;

export const accept = (inviteId) => {
  const data = new FormData();
  data.append("invite_id", inviteId);

  return http({
    method: "POST",
    url: `${AUTH_URL}/invites/accept`,
    data,
  });
};
