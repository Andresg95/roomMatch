import React, { Component } from "react";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import IconButton from "@material-ui/core/IconButton";
import CssBaseline from "@material-ui/core/CssBaseline";
import { makeStyles } from "@material-ui/core/styles";
import useMediaQuery from "@material-ui/core/useMediaQuery";
import atoms from "../components/atoms";
import molecules from "../components/molecules";
import Header from "../components/Header/Header1";
import theme from "../theme/instapaper/theme";
import withTheme from "./withTheme";
import Box from "@material-ui/core/Box";
import { Router, Route, hashHistory, BrowserRouter, Link } from "react-router-dom";
import EventSeat from "@material-ui/icons/EventSeat";
import Avatar1 from "@material-ui/core/Avatar";
import Axios from "../api/Axios";
import TextField from "../components/molecules/TextField";
import MenuItem from "../components/molecules/MenuItem";

const { Avatar, Icon, Typography } = atoms;

const { Tabs, Tab} = molecules;

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
  root: {
    '& .MuiTextField-root': {
      margin: theme.spacing(1),
      width: '25ch',
    }}
});

const Tsexo = [
  {
    value: "masculino",
    label: "Masculino",
  },
  {
    value: "femenino",
    label: "Femenino",
  },
];


class TestUR extends Component {
  /**
   * Aqui se tendria que realizar las funciones de HandleClick(), para:
   * Sexo {Tsexo}
   * Pelicula, serie o ambas {Que prefieres}
   * Consume tabaco y / o Alcohol
   * Fiestas
   * Intro/extro
   * 1-10 Importate el orden
   * 1-10 como de ordenado eres
   */

  render() {
    return (
      <React.Fragment>
        <CssBaseline />
        <Header />
        <Box
          component="main"
          maxWidth={"auto"}
          margin="auto"
          padding="85px 364px 10px"
        >
          <Box width="900">
            <Grid container spacing={3} display="center">
              <Grid item md={12}>
                <Typography component="h1" variant="h3">
                  Test de Afinidad
                </Typography>
              </Grid>
              <Grid item lg={12} width="auto">
                <TextField
                  id="sexo"
                  select
                  label="¿Cual es tu sexo?"
                  value={Tsexo}
                  helperText="Elige una  respuesta"
                  fullWidth
                  margin="normal"
                >
                  <MenuItem>Femenino</MenuItem>
                  <MenuItem>Masculino</MenuItem>
                </TextField>
              </Grid>
              <Grid item lg={12} width="auto">
                <TextField
                  id="filled-basic"
                  label="¿Cúal es tu edad?"
                  fullWidth
                  margin="normal"
                  multiline
                />
              </Grid>
              <Grid item lg={12} width="auto">
                <TextField
                  id="filled-basic"
                  label="¿Cúal es tu género musical favorito?"
                  fullWidth
                  margin="normal"
                />
              </Grid>
              <Grid item lg={12} width="auto">
                <TextField
                  id="filled-basic"
                  label="¿Qué deporter practicas?"
                  fullWidth
                  margin="normal"
                />
              </Grid>
              <Grid item lg={12} width="auto">
                <TextField
                  id="filled-basic"
                  label="¿Tienes un Hobbie o pasatiempo?"
                  fullWidth
                  margin="normal"
                />
              </Grid>
              <Grid item lg={12} width="auto">
                <TextField
                  id="prefieresSeriesPeliculas"
                  select
                  label="¿Qué prefieres?"
                  helperText="Elige una  respuesta"
                  fullWidth
                  margin="normal"
                >
                  <MenuItem>Series</MenuItem>
                  <MenuItem>Película</MenuItem>
                  <MenuItem>Ambas</MenuItem>
                </TextField>
              </Grid>
              <Grid item lg={12} width="auto">
                <TextField
                  id="filled-basic"
                  label="¿Género favorito de la pregunta anterior?"
                  fullWidth
                  margin="normal"
                />
              </Grid>
              <Grid item lg={12} width="auto">
                <TextField
                  id="tabaco"
                  select
                  label="¿Fumas Tabaco?"
                  helperText="Elige una  respuesta"
                  fullWidth
                  margin="normal"
                >
                  <MenuItem>Sí</MenuItem>
                  <MenuItem>No</MenuItem>
                </TextField>
              </Grid>
              <Grid item lg={12} width="auto">
                <TextField
                  id="alcohol"
                  select
                  label="¿Consumes Alcohol?"
                  helperText="Elige una  respuesta"
                  fullWidth
                  margin="normal"
                >
                  <MenuItem>Sí</MenuItem>
                  <MenuItem>No</MenuItem>
                </TextField>
              </Grid>
              <Grid item lg={12} width="auto">
                <TextField
                  id="fiesta"
                  select
                  label="¿Te gustan las fiestas?"
                  helperText="Elige una  respuesta"
                  fullWidth
                  margin="normal"
                >
                  <MenuItem>Sí</MenuItem>
                  <MenuItem>No</MenuItem>
                </TextField>
              </Grid>
              <Grid item lg={12} width="auto">
                <TextField
                  id="introExtro"
                  select
                  label="¿Te consideras más introvertid@ o extrovertid@?"
                  helperText="Elige una respuesta"
                  fullWidth
                  margin="normal"
                >
                  <MenuItem>Introvertid@</MenuItem>
                  <MenuItem>Extrovertid@</MenuItem>
                </TextField>
              </Grid>          
              <Grid item lg={12} width="auto">
                <TextField
                  id="standard-textarea"
                  select
                  label="En la escala de 1 a 10, 1 siendo poco y 10 mucho, ¿Qué tan importante consideras el orden y la limpieza para la convivencia?"
                  helperText="Elige una respuesta"
                  fullWidth
                  margin="normal"
                  multiline
                >
                  <MenuItem>1</MenuItem>
                  <MenuItem>2</MenuItem>
                  <MenuItem>3</MenuItem>
                  <MenuItem>4</MenuItem>
                  <MenuItem>5</MenuItem>
                  <MenuItem>6</MenuItem>
                  <MenuItem>7</MenuItem>
                  <MenuItem>8</MenuItem>
                  <MenuItem>9</MenuItem>
                  <MenuItem>10</MenuItem>
                </TextField>
              </Grid>
              <Grid item lg={12} width="auto">
                <TextField
                  id="standard-textarea"
                  select
                  label="En la escala de 1 a 10, 1 siendo poco y 10 mucho, ¿Cómo te consideras respecto al orden y limpieza?"
                  helperText="Elige una respuesta"
                  fullWidth
                  margin="normal"
                  multiline
                >
                  <MenuItem>1</MenuItem>
                  <MenuItem>2</MenuItem>
                  <MenuItem>3</MenuItem>
                  <MenuItem>4</MenuItem>
                  <MenuItem>5</MenuItem>
                  <MenuItem>6</MenuItem>
                  <MenuItem>7</MenuItem>
                  <MenuItem>8</MenuItem>
                  <MenuItem>9</MenuItem>
                  <MenuItem>10</MenuItem>
                </TextField>
              </Grid>
            </Grid>
          </Box>
          <Box mb="40px">
              <Grid>
                  <Grid item mb={3}>
                    <Link to="/Home" id="link">
                    <Button variant="outlined" color="primary" >Enviar</Button>
                    </Link>
                  
                  </Grid>
              </Grid>
            </Box>
        </Box>
      </React.Fragment>
    );
  }
}

export default withTheme(theme)(TestUR);
