import { useMutation, useQuery } from "react-query";
import { useToast } from ".";
import { queryCacheProps } from "./hookCommon";
import { DashboardService } from "../services";
import { useContext } from "react";
import UserContext from "../providers/UserProvider/context";

const useDashboard = () => {
  const toast = useToast();
  const { user } = useContext(UserContext);
  const createDashboard = useMutation(DashboardService.createDashboard, {
    onSuccess: () => {
      toast("Created new dashboard", "success");
    },
    onError: (error) => {
      toast(error.error, "error", "Fail");
    },
  });

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

  return { createDashboard, dashboardsListCache };
};

export default useDashboard;
