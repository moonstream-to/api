import { http } from "../utils";

const AUTH_URL = process.env.NEXT_PUBLIC_SIMIOTICS_AUTH_URL;

export const manageSubscription = () => ({
  groupId,
  desiredUnits,
  planType,
}) => {
  const data = new FormData();
  data.append("group_id", groupId);
  data.append("units_required", desiredUnits);
  data.append("plan_type", planType);
  return http({
    method: "POST",
    url: `${AUTH_URL}/subscription/manage`,
    data,
  });
};

export const getSubscriptions = (groupId) => {
  return http({
    method: "GET",
    url: `${AUTH_URL}/groups/${groupId}/subscriptions`,
  });
};
