import { http } from "../utils";
// import axios from "axios";

const API = process.env.NEXT_PUBLIC_MOONSTREAM_API_URL;

export const getStream = ({
  searchTerm,
  start_time,
  end_time,
  include_start,
  include_end,
}) =>
  http({
    method: "GET",
    url: `${API}/streams/`,
    params: {
      q: searchTerm,
      start_time: start_time,
      end_time: end_time,
      include_start: include_start,
      include_end: include_end,
    },
  });
