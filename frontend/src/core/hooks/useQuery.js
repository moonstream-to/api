import { useState } from "react";
import { useRouter } from ".";
// Hook
const useQuery = (key, initialValue, push, shallow) => {
  const { query, appendQuery } = useRouter();
  // State to store our value
  // Pass initial state function to useState so logic is only executed once
  const [storedValue, setStoredValue] = useState(() => {
    try {
      // Get from local storage by key
      const item = query[key];
      // Parse stored json or if none return initialValue
      return item ?? initialValue;
    } catch (error) {
      // If error also return initialValue
      console.warn(error);
      return initialValue;
    }
  });
  // Return a wrapped version of useState's setter function that ...
  // ... persists the new value to localStorage.
  const setValue = (value, push) => {
    try {
      // Allow value to be a function so we have same API as useState
      const valueToStore =
        value instanceof Function ? value(storedValue) : value;
      // Save state
      setStoredValue(valueToStore);
      // Save to local storage
      appendQuery(key, valueToStore, push, shallow);
    } catch (error) {
      // A more advanced implementation would handle the error case
      console.warn(error);
    }
  };
  return [storedValue, setValue];
};

export default useQuery;
