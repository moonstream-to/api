import { http } from "../utils";

const API_URL = process.env.NEXT_PUBLIC_MOONSTREAM_API_URL;
export const PREFERENCES_URL = `${API_URL}/users`;

export const getOnboardingState = () =>
  http({
    method: "GET",
    url: `${PREFERENCES_URL}/onboarding`,
  });

export const setOnboardingState = (data) => {
  return http({
    method: "POST",
    url: `${PREFERENCES_URL}/onboarding`,
    data,
  });
};
