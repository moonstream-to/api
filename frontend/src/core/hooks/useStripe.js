import { useContext } from "react";
import { StripeContext } from "../providers/StripeProvider";

const useStripe = () => {
  const stripe = useContext(StripeContext);
  return stripe;
};

export default useStripe;
