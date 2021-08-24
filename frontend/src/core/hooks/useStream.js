import { useState } from "react";

import { StreamService } from "../services";
import { useQuery } from "react-query";
import { queryCacheProps } from "./hookCommon";
import { defaultStreamBoundary } from "../services/servertime.service.js";

const useStream = (q) => {
  const [streamQuery, setStreamQuery] = useState(
    q || "type:ethereum_whalewatch"
  );
  const [events, setEvents] = useState([]);
  const [streamBoundary, setStreamBoundary] = useState({});
  const [olderEvent, setOlderEvent] = useState(null);
  const [newerEvent, setNewerEvent] = useState(null);

  const isStreamBoundaryEmpty = () => {
    return !streamBoundary.start_time && !streamBoundary.end_time;
  };

  const setDefaultBoundary = async () => {
    const defaultBoundary = await defaultStreamBoundary();
    setStreamBoundary(defaultBoundary);
  };

  const updateStreamBoundaryWith = (
    extensionBoundary,
    { ignoreStart, ignoreEnd }
  ) => {
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
    if (!ignoreStart) {
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
    }

    if (!ignoreEnd) {
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
    }

    setStreamBoundary(newBoundary);
    return newBoundary;
  };

  const getEvents = async (customStreamBoundary) => {
    let requestStreamBoundary = customStreamBoundary;
    if (!requestStreamBoundary) {
      requestStreamBoundary = streamBoundary;
    }
    const response = await StreamService.getEvents({
      q: streamQuery,
      ...requestStreamBoundary,
    });
    return response.data;
  };

  const {
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
      retry: 2,
      onSuccess: (newEvents) => {
        if (newEvents && newEvents.stream_boundary && newEvents.events) {
          setEvents([...newEvents.events]);
          updateStreamBoundaryWith(newEvents.stream_boundary, {});
        }
      },
    }
  );

  const { refetch: loadOlderEvents, isFetching: loadOlderEventsIsFetching } =
    useQuery(
      ["stream-events", streamQuery],
      () => {
        if (olderEvent) {
          const newStreamBoundary = {
            // 5 minutes before the previous event
            start_time: olderEvent.event_timestamp - 5 * 60,
            include_start: true,
            // TODO(zomglings): This is a workaround to what seems to be a filter bug on `created_at:<=...` filters
            // on Bugout journals. Please look into it.
            end_time: olderEvent.event_timestamp + 1,
            include_end: false,
          };
          return getEvents(newStreamBoundary);
        }
      },
      {
        ...queryCacheProps,
        enabled: false,
        retry: 2,
        onSuccess: (newEvents) => {
          if (newEvents && newEvents.stream_boundary && newEvents.events) {
            setEvents([...newEvents.events, ...events]);
            updateStreamBoundaryWith(newEvents.stream_boundary, {
              ignoreEnd: true,
            });
          }
        },
      }
    );

  const { refetch: loadNewerEvents, isFetching: loadNewerEventsIsFetching } =
    useQuery(
      ["stream-events", streamQuery],
      () => {
        if (newerEvent) {
          const newStreamBoundary = {
            // TODO(zomglings): This is a workaround to what seems to be a filter bug on `created_at:>=...` filters
            // on Bugout journals. Please look into it.
            start_time: newerEvent.event_timestamp - 1,
            include_start: false,
            // 5 minutes after the next event
            end_time: newerEvent.event_timestamp + 5 * 60,
            include_end: true,
          };
          return getEvents(newStreamBoundary);
        }
      },
      {
        ...queryCacheProps,
        enabled: false,
        retry: 2,
        onSuccess: (newEvents) => {
          if (newEvents && newEvents.stream_boundary && newEvents.events) {
            setEvents([...events, ...newEvents.events]);
            updateStreamBoundaryWith(newEvents.stream_boundary, {
              ignoreStart: true,
            });
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
    setNewerEvent({ ...response.data });
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
    setOlderEvent({ ...response.data });
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
    loadOlderEvents,
    loadOlderEventsIsFetching,
    loadNewerEvents,
    loadNewerEventsIsFetching,
  };
};
export default useStream;
