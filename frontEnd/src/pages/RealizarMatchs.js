import React, { Component, useRef } from "react";
import Button from "@material-ui/core/Button";
import ButtonGroup from "@material-ui/core/ButtonGroup";
import Grid from "@material-ui/core/Grid";
import CssBaseline from "@material-ui/core/CssBaseline";
import atoms from "../components/atoms";
import molecules from "../components/molecules";
import Header from "../components/Header/Header5";
import theme from "../theme/instapaper/theme";
import withTheme from "./withTheme";
import Box from "@material-ui/core/Box";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import { Link } from "react-router-dom";
import axios from "axios";
import { makeStyles } from "@material-ui/core/styles";

const { Avatar, Icon, Typography } = atoms;
const { Tabs, Tab } = molecules;

const useStyles = makeStyles({
  editButton: {
    marginLeft: 20,
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

class RealizarMatchs extends Component {
 
  constructor(props) {
    super(props);

    this.state = {
      isButtonDisabled: false,
      isButtonDisabled1: false,
      datosHombres:[],
      datosMujeres:[],
    };
  }

  makeMatchsHombres() {
    let token = sessionStorage.getItem("token");
    axios
      .get("/api/ia/matchsHFinalTest", {
        headers: {
          "x-access-token": token,
        },
      })
      .then((response) => {
        if (!response.err){
          let dato = response.data;
          let dato2 = [];
          Object.values(dato).forEach(val => {
            dato2.push(val)
          });
         
          this.setState({datosHombres:dato2})
          console.log(this.state.datosHombres)
        }
      });

    this.setState({
      isButtonDisabled: true,
    });
  }

  makeMatchsMujeres() {
    let token = sessionStorage.getItem("token");
    axios
      .get("/api/ia/matchsMFinalTest", {
        headers: {
          "x-access-token": token,
        },
      })
      .then((response) => {
        if (!response.err){
          let dato = response.data;
          let dato2 = [];
          Object.values(dato).forEach(val => {
            dato2.push(val)
          });
         
          this.setState({datosMujeres:dato2})
          console.log(this.state.datosMujeres)
        }
      });
    this.setState({
      isButtonDisabled1: true,
    });
  }
  

  render() {
    const { datosHombres} = this.state;
  
    const { datosMujeres } = this.state;
  
    return (
      <React.Fragment>
        <CssBaseline />
        <Header />
        <Box
          component="main"
          maxWidth={735}
          margin="auto"
          padding="120px 30px 0"
        >
          <Box mb="50px">
            <Grid container spacing={3} display="center">
              <Grid item md={12}>
                <Button
                  variant="contained"
                  color="primary"
                  type="submit"
                  onClick={() => this.makeMatchsHombres()}
                  disabled={this.state.isButtonDisabled}
                >
                  Realizar Emparejamientos Hombres
                </Button>
              </Grid>
              <Grid item md={12}>
                <Button variant="contained"
                  color="primary"
                  type="submit"
                  onClick={() => this.makeMatchsMujeres()}
                  disabled={this.state.isButtonDisabled1}>
                  Realizar Emparejamientos Mujeres
                </Button>
              </Grid>
            </Grid>
            <Grid container spacing={3} display="center">
{
  datosHombres.map((dato) => (
    <Grid item xs={6} sm={"auto"} >
      <Card className={"root"} variant="outlined"  borderColor="primary.main">
     <CardContent >
       <Typography color="textPrimary" variant="h3" component="h3">
         Tiempos Cluster Hombres
       </Typography>
       <hr></hr>
       <Typography variant="h5" component="h4" mt="4">
         Tiempo Total: {dato.tiempoT}
       </Typography>
       <br></br>
       <Typography variant="h5" component="h4" mt="4">
         Tiempo Inteligencia Artificial: {dato.TimepoIA}
       </Typography>
       <br></br>
    <Typography variant="h5" component="h4" mt="4">
         Tiempo Procesado: {dato.tiempoP}
       </Typography>
       <br></br>
    <Typography variant="h5" component="h4" mt="4">
         Tiempo Clustering: {dato.tiempoC}
       </Typography>
       <br></br>
    <Typography variant="h5" component="h4" mt="4">
         Error: {dato.error}
       </Typography>
       <br></br>
       <Typography variant="h5" component="h4" mt="4">
         NFound: {dato.nS}
       </Typography>
       <br></br>
     </CardContent>
   </Card>
  
  
   </Grid>))}
   {
  datosMujeres.map((dato) => (
    <Grid item xs={6} sm={"auto"} >
      <Card className={"root"} variant="outlined"  borderColor="primary.main">
     <CardContent >
       <Typography color="textPrimary" variant="h3" component="h3">
         Tiempos Cluster Mujeres
       </Typography>
       <hr></hr>
       <Typography variant="h5" component="h4" mt="4">
         Tiempo Total: {dato.tiempoT}
       </Typography>
       <br></br>
       <Typography variant="h5" component="h4" mt="4">
         Tiempo Inteligencia Artificial: {dato.TimepoIA}
       </Typography>
       <br></br>
    <Typography variant="h5" component="h4" mt="4">
         Tiempo Procesado: {dato.tiempoP}
       </Typography>
       <br></br>
    <Typography variant="h5" component="h4" mt="4">
         Tiempo Clustering: {dato.tiempoC}
       </Typography>
       <br></br>
    <Typography variant="h5" component="h4" mt="4">
         Error: {dato.error}
       </Typography>
       <br></br>
       <Typography variant="h5" component="h4" mt="4">
         NFound: {dato.nS}
       </Typography>
       <br></br>
     </CardContent>
   </Card>
  
  
   </Grid>))}
 
            </Grid>
          </Box>
        </Box>
      </React.Fragment>
    );
  }
}

export default withTheme(theme)(RealizarMatchs);
