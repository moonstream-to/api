import { useQuery, useQueryCache } from "react-query";
import { PreferencesService } from "../services";
import { queryCacheProps } from "./hookCommon";

const getPreferences = async () => {
  let preferences = {};
  try {
    const defaultJournalResponse = await PreferencesService.getDefaultJournal();
    preferences.defaultJournal = defaultJournalResponse.data?.id;
  } catch {
    preferences.defaultJournal = null;
  }
  return preferences;
};

const usePreferences = () => {
  const preferencesKey = "preferences-default-journal";
  const cache = useQueryCache();
  const { data, refetch } = useQuery(preferencesKey, getPreferences, {
    ...queryCacheProps,
    staleTime: 300000,
  });

  const invalidateAfter = (modifierFn) => {
    return async function (...args) {
      await modifierFn(...args);
      cache.invalidateQueries(preferencesKey);
    };
  };

  const setPreference = {
    defaultJournal: invalidateAfter(PreferencesService.setDefaultJournal),
  };
  const unsetPreference = {
    defaultJournal: invalidateAfter(PreferencesService.unsetDefaultJournal),
  };
  return { data, refetch, setPreference, unsetPreference };
};

export default usePreferences;
