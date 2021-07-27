import { http } from "../utils";

const API = process.env.NEXT_PUBLIC_SIMIOTICS_JOURNALS_URL;
const PREFERENCES_API = `${API}/preferences`;

export const getDefaultJournal = () =>
  http({
    method: "GET",
    url: `${PREFERENCES_API}/default_journal`,
  });

export const setDefaultJournal = (journalId) =>
  http({
    method: "POST",
    url: `${PREFERENCES_API}/default_journal`,
    data: { id: journalId },
  });

export const unsetDefaultJournal = () =>
  http({
    method: "DELETE",
    url: `${PREFERENCES_API}/default_journal`,
  });
