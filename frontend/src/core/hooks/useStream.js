import { useState } from "react";

import { StreamService } from "../services";
import { useQuery } from "react-query";
import { queryCacheProps } from "./hookCommon";
import { defaultStreamBoundary } from "../services/servertime.service.js";

const useStream = (q) => {
  const [streamQuery, setStreamQuery] = useState(q || "");
  const [streamBoundary, setStreamBoundary] = useState({});

  const isStreamBoundaryEmpty = () => {
    return !streamBoundary.start_time && !streamBoundary.end_time;
  };

  const setDefaultBoundary = async () => {
    const defaultBoundary = await defaultStreamBoundary();
    setStreamBoundary(defaultBoundary);
  };

  const updateStreamBoundaryWith = (extensionBoundary) => {
    if (!extensionBoundary) {
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
      (extensionBoundary.start_time &&
        extensionBoundary.start_time <= newBoundary.start_time)
    ) {
      newBoundary.start_time = extensionBoundary.start_time;
      newBoundary.include_start =
        newBoundary.include_start || extensionBoundary.include_start;
    }
    newBoundary.include_start =
      newBoundary.include_start || extensionBoundary.include_start;

    if (
      !newBoundary.end_time ||
      (extensionBoundary.end_time &&
        extensionBoundary.end_time >= newBoundary.end_time)
    ) {
      newBoundary.end_time = extensionBoundary.end_time;
      newBoundary.include_end =
        newBoundary.include_end || extensionBoundary.include_end;
    }

    newBoundary.include_end =
      newBoundary.include_end || extensionBoundary.include_end;

    setStreamBoundary(newBoundary);
    return newBoundary;
  };

  const getEvents = () => async () => {
    const response = await StreamService.getEvents({
      streamQuery,
      ...streamBoundary,
    });
    return response.data;
  };

  const {
    data: events,
    isLoading: eventsIsLoading,
    refetch: eventsRefetch,
    isFetching: eventsIsFetching,
    remove: eventsRemove,
  } = useQuery(
    ["stream-events", streamQuery],
    () => {
      if (isStreamBoundaryEmpty()) {
        return null;
      }
      return getEvents();
    },
    {
      ...queryCacheProps,
      keepPreviousData: true,
      retry: 2,
      onSuccess: (newEvents) => {
        if (newEvents) {
          updateStreamBoundaryWith(newEvents.stream_boundary);
        }
      },
    }
  );

  const getLatestEvents = async () => {
    const response = await StreamService.latestEvents({ q: streamQuery });
    return response.data;
  };

  const {
    data: latestEvents,
    isLoading: latestEventsIsLoading,
    refetch: latestEventsRefetch,
    isFetching: latestEventsIsFetching,
    remove: latestEventsRemove,
  } = useQuery(
    ["stream-latest", streamQuery],
    () => {
      if (isStreamBoundaryEmpty()) {
        return null;
      }
      return getLatestEvents();
    },
    {
      ...queryCacheProps,
      keepPreviousData: false,
      retry: 2,
    }
  );

  const getNextEvent = async () => {
    const response = await StreamService.nextEvent({
      q: streamQuery,
      ...streamBoundary,
    });
    return response.data;
  };

  const {
    data: nextEvent,
    isLoading: nextEventIsLoading,
    refetch: nextEventRefetch,
    isFetching: nextEventIsFetching,
    remove: nextEventRemove,
  } = useQuery(
    ["stream-next", streamQuery],
    () => {
      if (isStreamBoundaryEmpty()) {
        return null;
      }
      return getNextEvent();
    },
    {
      ...queryCacheProps,
      keepPreviousData: false,
      retry: 2,
    }
  );

  const getPreviousEvent = async () => {
    const response = await StreamService.previousEvent({
      q: streamQuery,
      ...streamBoundary,
    });
    return response.data;
  };

  const {
    data: previousEvent,
    isLoading: previousEventIsLoading,
    refetch: previousEventRefetch,
    isFetching: previousEventIsFetching,
    remove: previousEventRemove,
  } = useQuery(
    ["stream-previous", streamQuery],
    () => {
      if (isStreamBoundaryEmpty()) {
        return null;
      }
      return getPreviousEvent();
    },
    {
      ...queryCacheProps,
      keepPreviousData: false,
      retry: 2,
    }
  );

  return {
    streamBoundary,
    setDefaultBoundary,
    updateStreamBoundaryWith,
    events,
    eventsIsLoading,
    eventsRefetch,
    eventsIsFetching,
    eventsRemove,
    setStreamQuery,
    latestEvents,
    latestEventsIsLoading,
    latestEventsRefetch,
    latestEventsIsFetching,
    latestEventsRemove,
    nextEvent,
    nextEventIsLoading,
    nextEventRefetch,
    nextEventIsFetching,
    nextEventRemove,
    previousEvent,
    previousEventIsLoading,
    previousEventRefetch,
    previousEventIsFetching,
    previousEventRemove,
  };
};
export default useStream;
