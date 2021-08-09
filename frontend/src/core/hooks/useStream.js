import { StreamService } from "../services";
import { useQuery } from "react-query";
import { queryCacheProps } from "./hookCommon";

const useJournalEntries = ({
  refreshRate,
  searchQuery,
  start_time,
  end_time,
  include_start,
  include_end,
  updateStreamBoundaryWith,
  enabled,
}) => {
  // set our get method
  const getStream =
    (searchTerm, start_time, end_time, include_start, include_end) =>
    async () => {
      // Request with params to streams
      const response = await StreamService.getStream({
        searchTerm: searchTerm,
        start_time: start_time,
        end_time: end_time,
        include_start: include_start,
        include_end: include_end,
      });

      // new events from stream
      const newEventsList = response.data.stream.map((event) => ({
        ...event,
      }));

      return {
        data: [...newEventsList],
        boundaries: { ...response.data.boundaries },
      };
    };

  const { data, isLoading, refetch } = useQuery(
    ["stream", { searchQuery }],
    getStream(searchQuery, start_time, end_time, include_start, include_end),
    {
      refetchInterval: refreshRate,
      ...queryCacheProps,
      onSuccess: (response) => {
        // response is object which return condition in getStream
        // TODO(andrey): Response should send page parameters inside "boundary" object (can be null).
        updateStreamBoundaryWith(response.boundaries);
      },
      enabled: !!enabled,
    }
  );

  return {
    EntriesPages: data,
    isLoading,
    refetch,
  };
};
export default useJournalEntries;
