import { http } from "../utils";

const AUTH_URL = process.env.NEXT_PUBLIC_SIMIOTICS_AUTH_URL;

export const getGroupUsers = (key, groupId) => {
  return http({
    method: "GET",
    url: `${AUTH_URL}/group/${groupId}/users`,
  });
};

export const getGroups = () => {
  return http({
    method: "GET",
    url: `${AUTH_URL}/groups`,
  });
};

export const createGroup = (groupName) => {
  const data = new FormData();
  data.append("group_name", groupName);

  return http({
    method: "POST",
    url: `${AUTH_URL}/groups`,
    data,
  });
};

export const setGroupUser = (groupId) => (invitee) => {
  const data = new FormData();
  data.append("email", invitee.email);
  data.append("user_type", invitee.role);
  return http({
    method: "POST",
    url: `${AUTH_URL}/groups/${groupId}/role`,
    data,
  });
};

export const setGroupName = ({ name, groupId }) => {
  const data = new FormData();
  data.append("group_name", name);
  return http({
    method: "POST",
    url: `${AUTH_URL}/groups/${groupId}/name`,
    data,
  });
};

export const deleteGroupUser = (groupId) => (userName) => {
  const data = new FormData();
  data.append("username", userName);
  return http({
    method: "DELETE",
    url: `${AUTH_URL}/groups/${groupId}/role`,
    data,
  });
};

export const deleteGroup = (groupId) => {
  return http({
    method: "DELETE",
    url: `${AUTH_URL}/groups/${groupId}`,
  });
};

export const sendInvite = (groupId) => (invitee) => {
  const data = new FormData();
  data.append("group_id", groupId);

  //If not email - invite will be public
  if (invitee?.email) {
    data.append("email", invitee.email);
    data.append("user_type", invitee.role);
  }

  return http({
    method: "POST",
    url: `${AUTH_URL}/groups/${groupId}/invites/send`,
    data,
  });
};

export const getInvites = (groupId) => {
  return http({
    method: "GET",
    url: `${AUTH_URL}/groups/${groupId}/invites`,
  });
};

export const deleteInvite = (groupId) => (inviteId) => {
  const data = new FormData();
  data.append("invite_id", inviteId);
  return http({
    method: "DELETE",
    url: `${AUTH_URL}/groups/${groupId}/invites`,
    data,
  });
};
