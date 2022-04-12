import { http } from "../utils";

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
  ({ id, label, color, abi }) => {
    const data = new FormData();
    color && data.append("color", color);
    label && data.append("label", label);
    abi && data.append("abi", abi);
    return http({
      method: "PUT",
      url: `${API}/subscriptions/${id}`,
      data,
    });
  };

export const deleteSubscription = () => (id) => {
  return http({
    method: "DELETE",
    url: `${API}/subscriptions/${id}`,
  });
};

export const getSubscriptionABI = (id) => () => {
  return http({
    method: "GET",
    url: `${API}/subscriptions/${id}/abi`,
  });
};

export const getSubscription = (id) =>
  http({
    method: "GET",
    url: `${API}/subscriptions/${id}`,
  });
