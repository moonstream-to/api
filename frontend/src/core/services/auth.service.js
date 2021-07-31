import { http } from "../utils";

const API_URL = process.env.NEXT_PUBLIC_MOONSTREAM_API_URL;
const AUTH_URL = `${API_URL}/users`;

export const login = ({ username, password }) => {
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
    method: "DELETE",
    url: `${AUTH_URL}/token`,
  });
};

export const register =
  () =>
  ({ username, email, password }) => {
    const data = new FormData();
    data.append("username", username);
    data.append("email", email);
    data.append("password", password);

    return http({
      method: "POST",
      url: `${AUTH_URL}/`,
      data,
    }).then(() =>
      http({
        method: "POST",
        url: `${AUTH_URL}/token`,
        data,
      })
    );
  };

export const forgotPassword = ({ email }) => {
  const data = new FormData();
  data.append("email", email);
  return http({
    method: "POST",
    url: `${AUTH_URL}/password/reset_initiate`,
    data,
  });
};

export const resetPassword = ({ newPassword, resetId }) => {
  const data = new FormData();
  data.append("reset_id", resetId);
  data.append("new_password", newPassword);
  return http({
    method: "POST",
    url: `${AUTH_URL}/password/reset_complete`,
    data,
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
