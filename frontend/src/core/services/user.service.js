import { http } from "../utils";

const AUTH_URL = process.env.NEXT_PUBLIC_SIMIOTICS_AUTH_URL;

export const findUser = (query) => {
  return http({
    method: "GET",
    url: `${AUTH_URL}/user/find?${query}`,
  });
};
