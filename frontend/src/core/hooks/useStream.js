import { useState } from "react";

import { queryCacheProps } from "./hookCommon";
import { SubscriptionsService } from "../services";

const useJournalEntries = ({
  refreshRate,
  searchQuery,
  start_time,
  end_time,
  include_start,
  include_end,
  enabled,
}) => {
  const [streamBoundary, setStreamBoundary] = useState({
    start_time: null,
    end_time: null,
    include_start: false,
    include_end: false,
    next_event_time: null,
    previous_event_time: null,
  });

  const updateStreamBoundaryWith = (pageBoundary) => {
    if (!pageBoundary) {
      return streamBoundary;
    }
    let newBoundary = { ...streamBoundary };
    // We do not check if there is no overlap between the streamBoundary and the pageBoundary - we assume
    // that there *is* an overlap and even if there isn't the stream should gracefully respect the
    // pageBoundary because that was the most recent request the user made.
    // TODO(zomglings): If there is no overlap in boundaries, replace streamBoundary with pageBoundary.
    // No overlap logic:
    // if (<no overlap>) {
    //   setStreamBoundary(pageBoundary)
    //   return pageBoundary
    // }
    if (
      !newBoundary.start_time ||
      (pageBoundary.start_time &&
        pageBoundary.start_time <= newBoundary.start_time)
    ) {
      newBoundary.start_time = pageBoundary.start_time;
      newBoundary.include_start =
        newBoundary.include_start || pageBoundary.include_start;
    }
    if (
      !newBoundary.end_time ||
      (pageBoundary.end_time && pageBoundary.end_time >= newBoundary.end_time)
    ) {
      newBoundary.end_time = pageBoundary.end_time;
      newBoundary.include_end =
        newBoundary.include_end || pageBoundary.include_end;
    }

    if (
      !newBoundary.next_event_time ||
      (pageBoundary.next_event_time &&
        pageBoundary.next_event_time > newBoundary.next_event_time)
    ) {
      newBoundary.next_event_time = pageBoundary.next_event_time;
    }

    if (
      !newBoundary.previous_event_time ||
      (pageBoundary.previous_event_time &&
        pageBoundary.previous_event_time > newBoundary.previous_event_time)
    ) {
      newBoundary.previous_event_time = pageBoundary.previous_event_time;
    }

    setStreamBoundary(newBoundary);
    return newBoundary;
  };

  // set our get method
  const getStream =
    (searchTerm, start_time, end_time, include_start, include_end) =>
    async () => {
      // Request with params to streams
      const response = await SubscriptionsService.getStream({
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
        // TODO(andrey): Get rid of this.
        pageParams: {
          // timeinterval
          start_time: response.data.start_time, // from old
          end_time: response.data.end_time, // to new

          // closes available transactions
          next_event_time: response.data.next_event_time,
          previous_event_time: response.data.previous_event_time,

          // boundaries
          include_start: response.data.include_start,
          include_end: response.data.include_end,
        },
      };
    };

  const { data, isLoading, refetch } = useQuery(
    ["stream", { searchQuery }],
    getStream(searchQuery, start_time, end_time, include_start, include_end),
    {
      refetchInterval: refreshRate,
      ...queryCacheProps,
      onSuccess: (response) => {
        // TODO(andrey): Response should send page parameters inside "boundary" object (can be null).
        updateStreamBoundaryWith(response.data.boundary);
      },
      enabled: !!enabled,
    }
  );

  return {
    EntriesPages: data,
    isLoading,
    refetch,
    streamBoundary,
    updateStreamBoundaryWith,
  };
};
export default useJournalEntries;
