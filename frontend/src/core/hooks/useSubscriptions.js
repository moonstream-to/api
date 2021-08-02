import { SubscriptionsService } from "../services";
import { useMutation } from "react-query";
import { useToast } from ".";
import { queryCacheProps } from "./hookCommon";
import useStripe from "./useStripe";
import { useQuery } from "react-query";

const useSubscriptions = () => {
  const toast = useToast();
  const stripe = useStripe();

  const getSubscriptions = async () => {
    const response = await SubscriptionsService.getSubscriptions();
    return response.data.data;
  };

  const subscriptionsCache = useQuery(["subscriptions"], getSubscriptions, {
    ...queryCacheProps,
    onError: (error) => {
      toast(error, "error");
    },
  });

  const getSubscriptionTypes = async () => {
    const response = await SubscriptionsService.getTypes();
    return response.data.data;
  };

  const typesCache = useQuery(["subscription_types"], getSubscriptionTypes, {
    ...queryCacheProps,
    onError: (error) => {
      toast(error, "error");
    },
  });

  const createSubscription = useMutation(
    SubscriptionsService.createSubscription(),
    {
      onError: (error) => toast(error, "error"),
      onSuccess: (response) => {
        subscriptionsCache.refetch();
        const { session_id: sessionId, session_url: sessionUrl } =
          response.data;
        if (sessionId) {
          stripe.redirectToCheckout({ sessionId });
        } else if (sessionUrl) {
          window.location = sessionUrl;
        }
      },
    }
  );

  const changeNote = useMutation(SubscriptionsService.modifySubscription(), {
    onError: (error) => toast(error, "error"),
    onSuccess: () => {
      subscriptionsCache.refetch();
    },
  });

  const deleteSubscription = useMutation(
    SubscriptionsService.deleteSubscription(),
    {
      onError: (error) => toast(error, "error"),
      onSuccess: () => {
        subscriptionsCache.refetch();
      },
    }
  );

  return {
    createSubscription,
    subscriptionsCache,
    typesCache,
    changeNote,
    deleteSubscription,
  };
};

export default useSubscriptions;
