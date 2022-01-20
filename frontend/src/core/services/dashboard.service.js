import { http } from "../utils";

const API_URL = process.env.NEXT_PUBLIC_MOONSTREAM_API_URL;

export const createDashboard = (data) => {
  return http({
    method: "POST",
    url: `${API_URL}/dashboards/`,
    data,
  });
};

export const updateDashboard = ({ dashboard, id }) => {
  return http({
    method: "PUT",
    url: `${API_URL}/dashboards/${id}`,
    data: dashboard,
  });
};

export const getDashboardsList = () => {
  return http({
    method: "GET",
    url: `${API_URL}/dashboards/`,
  });
};

export const deleteDashboard = (id) => {
  return http({
    method: "DELETE",
    url: `${API_URL}/dashboards/${id}`,
  });
};

export const getDashboard = (dashboardId) => {
  return http({
    method: "GET",
    url: `${API_URL}/dashboards/${dashboardId}`,
  });
};

export const getDashboardLinks = (dashboardId) => {
  return http({
    method: "GET",
    url: `${API_URL}/dashboards/${dashboardId}/stats`,
  });
};

export const refreshDashboard = ({ dashboardId, timeRange }) => {
  return http({
    method: "POST",
    url: `${API_URL}/dashboards/${dashboardId}/stats_update`,
    data: {
      timescales: [timeRange],
    },
  });
};
