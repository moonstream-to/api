import { http } from "../utils";
// import axios from "axios";

const API = process.env.NEXT_PUBLIC_SIMIOTICS_AUTH_URL;

export const getTypes = () =>
  http({
    method: "GET",
    url: `${API}/subscription_types/`,
  });

export const getSubscriptions = () =>
  http({
    method: "GET",
    url: `${API}/subscriptions/`,
  });

export const create = ({ address, note, blockchain }) => {
  const data = new FormData();
  data.append("address", address);
  data.append("note", note);
  data.append("blockchain", blockchain);
  http({
    method: "POST",
    url: `${API}/subscriptions/`,
    data,
  });
};

export const deleteJournal = (id) => () =>
  http({
    method: "DELETE",
    url: `${API}/journals/${id}`,
  });

export const createSubscription =
  () =>
  ({ address, type, note }) => {
    console.log("createSubscription: ", address, type, note);
    const data = new FormData();
    data.append("address", address);
    data.append("subscription_type", type);
    data.append("note", note);
    return http({
      method: "POST",
      url: `${API}/subscriptions/`,
      data,
    });
  };

export const modifySubscription =
  () =>
  ({ id, note }) => {
    console.log("modifySubscription: ", note, id);
    const data = new FormData();
    data.append("note", note);
    data.append("id", id);
    return http({
      method: "POST",
      url: `${API}/subscription/${id}`,
      data,
    });
  };

export const deleteSubscription = () => (id) => {
  console.log("deleteSubscription: ", id);
  return http({
    method: "DELETE",
    url: `${API}/subscription/${id}`,
  });
};

// export const getSubscriptions = (groupId) => {
//   return http({
//     method: "GET",
//     url: `${API}/groups/${groupId}/subscriptions`,
//   });
// };
