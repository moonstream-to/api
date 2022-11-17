/* eslint-disable react/react-in-jsx-scope */
import styles from "./PlainButton.module.css";

const PlainButton = (props) => {
  return (
    <div
      onClick={props.onClick}
      className={styles.button}
      style={props.style}
      type={props.type}
    >
      {props.children}
    </div>
  );
};
export default PlainButton;
