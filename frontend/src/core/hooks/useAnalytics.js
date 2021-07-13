import AnalyticsContext from "../providers/AnalyticsProvider/context";
import { useContext } from "react";
import { useState, useEffect, useCallback } from "react";
const useAnalytics = () => {
  const { mixpanel, isLoaded, MIXPANEL_EVENTS, MIXPANEL_PROPS } = useContext(
    AnalyticsContext
  );
  const [trackProps, setTrackProps] = useState({
    event: null,
    props: null,
    queued: false,
  });

  const track = useCallback((e, props) => {
    setTrackProps({ event: e, props: props, queued: true });
  }, []);

  useEffect(() => {
    if (isLoaded && trackProps.queued === true) {
      mixpanel.track(trackProps.event, trackProps.props);
      setTrackProps({ event: null, props: null, queued: false });
    }
  }, [isLoaded, mixpanel, trackProps]);

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
