import { queryCacheProps } from "./hookCommon";
import { useToast } from ".";
import { useQuery } from "react-query";
import { SubscriptionsService } from "../services";
import { useContext } from "react";
import UserContext from "../providers/UserProvider/context";

const useSubscription = ({ id }) => {
  const toast = useToast();
  const user = useContext(UserContext);

  const { subscriptionLinksCache } = useQuery(
    ["dashboardLinks", id],
    SubscriptionsService.getSubscriptionABI(id),
    {
      ...queryCacheProps,
      onError: (error) => {
        toast(error, "error");
      },
      enabled: !!user && !!id,
    }
  );
  return { subscriptionLinksCache };
};

export default useSubscription;
