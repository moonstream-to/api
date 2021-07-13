import { useQuery } from "react-query";
import { JournalService } from "../services";
import { queryCacheProps } from "./hookCommon";
import { useToast, useUser } from ".";

const useJournals = () => {
  const toast = useToast();
  const { user } = useUser();

  const getAllJournals = async () => {
    const response = await JournalService.getAll();
    const newAllJournals = [...response.data.journals];
    newAllJournals.sort(function (a, b) {
      var aName = a.name.toUpperCase();
      var bName = b.name.toUpperCase();
      return aName < bName ? -1 : aName < bName ? 1 : 0;
    });
    return [...newAllJournals];
  };

  const journalsCache = useQuery("journals-list", getAllJournals, {
    ...queryCacheProps,
    placeholderData: [],
    enabled: !!user,
    onError: (error) => {
      toast(error, "error");
    },
  });

  const getPublicJournals = async () => {
    const response = await JournalService.getPublicJournals();

    const newPublicJournals = [...response.data.journals];
    newPublicJournals.sort(function (a, b) {
      var aName = a.name.toUpperCase();
      var bName = b.name.toUpperCase();
      return aName < bName ? -1 : aName < bName ? 1 : 0;
    });

    return [...newPublicJournals];
  };

  const publicJournalsCache = useQuery(["journals-public"], getPublicJournals, {
    placeholderData: [],
    ...queryCacheProps,

    onError: (error) => {
      toast(error, "error");
    },
  });

  return {
    journalsCache,
    publicJournalsCache,
  };
};

export default useJournals;
