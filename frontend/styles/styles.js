import { css } from "@emotion/react";

const styles = {
  container: css`
    & > div {
      width: 100%;
    }
    * {
      max-width: 100%;
    }
  `,

  saveButton: css`
    position: fixed;
    z-index: 9;
    bottom: 20px;
    right: 20px;
    border-radius: 100px;
    width: 64px;
    height: 64px;
    padding: 0;

    img {
      height: 24px;
    }
  `,
  reactMde: css`
    .react-mde {
      border: none;
      width: 100%;
      overflow: hidden;

      .react-mde-tabbed-layout {
        overflow: visible;
        max-height: calc(100% - 49px);
      }

      .mde-header {
        background: transparent;
        padding-left: 10px;
        border-color: #eaebf7;
        flex-wrap: nowrap;

        .mde-tabs {
          button {
            margin-top: 0px;
            margin-bottom: 0px;
            overflow: clip;

            padding: 0px;
            font-size: 0.875rem;

            &.selected {
              font-weight: bold;
              border: none;
            }

            &:first-of-type {
              order: 2;
            }
          }
        }

        .svg-icon {
          transform: scale(0.8);
          opacity: 0.7;
        }
      }

      .mde-textarea-wrapper {
        textarea.mde-text {
          padding: 1rem;
          overflow: scroll;
          display: flex;
          flex-grow: 1;
        }
      }

      .mde-preview-content {
        overflow: initial;
      }

      .grip {
        display: none;
      }
    }
  `,
};

export default styles;
