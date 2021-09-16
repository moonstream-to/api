/** @jsxRuntime classic */
/** @jsx jsx */
import { jsx } from "@emotion/react";
import { Flex, Image } from "@chakra-ui/react";
import CustomIcon from "../CustomIcon";
import styles from "./styles";

const Modal = ({ children, onClose }) => (
  <Flex onClick={onClose} css={styles.modal} zIndex={100002}>
    <Flex onClick={(e) => e.stopPropagation()} css={styles.flex}>
      <Image
        color="primary.900"
        height="24px"
        width="22px"
        sx={{ filter: "grayscale: 50%" }}
        fill="primary.800"
        src={
          "https://s3.amazonaws.com/static.simiotics.com/moonstream/assets/logo-black.svg"
        }
      />
      <Flex cursor="pointer" onClick={onClose} css={styles.close}>
        <CustomIcon height="13px" width="13px" icon="close" />
      </Flex>
      {children}
    </Flex>
  </Flex>
);

export default Modal;
