import React, { Component } from "react";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import IconButton from "@material-ui/core/IconButton";
import CssBaseline from "@material-ui/core/CssBaseline";
import { makeStyles } from "@material-ui/core/styles";
import useMediaQuery from "@material-ui/core/useMediaQuery";
import atoms from "../components/atoms";
import molecules from "../components/molecules";
import Header from "../components/Header/Header3";
import theme from "../theme/instapaper/theme";
import withTheme from "./withTheme";
import Box from "@material-ui/core/Box";
import { Router, Route, hashHistory, BrowserRouter, Link } from "react-router";
import EventSeat from "@material-ui/icons/EventSeat";
import Avatar1 from "@material-ui/core/Avatar";
import axios from "axios";

import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';
import token from "basic-auth-token";

const { Avatar, Icon  } = atoms;
const { Tabs, Tab } = molecules;
const useStyles = makeStyles({
  editButton: {
    marginLeft: 0,
    marginTop: 12,
    [theme.breakpoints.up("sm")]: {
      marginLeft: 20,
      marginTop: 0
    }
  },
  settings: {
    [theme.breakpoints.up("sm")]: {
      marginLeft: 5
    }
  },
  root: {
    minWidth: 275,
  },
  bullet: {
    display: 'inline-block',
    margin: '0 2px',
    transform: 'scale(0.8)',
  },
  title: {
    fontSize: 14,
  },
  pos: {
    marginBottom: 12,
  },
});

class Profile extends Component {


  constructor(props){
    super(props);
    this.state={
      name: "",
      lastname: "",
      sharedRoom: ""
    }
  }

  componentWillMount(){

    let token = sessionStorage.getItem("token");
    console.log("token",token);
    axios.get("/api/perfil", { headers : {
      "x-access-token" : token
    }})
    .then(response=>{
      if (!response.err) {
        let {resident} = response.data;
        this.setState({name : resident.name, lastname: resident.lastName, sharedRoom: resident.sharedRoom})
         
      }
    })


  }
 
  render() {

    
    const bull = <span className={"bullet"}>•</span>;
    const { name, lastname, sharedRoom } = this.state;
    const roomtext = (sharedRoom==0) ? "No"  : "si";
    
    return (
      <React.Fragment>
        <CssBaseline />
        <Header />
        <Grid>
          <Box
            component="main"
            maxWidth={"600px"}
            margin="auto"
            padding="120px 30px 0"
          >
            <Box>
            <Card className={"root"} variant="outlined">
              <CardContent>
                <Typography
                  color="textPrimary"
                  variant="h3"
                  component="h3"
                >
                  Datos personales
                </Typography>
                <hr></hr>
                <Typography variant="h5" component="h4"  mt="4">
                  {bull} Nombre: {name}
                </Typography><br></br>
                <Typography  variant="h5" component="h4" mt="4">
                {bull} Apellidos: {lastname}
                </Typography><br></br>
                <Typography  variant="h5" component="h4" mt="4">
                {bull} Cuarto Compartido: {roomtext}
            </Typography>
              </CardContent>
            </Card>
            </Box>
            
          </Box>
        </Grid>
      </React.Fragment>
    );
  }
}

export default withTheme(theme)(Profile);
