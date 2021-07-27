/** @jsxRuntime classic */
/** @jsx jsx */
import { jsx } from "@emotion/react";
import { Flex } from "@chakra-ui/react";
import CustomIcon from "../CustomIcon"
import styles from "./styles";

const Modal = ({ children, onClose }) => (
  <Flex onClick={onClose} css={styles.modal}>
    <Flex onClick={(e) => e.stopPropagation()} css={styles.flex}>
      <CustomIcon height="24px" width="22px" icon="logo" />
      <Flex cursor="pointer" onClick={onClose} css={styles.close}>
        <CustomIcon height="13px" width="13px" icon="close" />
      </Flex>
      {children}
    </Flex>
  </Flex>
);

export default Modal;
