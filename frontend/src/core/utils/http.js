import enableMockupRequests from "./mockupRequests";
let axios = require("axios");

process.env.NODE_ENV !== "production" && enableMockupRequests(axios);

const http = (config) => {
  const token = localStorage.getItem("MOONSTREAM_ACCESS_TOKEN");
  const authorization = token ? { Authorization: `Bearer ${token}` } : {};
  const defaultHeaders = config.headers ?? {};
  const options = {
    ...config,
    headers: {
      ...defaultHeaders,
      ...authorization,
    },
  };

  return axios(options);
};

export { axios };
export default http;
