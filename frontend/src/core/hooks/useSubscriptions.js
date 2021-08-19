import { useState, useEffect } from "react";
import { useQuery } from "react-query";
import { SubscriptionsService } from "../services";
import { useMutation } from "react-query";
import { useToast } from ".";
import { queryCacheProps } from "./hookCommon";
import useStripe from "./useStripe";

const useSubscriptions = () => {
  const toast = useToast();
  const stripe = useStripe();

  const [subscriptionTypeIcons, setSubscriptionTypeIcons] = useState({});

  const getSubscriptions = async () => {
    const response = await SubscriptionsService.getSubscriptions();
    return response.data;
  };

  const subscriptionsCache = useQuery(["subscriptions"], getSubscriptions, {
    ...queryCacheProps,
    onError: (error) => {
      toast(error, "error");
    },
  });

  const getSubscriptionTypes = async () => {
    const response = await SubscriptionsService.getTypes();
    let result = [];
    if (response.data.subscription_types) {
      result = response.data.subscription_types;
    }
    return result;
  };

  const typesCache = useQuery(["subscription_types"], getSubscriptionTypes, {
    ...queryCacheProps,
    onError: (error) => {
      toast(error, "error");
    },
  });

  useEffect(() => {
    let icons = {};
    if (typesCache.data) {
      typesCache.data.forEach(
        (subscriptionType) =>
          (icons[subscriptionType.id] = subscriptionType.icon_url)
      );
      setSubscriptionTypeIcons(icons);
    }
  }, [typesCache.data]);

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

  const updateSubscription = useMutation(
    SubscriptionsService.modifySubscription(),
    {
      onError: (error) => toast(error, "error"),
      onSuccess: () => {
        subscriptionsCache.refetch();
      },
    }
  );

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
    updateSubscription,
    deleteSubscription,
    subscriptionTypeIcons,
  };
};

export default useSubscriptions;
