export const shorten = (string, length = 80) => {
  if (string.length <= length) {
    return string;
  }

  return string.substring(0, length) + "...";
};
