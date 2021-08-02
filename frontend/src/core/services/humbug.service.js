import { http } from "../utils";
const API = process.env.NEXT_PUBLIC_SIMIOTICS_JOURNALS_URL;

export const createHumbug = ({ groupId, journalName }) => {
  const data = new FormData();
  data.append("group_id", groupId);
  data.append("journal_name", journalName);

  return http({
    method: "POST",
    url: `${API}/humbug/`,
    data,
  });
};

export const deleteHumbug = (humbugId) => {
  return http({
    method: "DELETE",
    url: `${API}/humbug/${humbugId}`,
  });
};

/**
 * getHumbugIntegrations provides a list of humbug integrations
 * that user has.
 *
 * Specifying groupId field will return only integrations for that groupId
 */
export const getHumbugItegrations = (query) => {
  var url = `${API}/humbug/integrations`;
  url = query ? `${url}?${query}` : url;
  return http({
    method: "GET",
    url: url,
  });
};

export const getHumbug = (key, { humbugId }) => {
  return http({
    method: "GET",
    url: `${API}/humbug/${humbugId}`,
  });
};

// ************ Restricted tokens *******************
export const getTokens = (humbugId) => {
  return http({
    method: "GET",
    url: `${API}/humbug/${humbugId}/tokens`,
  });
};

export const createRestrictedToken =
  (humbugId) =>
  ({ appName, appVersion }) => {
    const data = new FormData();
    data.append("app_name", appName);
    data.append("app_version", appVersion);

    return http({
      method: "POST",
      url: `${API}/humbug/${humbugId}/tokens`,
      data,
    });
  };

export const deleteRestrictedToken = (humbugId) => (tokenId) => {
  const data = new FormData();

  data.append("restricted_token_id", tokenId);
  return http({
    method: "DELETE",
    url: `${API}/humbug/${humbugId}/tokens`,
    data,
  });
};
