import { http } from "../utils";
// import axios from "axios";

const API = process.env.NEXT_PUBLIC_MOONSTREAM_API_URL;

export const getStream = ({
  searchTerm,
  start_time,
  end_time,
  include_start,
  include_end,
}) => {
  let params = {};

  if (searchTerm) {
    params.q = encodeURIComponent(searchTerm);
  }

  if (start_time) {
    params.start_time = encodeURIComponent(start_time);
  }

  if (end_time) {
    params.end_time = encodeURIComponent(end_time);
  }

  if (include_start) {
    params.include_start = encodeURIComponent(true);
  }

  if (include_end) {
    params.include_end = encodeURIComponent(true);
  }

  return http({
    method: "GET",
    url: `${API}/streams/`,
    params: params,
  });
};
