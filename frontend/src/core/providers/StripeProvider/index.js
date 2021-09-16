import React, { createContext, useEffect, useState } from "react";
import { loadStripe } from "@stripe/stripe-js";

export const StripeContext = createContext();

export const StripeProvider = ({ children }) => {
  const stripePublishableKey = process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY;

  const [stripe, setStripe] = useState(null);

  useEffect(() => {
    let isMounted = true;
    if (isMounted) {
      if (!stripePublishableKey) {
        console.warn(
          "Unable to process payments: Stripe publishable key not provided"
        );
        return;
      }

      loadStripe(stripePublishableKey).then(setStripe);
    }
    return () => {
      isMounted = false;
    };
  }, [stripePublishableKey]);

  return (
    <StripeContext.Provider value={stripe}>{children}</StripeContext.Provider>
  );
};

export default StripeProvider;
