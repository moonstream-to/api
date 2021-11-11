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

export const deleteDashboard = (id) => {
  console.log("delete:", id);
  return http({
    method: "DELETE",
    url: `${API_URL}/dashboards/${id}/`,
  });
};

export const getDashboard = (dashboardId) => {
  console.log("get dashboard");
  //   const dashboardId = query.queryKey[2].dashboardId;
  //   console.assert(
  //     dashboardId,
  //     "No dashboard ID found in query object that was passed to service"
  //   );
  console.log("service", dashboardId);
  return http({
    method: "GET",
    url: `${API_URL}/dashboards/${dashboardId}/data_links`,
  });
};
