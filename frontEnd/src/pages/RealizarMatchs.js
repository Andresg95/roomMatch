import React, { Component } from "react";
import Button from "@material-ui/core/Button";
import ButtonGroup from "@material-ui/core/ButtonGroup";
import Grid from "@material-ui/core/Grid";
import CssBaseline from "@material-ui/core/CssBaseline";
import atoms from "../components/atoms";
import Header from "../components/Header/Header3";
import theme from "../theme/instapaper/theme";
import withTheme from "./withTheme";
import Box from "@material-ui/core/Box";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import { Link } from "react-router-dom";

class RealizarMatchs extends Component {


    render(){
        return(
            <React.Fragment>
                <CssBaseline />
                <Header/>
                <Box
          component="main"
          maxWidth={"auto"}
          margin="auto"
          padding="120px 30px 0"
        >
            <Grid container justify="center" alignItems="baseline">

            

            </Grid>
        
        </Box>

            </React.Fragment>
        )
    }
}

export default withTheme(theme)(RealizarMatchs);