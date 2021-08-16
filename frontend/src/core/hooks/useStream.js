import { StreamService } from "../services";
import { useQuery } from "react-query";
import { queryCacheProps } from "./hookCommon";

const useJournalEntries = ({
  searchQuery,
  start_time,
  end_time,
  include_start,
  include_end,
  updateStreamBoundaryWith,
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
        boundaries: { ...response.data.boundaries, update: false },
      };
    };

  const { data, isLoading, refetch, isFetching, remove } = useQuery(
    ["stream", searchQuery, start_time, end_time],
    getStream(searchQuery, start_time, end_time, include_start, include_end),
    {
      //refetchInterval: refreshRate,
      ...queryCacheProps,
      keepPreviousData: true,
      retry: 3,
      onSuccess: (response) => {
        // response is object which return condition in getStream
        // TODO(andrey): Response should send page parameters inside "boundary" object (can be null).
        updateStreamBoundaryWith(response.boundaries);
      },
    }
  );

  return {
    EntriesPages: data,
    isLoading,
    refetch,
    isFetching,
    remove,
  };
};
export default useJournalEntries;
