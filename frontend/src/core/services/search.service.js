import { BUGOUT_API_URL, BUGOUT_ENDPOINTS } from "../constants";

export const getResultsByEndpoint = async (query, endpoint, clientID) => {
  if (!BUGOUT_ENDPOINTS[endpoint]) {
    throw new Error(`Invalid Bugout endpoint: ${endpoint}`);
  }

  let data;
  try {
    const requestURL = `${BUGOUT_API_URL}/${
      BUGOUT_ENDPOINTS[endpoint]
    }?q=${encodeURIComponent(query)}`;
    const method = "GET";
    const headers = {
      "x-simiotics-client-id": clientID,
    };

    // TODO(neeraj): Configure search API to accept Authorization header. The way it is set up
    // now, the AWS Lambdas accept all origins for CORS purposes. This prevents us from setting
    // Authorization header since we need to set Access-Control-Allow-Authentication to true,
    // which requires us to restrict origins. On Lambda, since I am setting CORS headers
    // myself, I would have to implement the logic to handle multiple origins (since the
    // Access-Control-Allow-Origins only takes one origin).
    // At that point, uncomment the following:
    // const token = localStorage.getItem('MOONSTREAM_ACCESS_TOKEN')
    // if (token) {
    //     headers.Authorization = `Bearer ${localStorage.getItem('MOONSTREAM_ACCESS_TOKEN')}`
    // }

    const response = await fetch(requestURL, { method, headers });
    data = await response.json();

    return {
      endpoint,
      data,
    };
  } catch (err) {
    console.log(err);
    throw new Error(`Error using Bugout Search API: ${err}`);
  }
};
