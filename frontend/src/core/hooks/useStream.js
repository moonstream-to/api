import { useState } from "react";
import { StreamService } from "../services";
import { useQuery } from "react-query";
import { queryCacheProps } from "./hookCommon";
import { defaultStreamBoundary } from "../services/servertime.service.js";
import { PAGE_SIZE } from "../constants";
const useStream = (q, streamCache, setStreamCache, cursor, setCursor) => {
  const [streamQuery, setStreamQuery] = useState(q || "");
  const [events, setEvents] = useState([]);
  const [streamBoundary, setStreamBoundary] = useState({});
  const [olderEvent, setOlderEvent] = useState(null);
  const [newerEvent, setNewerEvent] = useState(null);

  const twentyFourHoursInMs = 1000 * 60 * 60 * 24;

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

  //////////////////////////////////////////////////
  /// Just load event by current event boundary ///
  ////////////////////////////////////////////////

  const {
    isLoading: eventsIsLoading,
    refetch: eventsRefetch,
    isFetching: eventsIsFetching,
    remove: eventsRemove,
  } = useQuery(
    "stream-default",
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
          if (cursor === null) {
            setCursor(0);
            setStreamCache([...newEvents.events]);
            if (newEvents.events.length > PAGE_SIZE) {
              setEvents(newEvents.events.slice(0, PAGE_SIZE));
            } else {
              setEvents(newEvents.events.slice(0, newEvents.events.length));
            }
          }

          updateStreamBoundaryWith(newEvents.stream_boundary, {});
        }
      },
    }
  );

  ///////////////////////////
  /// Load olders events ///
  /////////////////////////

  const { refetch: loadOlderEvents, isFetching: loadOlderEventsIsFetching } =
    useQuery(
      "stream-older-events",
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
        refetchOnWindowFocus: false,
        refetchOnmount: false,
        refetchOnReconnect: false,
        staleTime: twentyFourHoursInMs,
        retry: 2,
        onSuccess: (newEvents) => {
          if (newEvents && newEvents.stream_boundary && newEvents.events) {
            let oldEventsList = streamCache;

            setStreamCache([...oldEventsList, ...newEvents.events]);

            updateStreamBoundaryWith(newEvents.stream_boundary, {
              ignoreEnd: true,
            });
          }
        },
      }
    );

  ///////////////////////////
  /// Load newest events ///
  /////////////////////////

  const { refetch: loadNewerEvents, isFetching: loadNewerEventsIsFetching } =
    useQuery(
      "stream-newest-events",
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
        refetchOnWindowFocus: false,
        refetchOnmount: false,
        refetchOnReconnect: false,
        retry: 2,
        staleTime: twentyFourHoursInMs,
        onSuccess: (newEvents) => {
          if (newEvents && newEvents.stream_boundary && newEvents.events) {
            let oldEventsList = streamCache;

            setStreamCache([...newEvents.events, ...oldEventsList]);

            if (oldEventsList.length > 0) {
              setCursor(cursor + newEvents.events.length);
            }

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

  /////////////////////
  /// latest event ///
  ///////////////////

  const {
    data: latestEvents,
    isLoading: latestEventsIsLoading,
    refetch: latestEventsRefetch,
    isFetching: latestEventsIsFetching,
    remove: latestEventsRemove,
  } = useQuery(
    "stream-latest",
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
    if (response.data) {
      setNewerEvent({ ...response.data });
    } else {
      setNewerEvent(null);
    }
    return response.data;
  };

  ///////////////////////
  /// get next event ///
  /////////////////////

  const {
    data: nextEvent,
    isLoading: nextEventIsLoading,
    refetch: nextEventRefetch,
    isFetching: nextEventIsFetching,
    remove: nextEventRemove,
  } = useQuery(
    "stream-next",
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

  ///////////////////////////
  /// get previous event ///
  /////////////////////////

  const {
    data: previousEvent,
    isLoading: previousEventIsLoading,
    refetch: previousEventRefetch,
    isFetching: previousEventIsFetching,
    remove: previousEventRemove,
  } = useQuery(
    "stream-previous",
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

  /// handle previous events
  const loadPreviousEventHandler = () => {
    if (streamCache.length > cursor + PAGE_SIZE) {
      setCursor(cursor + PAGE_SIZE);
    } else if (streamCache.length == cursor + PAGE_SIZE) {
      setCursor(cursor + PAGE_SIZE);
      loadOlderEvents();
      previousEventRefetch();
    } else {
      loadOlderEvents();
      previousEventRefetch();
    }
  };

  /// handle newest events
  const loadNewesEventHandler = () => {
    if (0 < cursor - PAGE_SIZE) {
      setCursor(cursor - PAGE_SIZE);
    } else if (0 == cursor - PAGE_SIZE) {
      setCursor(cursor - PAGE_SIZE);
      loadNewerEvents();
      nextEventRefetch();
    } else {
      loadNewerEvents();
      nextEventRefetch();
    }
  };

  return {
    streamBoundary,
    setDefaultBoundary,
    updateStreamBoundaryWith,
    events,
    eventsIsLoading,
    eventsRefetch,
    eventsIsFetching,
    eventsRemove,
    setEvents,
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
    loadPreviousEventHandler,
    loadNewesEventHandler,
    olderEvent,
  };
};
export default useStream;
