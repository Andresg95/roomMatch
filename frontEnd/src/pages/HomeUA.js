/**
 * HomeUA es para los Usuarios Residentes y tendra Header4
 *  **/
import React, { Component } from "react";
import ReactDOM from "react-dom";
import Button from "@material-ui/core/Button";
import ButtonGroup from "@material-ui/core/ButtonGroup";
import Grid from "@material-ui/core/Grid";
import IconButton from "@material-ui/core/IconButton";
import CssBaseline from "@material-ui/core/CssBaseline";
import { makeStyles } from "@material-ui/core/styles";
import useMediaQuery from "@material-ui/core/useMediaQuery";
import atoms from "../components/atoms";
import molecules from "../components/molecules";
import Header from "../components/Header/Header4";
import theme from "../theme/instapaper/theme";
import withTheme from "./withTheme";
import Box from "@material-ui/core/Box";
import styles from "./Home.css";
import { Link } from "react-router-dom";

const { Avatar, Icon, Typography } = atoms;
const { Tabs, Tab } = molecules;

const useStyles = makeStyles({
  editButton: {
    marginLeft: 0,
    marginTop: 12,
    [theme.breakpoints.up("sm")]: {
      marginLeft: 20,
      marginTop: 0,
    },
  },
  settings: {
    [theme.breakpoints.up("sm")]: {
      marginLeft: 5,
    },
  },
});

class HomeUA extends Component {
  /*constructor(props) {
    super(props);
      // const [tabIndex, setTabIndex] = React.useState(0);
      // const classes = useStyles();
      // const upSm = useMediaQuery(theme.breakpoints.up("sm"), {
      //   defaultMatches: true
      // });
  }*/

  render() {
    return (
      <React.Fragment>
        <CssBaseline />
        <Header />
        <Box
          component="main"
          maxWidth={935}
          margin="auto"
          padding="100px 140px 0"
        >
          <Box mb="44px">
            <Grid container spacing={3} display="center">
              <Grid item md={12}>
              <Link to="/ValidarR" id="link">
              <Button variant="contained" color="primary">
                  Validar Resultados
                </Button>
              </Link>
              </Grid>
              <Grid item md={12}>
              <Button variant="contained" color="primary">
                  Realizar Matchs
              </Button>
              </Grid>
            </Grid>
          </Box>
        </Box>
      </React.Fragment>
    );
  }
}

export default withTheme(theme)(HomeUA);
