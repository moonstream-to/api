export const makeColor = () => {
  var result = "#";
  var characters = "0123456789ABCDEF";
  var charactersLength = characters.length;
  for (var i = 0; i < 6; i++) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength));
  }
  return result;
};
