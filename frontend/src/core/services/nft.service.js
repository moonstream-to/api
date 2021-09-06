import { http } from "../utils";

const API = process.env.NEXT_PUBLIC_MOONSTREAM_API_URL;

export const getNFTStats = () =>
  http({
    method: "GET",
    url: `${API}/nft`,
  });
