import { http } from "../utils";

const API = process.env.NEXT_PUBLIC_SIMIOTICS_JOURNALS_URL;

export const createTag = (journalId, entryId) => (data) =>
  http({
    method: "POST",
    url: `${API}/journals/${journalId}/entries/${entryId}/tags`,
    data,
  });

export const deleteTag = (journalId, entryId) => (data) =>
  http({
    method: "DELETE",
    url: `${API}/journals/${journalId}/entries/${entryId}/tags`,
    data,
  });

export const getTags = (journalId, entryId) => (data) =>
  http({
    method: "GET",
    url: `${API}/journals/${journalId}/entries/${entryId}/tags`,
    data,
  });
