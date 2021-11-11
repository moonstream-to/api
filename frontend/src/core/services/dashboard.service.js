import { http } from "../utils";

const API_URL = process.env.NEXT_PUBLIC_MOONSTREAM_API_URL;

export const createDashboard = (data) => {
  return http({
    method: "POST",
    url: `${API_URL}/dashboards`,
    data,
  });
};

export const getDashboardsList = () => {
  return http({
    method: "GET",
    url: `${API_URL}/dashboards`,
  });
};
