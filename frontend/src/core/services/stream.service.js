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
  let params = {
    q: searchTerm,
  };
  if (start_time || start_time === 0) {
    params.start_time = start_time;
  }
  if (end_time || end_time === 0) {
    params.end_time = end_time;
  }
  if (include_start) {
    params.include_start = include_start;
  }
  if (include_end) {
    params.include_end = include_end;
  }

  return http({
    method: "GET",
    url: `${API}/streams/`,
    params,
  });
};
