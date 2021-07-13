import { SubscriptionsService } from "../services";
import { useMutation } from "react-query";
import { useToast } from ".";
import { queryCacheProps } from "./hookCommon";
import useStripe from "./useStripe";
import { useQuery } from "react-query";

const useSubscriptions = (groupId) => {
  const toast = useToast();
  const stripe = useStripe();

  const [manageSubscription, mangeSeatsStatus] = useMutation(
    SubscriptionsService.manageSubscription(),
    {
      onError: (error) => toast(error, "error"),
      onSuccess: (response) => {
        const {
          session_id: sessionId,
          session_url: sessionUrl,
        } = response.data;
        if (sessionId) {
          stripe.redirectToCheckout({ sessionId });
        } else if (sessionUrl) {
          window.location = sessionUrl;
        }
      },
    }
  );

  const manageSubscriptionMutation = {
    manageSubscription,
    isLoading: mangeSeatsStatus.isLoading,
  };

  const getSubscriptions = async () => {
    const response = await SubscriptionsService.getSubscriptions(groupId);
    return response.data.subscriptions;
  };

  const subscriptionsCache = useQuery(
    ["subscriptions", groupId],
    getSubscriptions,
    {
      ...queryCacheProps,
      onError: (error) => {
        toast(error, "error");
      },
    }
  );

  return { manageSubscriptionMutation, subscriptionsCache };
};

export default useSubscriptions;
