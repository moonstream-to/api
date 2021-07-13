export const queryCacheProps = {
  enabled: true,
  retryDelay: (attempt) =>
    Math.min(attempt > 1 ? 2 ** attempt * 1000 : 1000, 30 * 1000),
  refetchOnWindowFocus: false,
  staleTime: 50000,
  refetchOnMount: false,
  refetchOnReconnect: false,
  retry: (failureCount, error) => {
    const status = error?.response?.status;
    return status === 404 || status === 403 ? false : true;
  },
};
