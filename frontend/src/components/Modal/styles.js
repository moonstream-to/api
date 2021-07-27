import { css } from "@emotion/react";

const styles = {
  modal: css`
    position: fixed;
    align-items: center;
    justify-content: center;
    display: flex;
    left: 0;
    top: 0;
    z-index: 100;
    height: 100%;
    width: 100%;
    background: rgba(0, 0, 0, 0.5);
  `,
  flex: css`
    position: relative;
    background: #ffffff;
    flex-direction: column;
    width: 31.25rem;
    padding: 2.5rem;
    border-radius: 0.375rem;
    @media (max-width: 576px) {
      width: 100%;
      height: 100%;
      align-items: center;
      justify-content: center;
      border-radius: 0;
    }
    box-shadow: 0 11px 34px 0 rgba(0, 0, 0, 0.15);
  `,
  close: css`
    position: absolute;
    right: 38px;
    top: 38px;
  `,
};

export default styles;
