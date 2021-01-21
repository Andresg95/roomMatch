import { rgbToHex } from "@material-ui/core";
import { lightBlue } from "@material-ui/core/colors";

export default ({ attach, nest, primary, theme, red, white, BUTTON, ICON }) => ({
  MuiButton: {
    root: {
      padding: '5px 9px',
      border: '1px solid transparent',
      minWidth: 500,
      minHeight: 115,
      [attach(BUTTON.inverted)]: {
        borderColor: white.secondary,
        color: white.text,
      },
      [`${attach(BUTTON.inverted)}:hover`]: {
        borderColor: lightBlue.primary,
        background: lightBlue.primary,
      },
    },
    label: {
      textTransform: 'none',
      fontWeight: 666,
      lineHeight: '45px',
      [nest(ICON.root)]: {
        fontSize: 20,
      },
      [nest(ICON.left)]: {
        marginRight: theme.spacing(1),
      },
      [nest(ICON.right)]: {
        marginLeft: theme.spacing(1),
      },
    },
    outlined: {
      borderColor: '#00a8d6',
      '&$disabled.inverted': {
        borderColor: red.text,
        color: white.text,
      },
    },
    contained: {
      boxShadow: theme.shadows[0],
      '&$focusVisible': {
        boxShadow: theme.shadows[0],
      },
      '&:active': {
        boxShadow: theme.shadows[0],
      },
      '&$disabled': {
        boxShadow: theme.shadows[0],
      },
      [attach(BUTTON.danger)]: {
        color: white.text,
        background: red.main,
      },
      [`${attach(BUTTON.danger)}:hover`]: {
        background: red.dark,
      },
    },
    containedPrimary: {
      '&:hover': {
        backgroundColor: primary.main,
      },
      '&:active': {
        opacity: 0.6,
      },
    },
  },
});
