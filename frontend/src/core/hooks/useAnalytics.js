import AnalyticsContext from "../providers/AnalyticsProvider/context";
import { useContext } from "react";
import { useState, useEffect } from "react";
import {
  MIXPANEL_PROPS,
  MIXPANEL_EVENTS,
} from "../providers/AnalyticsProvider/constants";

const useAnalytics = () => {
  const { mixpanel, isLoaded } = useContext(AnalyticsContext);
  const [eventsQueue, setEventsQueue] = useState([]);

  const track = (e, props) => {
    setEventsQueue((trackingQueue) => [
      ...trackingQueue,
      {
        event: e,
        props: props,
      },
    ]);
  };

  useEffect(() => {
    if (isLoaded && eventsQueue.length > 0 && mixpanel) {
      const newTrackingQueue = [...eventsQueue];
      const newTrackEvent = newTrackingQueue.pop();
      mixpanel.track(newTrackEvent.event, newTrackEvent.props);
      setEventsQueue(newTrackingQueue);
    }
  }, [isLoaded, mixpanel, eventsQueue]);

  const withTracking = (fn, event, props) => {
    track(event, props);
    return fn;
  };

  return {
    mixpanel,
    isLoaded,
    track,
    MIXPANEL_PROPS,
    MIXPANEL_EVENTS,
    withTracking,
  };
};
export default useAnalytics;
