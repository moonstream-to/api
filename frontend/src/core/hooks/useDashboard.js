import { useMutation, useQuery } from "react-query";
import { useRouter, useToast } from ".";
import { queryCacheProps } from "./hookCommon";
import { DashboardService } from "../services";
import { useContext } from "react";
import UserContext from "../providers/UserProvider/context";

const useDashboard = (dashboardId) => {
  const toast = useToast();
  const router = useRouter();
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

  const createDashboard = useMutation(DashboardService.createDashboard, {
    onSuccess: () => {
      toast("Created new dashboard", "success");
    },
    onError: (error) => {
      toast(error.error, "error", "Fail");
    },
    onSettled: () => {
      dashboardsListCache.refetch();
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

  const dashboardCache = useQuery(
    ["dashboards", { dashboardId }],
    () => DashboardService.getDashboard(dashboardId),
    {
      ...queryCacheProps,
      onError: (error) => {
        toast(error, "error");
      },
      enabled: !!user && !!dashboardId,
    }
  );

  const dashboardLinksCache = useQuery(
    ["dashboardLinks", { dashboardId }],
    () => DashboardService.getDashboardLinks(dashboardId),
    {
      ...queryCacheProps,
      onError: (error) => {
        toast(error, "error");
      },
      enabled: !!user && !!dashboardId,
    }
  );

  return {
    createDashboard,
    dashboardsListCache,
    dashboardCache,
    deleteDashboard,
    dashboardLinksCache,
  };
};

export default useDashboard;
