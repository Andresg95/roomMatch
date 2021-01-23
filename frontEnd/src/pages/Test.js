import React, { Component } from "react";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import IconButton from "@material-ui/core/IconButton";
import CssBaseline from "@material-ui/core/CssBaseline";
import { makeStyles } from "@material-ui/core/styles";
import useMediaQuery from "@material-ui/core/useMediaQuery";
import atoms from "../components/atoms";
import molecules from "../components/molecules";
import Header from "../components/Header/Header2";
import theme from "../theme/instapaper/theme";
import withTheme from "./withTheme";
import Box from "@material-ui/core/Box";
import axios from "axios";

import {
  Router,
  Route,
  hashHistory,
  BrowserRouter,
  Link,
} from "react-router-dom";

import EventSeat from "@material-ui/icons/EventSeat";
import Avatar1 from "@material-ui/core/Avatar";

import TextField from "../components/molecules/TextField";
import MenuItem from "../components/molecules/MenuItem";

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
  root: {
    "& .MuiTextField-root": {
      margin: theme.spacing(1),
      width: "25ch",
    },
  },
});

const Tsexo = [
  { value: "masculino", label: "Masculino" },
  { value: "femenino", label: "Femenino" },
];

const TseriesMovie = [
  { value: "series", label: "Series" },
  { value: "pelicula", label: "Películas" },
  { value: "ambas", label: "Ambas" },
];

const Ttabaco = [
  { value: "si", label: "si" },
  { value: "no", label: "no" },
];

const Talcohol = [
  { value: "si", label: "si"},
  { value: "no", label: "no"},
];

const Tparty = [
  { value: "si", label: "si" },
  { value: "no", label: "no" },
];

const Tperso = [
  { value: "intro", label: "Introvertid@" },
  { value: "extro", label: "Extrovertid@" }
];

const TordenP = [
  { value: "1", label: "1" },
  { value: "2", label: "2" },
  { value: "3", label: "3" },
  { value: "4", label: "4" },
  { value: "5", label: "5" },
  { value: "6", label: "6" },
  { value: "7", label: "7" },
  { value: "8", label: "8" },
  { value: "9", label: "9" },
  { value: "10",label: "10"},
];

