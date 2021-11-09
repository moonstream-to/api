import { http } from "../utils";

const API = process.env.NEXT_PUBLIC_MOONSTREAM_API_URL;

export const getEvents = ({
  q,
  start_time,
  end_time,
  include_start,
  include_end,
}) => {
  let params = {};
  if (q) {
    params.q = q;
  }
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

// params is expected to be an object defining the query parameters to the /streams/latest endpoint
// The /streams/latest endpoint accepts the following query parameters:
// - q: Query filters of the form type:<subscription type> or subscription:from:<address> or subscription:to:<address>
// This will change over time and the API documentation should be the source of truth for these parameters.
// TODO(zomglings): Link here once API docs are set up.
export const latestEvents = (params) => {
  return http({ method: "GET", url: `${API}/streams/latest`, params });
};

export const nextEvent = ({
  q,
  start_time,
  end_time,
  include_start,
  include_end,
}) => {
  let params = {};
  if (q) {
    params.q = q;
  }
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
    url: `${API}/streams/next`,
    params,
  });
};

export const previousEvent = ({
  q,
  start_time,
  end_time,
  include_start,
  include_end,
}) => {
  // TODO(zomglings): Factor this query parameter building code out into a separate function.
  let params = {};
  if (q) {
    params.q = q;
  }
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
    url: `${API}/streams/previous`,
    params,
  });
};
