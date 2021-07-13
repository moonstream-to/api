import { http } from "../utils";

const API = process.env.NEXT_PUBLIC_SIMIOTICS_JOURNALS_URL;

export const create = (journalId) => (data) =>
  http({
    method: "POST",
    url: `${API}/journals/${journalId}/entries`,
    data: {
      content: "",
      ...data,
    },
  });

export const update = (journalId, entryId) => (data) =>
  http({
    method: "PUT",
    url: `${API}/journals/${journalId}/entries/${entryId}`,
    data,
  });

export const deleteEntry = (journalId, entryId) => () =>
  http({
    method: "DELETE",
    url: `${API}/journals/${journalId}/entries/${entryId}`,
  });