const TordenC = [
  { value: "1", label: "1" },
  { value: "2", label: "2" },
  { value: "3", label: "3" },
  { value: "4", label: "4" },
  { value: "5", label: "5" },
  { value: "6", label: "6" },
  { value: "7", label: "7" },
  { value: "8", label: "8" },
  { value: "9", label: "9" },
  { value: "10",label: "10"},
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

  constructor(props) {
    super(props);
    this.state = {
      formCompleted: false,
      formCreated: false,
      gender: "",
      tabaco: "",
      seriesMovies: "",
      party: "",
      personality: "",
      orderP: "",
      orderC: "",
      alcohol: ""
    };
    this.sendTestForm = this.sendTestForm.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.returnHome = this.returnHome.bind(this);
  }

  //validation function
//si estate form is completed, send

  sendTestForm(event) {
    event.preventDefault();
    let token = sessionStorage.getItem("token");
    let headers = {
      "x-access-token": token,
    };
    
    let data = {
      gender: this.state.gender,
      age: parseInt(event.target.age.value),
      musicGender: event.target.musicGender.value,
      sport: event.target.sport.value,
      hobbie: event.target.hobbie.value,
      movieSeries: this.state.seriesMovies,
      filmGender: event.target.filmGender.value,
      tabaco: this.state.tabaco,
      alcohol: this.state.alcohol,
      party: this.state.party,
      ordenConvivencia: parseInt(this.state.orderC),
      ordenPersonal: parseInt(this.state.orderP),
      personalidad: this.state.personality
    };
    console.log({ data });
    axios.post("/api/test", data, {
      headers
    })
      .then(response => {
        if (!response.err) {
          this.setState({formCreated: true}, ()=> this.returnHome());
        }
      })
      .catch(e => {
        console.log(e.response.data.err);
        //el server fallo al crear el test
        this.setState({ defaultErrorMessage: e.response.data.err });
      });   
  }
  returnHome(){
    if(this.state.formCreated) {
      this.props.history.push("/Home") 
    }
  }

  handleChange(key, value) {
    this.setState({ [key]: value });
  }
  /**
   * 
    user_id = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    musicGender = db.Column(db.String(25))
    sport = db.Column(db.String(25))
    hobbie = db.Column(db.String(25))
    movieSeries = db.Column(db.String(10))
    filmGender = db.Column(db.String(25))
    tabaco = db.Column(db.Integer)
    alcohol = db.Column(db.Integer)
    party = db.Column(db.Integer)
    ordenConvivencia = db.Column(db.Integer)
    ordenPersonal = db.Column(db.Integer)
    personalidad = db.Column(db.String(10)) 
  */

  render() {
    const {
      gender,
      seriesMovies,
      party,
      personality,
      orderP,
      orderC,
    } = this.state;
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
            <form onSubmit={this.sendTestForm}>
              <Grid container spacing={3} display="center">
                <Grid item md={12}>
                  <Typography component="h1" variant="h3">
                    Test de Afinidad
                  </Typography>
                </Grid>
                <Grid item lg={12} width="auto">
                  <TextField
                    id="gender"
                    select
                    label="¿Cual es tu sexo?"
                    value={this.state.Tsexo}
                    onChange={(event) => this.handleChange("gender", event.target.value)}
                    helperText="Elige una respuesta"
                    fullWidth
                    margin="normal"
                  >
                    {Tsexo.map((option) => (
                      <MenuItem key={option.value} value={option.value}>
                        {option.label}
                      </MenuItem>
                    ))}
                  </TextField>
                </Grid>
                <Grid item lg={12} width="auto">
                  <TextField
                    id="age"
                    label="¿Cúal es tu edad?"
                    fullWidth
                    margin="normal"
                    multiline
                  />
                </Grid>
                <Grid item lg={12} width="auto">
                  <TextField
                    id="musicGender"
                    label="¿Cúal es tu género musical favorito?"
                    fullWidth
                    margin="normal"
                  />
                </Grid>
                <Grid item lg={12} width="auto">
                  <TextField
                    id="sport"
                    label="¿Qué deporte practicas?"
                    fullWidth
                    margin="normal"
                  />
                </Grid>
                <Grid item lg={12} width="auto">
                  <TextField
                    id="hobbie"
                    label="¿Tienes un Hobbie o pasatiempo?"
                    fullWidth
                    margin="normal"
                  />
                </Grid>
                <Grid item lg={12} width="auto">
                  <TextField
                    id="movieSeries"
                    select
                    label="¿Qué prefieres?"
                    value={this.state.TseriesMovie}
                    onChange={(event) => this.handleChange("seriesMovies", event.target.value)}
                    helperText="Elige una  respuesta"
                    fullWidth
                    margin="normal"
                  >
                    {TseriesMovie.map((option) => (
                      <MenuItem key={option.value} value={option.value}>
                        {option.label}
                      </MenuItem>
                    ))}
                  </TextField>
                </Grid>
                <Grid item lg={12} width="auto">
                  <TextField
                    id="filmGender"
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
                    value={this.state.Ttabaco}
                    onChange={(event) => this.handleChange("tabaco", event.target.value)}
                    helperText="Elige una  respuesta"
                    fullWidth
                    margin="normal"
                  >
                    {Ttabaco.map((option) => (
                      <MenuItem key={option.value} value={option.value}>
                        {option.label}
                      </MenuItem>
                    ))}
                  </TextField>
                </Grid>
                <Grid item lg={12} width="auto">
                  <TextField
                    id="alcohol"
                    select
                    label="¿Consumes Alcohol?"
                    value={this.state.Talcohol}
                    onChange={(event) => this.handleChange("alcohol",event.target.value)}
                    helperText="Elige una  respuesta"
                    fullWidth
                    margin="normal"
                  >
                    {Talcohol.map((option) => (
                      <MenuItem key={option.value} value={option.value}>
                        {option.label}
                      </MenuItem>
                    ))}
                  </TextField>
                </Grid>
                <Grid item lg={12} width="auto">
                  <TextField
                    id="party"
                    select
                    label="¿Te gustan las fiestas?"
                    value={this.state.Tparty}
                    onChange={(event) => this.handleChange("party",event.target.value)}
                    helperText="Elige una  respuesta"
                    fullWidth
                    margin="normal"
                  >
                    {Tparty.map((option) => (
                      <MenuItem key={option.value} value={option.value}>
                        {option.label}
                      </MenuItem>
                    ))}
                  </TextField>
                </Grid>
                <Grid item lg={12} width="auto">
                  <TextField
                    id="personalidad"
                    select
                    label="¿Te consideras más introvertid@ o extrovertid@?"
                    value={this.state.Tperso}
                    onChange={(event) => this.handleChange("personality",event.target.value)}
                    helperText="Elige una respuesta"
                    fullWidth
                    margin="normal"
                  >
                    {Tperso.map((option) => (
                      <MenuItem key={option.value} value={option.value}>
                        {option.label}
                      </MenuItem>
                    ))}
                  </TextField>
                </Grid>
                <Grid item lg={12} width="auto">
                  <TextField
                    id="ordenConvivencia"
                    select
                    label="En la escala de 1 a 10, 1 siendo poco y 10 mucho, ¿Qué tan importante consideras el orden y la limpieza para la convivencia?"
                    value={this.state.TordenC}
                    onChange={(event) => this.handleChange("orderC",event.target.value)}
                    helperText="Elige una respuesta"
                    fullWidth
                    margin="normal"
                    multiline
                  >
                    {TordenC.map((option) => (
                      <MenuItem key={option.value} value={option.value}>
                        {option.label}
                      </MenuItem>
                    ))}
                  </TextField>
                </Grid>
                <Grid item lg={12} width="auto">
                  <TextField
                    id="ordenPersonal"
                    select
                    label="En la escala de 1 a 10, 1 siendo poco y 10 mucho,
                    ¿Cómo te consideras respecto al orden y limpieza?"
                    value={this.state.TordenP}
                    onChange={(event) => this.handleChange("orderP",event.target.value)}
                    helperText="Elige una respuesta"
                    fullWidth
                    margin="normal"
                    multiline
                  >
                    {TordenP.map((option) => (
                      <MenuItem key={option.value} value={option.value}>
                        {option.label}
                      </MenuItem>
                    ))}
                  </TextField>
                </Grid>
              </Grid>

              <Grid>
                <Grid item mb={3}>
                  <Button
                    type="submit"
                    fullWidth
                    variant="contained"
                    color="primary"
                  >
                    Enviar
                  </Button>
                </Grid>
              </Grid>
            </form>
          </Box>
        </Box>
      </React.Fragment>
    );
  }
}

export default withTheme(theme)(TestUR);
