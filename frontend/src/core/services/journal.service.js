import { http } from "../utils";

const API = process.env.NEXT_PUBLIC_SIMIOTICS_JOURNALS_URL;

export const getAll = () =>
  http({
    method: "GET",
    url: `${API}/journals/`,
  });

export const getEntry = (key, { journalId, entryId }) =>
  http({
    method: "GET",
    url: `${API}/journals/${journalId}/entries/${entryId}`,
  });

export const getPublicEntry = (key, { journalId, entryId }) =>
  http({
    method: "GET",
    url: `${API}/public/${journalId}/entries/${entryId}`,
  });

export const create = (data) =>
  http({
    method: "POST",
    url: `${API}/journals/`,
    data,
  });

export const deleteJournal = (id) => () =>
  http({
    method: "DELETE",
    url: `${API}/journals/${id}`,
  });

export const getJournal = (key, { journalId }) =>
  http({
    method: "GET",
    url: `${API}/journals/${journalId}`,
  });

export const getJournalPermissions = (journalId) => {
  const url = journalId
    ? `${API}/journals/${journalId}/permissions`
    : `${API}/journals/permissions`;
  return http({
    method: "GET",
    url: url,
  });
};

export const getCurrentUserJournalPermissions = (journalId) =>
  http({
    method: "GET",
    url: `${API}/journals/${journalId}/scopes`,
  });

export const getJournalsScopes = () => {
  return http({
    method: "GET",
    url: `${API}/journals/permissions`,
  });
};

export const setJournalPermission =
  (journalId) =>
  ({ holder_type, holder_id, permission_list }) => {
    const data = new FormData();
    data.append("holder_type", holder_type);
    data.append("holder_id", holder_id);
    data.append("permission_list", permission_list);

    return http({
      method: "POST",
      url: `${API}/journals/${journalId}/scopes`,
      data: { holder_type, holder_id, permission_list },
    });
  };

export const deleteJournalPermission =
  (journalId) =>
  ({ holder_type, holder_id, permission_list }) => {
    return http({
      method: "DELETE",
      url: `${API}/journals/${journalId}/scopes`,
      data: { holder_type, holder_id, permission_list },
      // permission_list: ["read"]
    });
  };

export const getPublicJournals = () =>
  http({
    method: "GET",
    url: `${API}/public/`,
  });

export const searchEntries =
  ({ journalId }) =>
  ({ searchTerm, limit, offset, isContent, journalType }) => {
    const journalScope = journalType === "personal" ? "journals" : "public";
    return http({
      method: "GET",
      url: `${API}/${journalScope}/${journalId}/search`,
      params: {
        // filters: searchTags,
        q: searchTerm,
        limit: encodeURIComponent(limit),
        offset: encodeURIComponent(offset),
        content: encodeURIComponent(isContent),
      },
    });
  };

export const publicSearchEntries =
  ({ journalId }) =>
  (query) =>
    http({
      method: "GET",
      url: `${API}/public/${journalId}/search?q=${query}`,
    });

export const getPublicJournal = (key, { journalId }) =>
  http({
    method: "GET",
    url: `${API}/public/${journalId}`,
  });

export const getJournalStats =
  (key, { journalId }) =>
  () =>
    http({
      method: "GET",
      url: `${API}/journals/${journalId}/stats`,
      params: { stats_version: 5 },
    });
