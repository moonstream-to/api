import { useMutation, useQuery, useQueryClient } from "react-query";
import { useRouter, useToast } from ".";
import { queryCacheProps } from "./hookCommon";
import { DashboardService } from "../services";
import { useContext } from "react";
import UserContext from "../providers/UserProvider/context";

const useDashboard = (dashboardId) => {
  const toast = useToast();
  const router = useRouter();
  const queryClient = useQueryClient();
  const { user } = useContext(UserContext);

  const dashboardsListCache = useQuery(
    ["dashboards-list"],
    DashboardService.getDashboardsList,
    {
      ...queryCacheProps,
      onError: (error) => {
        toast(error, "error");
      },
      enabled: !!user,
    }
  );

  // const dashboardUpdateState = useQuery(
  //   ["DashboardUpdateState", { dashboardId: dashboardId }],
  //   () =>
  //     new Promise((resolve, reject) =>
  //       reject("Dashboard Update State has no network functionality")
  //     ),
  //   {
  //     ...queryCacheProps,
  //     staleTime: Infinity,
  //     onError: (error) => {
  //       toast(error, "error");
  //     },
  //     enabled: false,
  //   }
  // );

  const _createDashboard = async (dashboard) => {
    const _dashboard = { ...dashboard };
    if (!_dashboard.subscription_settings) {
      _dashboard.subscription_settings = [];
    }
    const response = await DashboardService.createDashboard(_dashboard);
    return response.data;
  };

  const createDashboard = useMutation(_createDashboard, {
    onSuccess: () => {
      toast("Created new dashboard", "success");
      sessionStorage.removeItem("new_dashboard");
    },
    onError: (error) => {
      toast(error.error, "error", "Fail");
    },
    onSettled: () => {
      dashboardsListCache.refetch();
    },
  });

  const updateDashboard = useMutation(DashboardService.updateDashboard, {
    onSuccess: () => {
      toast("Updated new dashboard", "success");
    },
    onError: (error) => {
      toast(error.error, "error", "Fail");
    },
    onSettled: () => {
      dashboardsListCache.refetch();
      dashboardCache.refetch();
      dashboardLinksCache.refetch();
    },
  });

  const deleteDashboard = useMutation(
    () => DashboardService.deleteDashboard(dashboardId),
    {
      onSuccess: () => {
        toast("Deleted dashboard", "success");
        router.push("/welcome");
      },
      onError: (error) => {
        toast(error.error, "error", "Fail");
      },
      onSettled: () => {
        dashboardsListCache.refetch();
      },
    }
  );

  const _getDashboard = async (dashboardId) => {
    const response = await DashboardService.getDashboard(dashboardId);
    return response.data;
  };

  const dashboardCache = useQuery(
    ["dashboards", { dashboardId: dashboardId }],
    () => _getDashboard(dashboardId),
    {
      ...queryCacheProps,
      onError: (error) => {
        toast(error, "error");
      },
      enabled: !!user && !!dashboardId,
    }
  );

  const dashboardLinksCache = useQuery(
    ["dashboardLinks", { dashboardId: dashboardId }],
    () => DashboardService.getDashboardLinks(dashboardId),
    {
      ...queryCacheProps,
      onError: (error) => {
        toast(error, "error");
      },
      enabled: !!user && !!dashboardId,
    }
  );

  const refreshDashboard = useMutation(DashboardService.refreshDashboard, {
    onSuccess: (data) => {
      queryClient.setQueryData(
        ["dashboardLinks", { dashboardId: dashboardId }],
        (oldData) => {
          let newData = { ...oldData };

          Object.keys(data.data).forEach((subscription) => {
            Object.keys(data.data[subscription]).forEach((timeScale) => {
              newData.data[subscription][timeScale] =
                data.data[subscription][timeScale];
            });
          });
          return newData;
        }
      );
    },
    onError: (error) => {
      toast(error.error, "error", "Fail");
    },
  });

  return {
    createDashboard,
    dashboardsListCache,
    dashboardCache,
    deleteDashboard,
    dashboardLinksCache,
    refreshDashboard,
    updateDashboard,
  };
};

export default useDashboard;
