import { http } from "../utils";

const AUTH_URL = process.env.NEXT_PUBLIC_SIMIOTICS_AUTH_URL;

export const login = ({ username, password }) => {
  console.log('login',username, password)
  const data = new FormData();
  data.append("username", username);
  data.append("password", password);

  return http({
    method: "POST",
    url: `${AUTH_URL}/token`,
    data,
  });
};

export const revoke = () => {
  return http({
    method: "POST",
    url: `${AUTH_URL}/revoke/${localStorage.getItem("BUGOUT_ACCESS_TOKEN")}`,
  });
};

export const register = () => ({ username, email, password }) => {
  const data = new FormData();
  data.append("username", username);
  data.append("email", email);
  data.append("password", password);

  return http({
    method: "POST",
    url: `${AUTH_URL}/user`,
    data,
  }).then(() =>
    http({
      method: "POST",
      url: `${AUTH_URL}/token`,
      data,
    })
  );
};

export const verify = ({ code }) => {
  const data = new FormData();
  data.append("verification_code", code);
  return http({
    method: "POST",
    url: `${AUTH_URL}/confirm`,
    data,
  });
};

export const getTokenList = () => {
  const data = new FormData();
  return http({
    method: "GET",
    url: `${AUTH_URL}/tokens`,
    data,
  });
};

export const updateToken = ({ note, token }) => {
  const data = new FormData();
  data.append("token_note", note);
  data.append("access_token", token);
  return http({
    method: "PUT",
    url: `${AUTH_URL}/token`,
    data,
  });
};

export const forgotPassword = ({ email }) => {
  const data = new FormData();
  data.append("email", email);
  return http({
    method: "POST",
    url: `${AUTH_URL}/reset`,
    data,
  });
};

export const resetPassword = ({ newPassword, resetId }) => {
  const data = new FormData();
  data.append("reset_id", resetId);
  data.append("new_password", newPassword);
  return http({
    method: "POST",
    url: `${AUTH_URL}/password/reset`,
    data,
  });
};

export const revokeToken = (token) => {
  return http({
    method: "POST",
    url: `${AUTH_URL}/revoke/${token}`,
  });
};

export const changePassword = ({ currentPassword, newPassword }) => {
  const data = new FormData();
  data.append("current_password", currentPassword);
  data.append("new_password", newPassword);
  return http({
    method: "POST",
    url: `${AUTH_URL}/profile/password`,
    data,
  });
};
