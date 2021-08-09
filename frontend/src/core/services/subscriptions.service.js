import { http } from "../utils";
// import axios from "axios";

const API = process.env.NEXT_PUBLIC_MOONSTREAM_API_URL;

export const getTypes = () =>
  http({
    method: "GET",
    url: `${API}/subscriptions/types`,
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
  ({ address, type, label, color }) => {
    const data = new FormData();
    data.append("address", address);
    data.append("subscription_type_id", type);
    data.append("color", color);
    data.append("label", label);
    return http({
      method: "POST",
      url: `${API}/subscriptions/`,
      data,
    });
  };

export const modifySubscription =
  () =>
  ({ id, note }) => {
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
  return http({
    method: "DELETE",
    url: `${API}/subscriptions/${id}`,
  });
};
