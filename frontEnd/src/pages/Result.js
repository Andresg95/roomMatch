import React, { Component } from "react";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import CssBaseline from "@material-ui/core/CssBaseline";
import atoms from "../components/atoms";
import Header from "../components/Header/Header1";
import theme from "../theme/instapaper/theme";
import withTheme from "./withTheme";
import Box from "@material-ui/core/Box";
import { Link } from "react-router-dom";
import Axios from "../api/Axios";


const { Typography } = atoms;

class Result extends Component {
  
  /*
  constructor(props) {
    super(props);
    this.state = {
      poster: "",
      title: "",
      year: "",
      genre: "",
      runtime: "",
      director: "",
      writer: "",
      plot: "",
      actors: "",
      imdbid: "",
      reviews: []
    };


  }
*/

/*
  fetchData(id) {
    Axios.get(`/movie/${id}`)
      .then(response => {
        return response.data;
      })
      .then(peliculaData => {
        this.setState({
          poster: peliculaData.poster,
          title: peliculaData.title,
          year: peliculaData.year,
          genre: peliculaData.genre,
          runtime: peliculaData.runtime,
          director: peliculaData.director,
          writer: peliculaData.writer,
          plot: peliculaData.plot,
          actors: peliculaData.actors,
          imdbid: peliculaData.imdbid,
          reviews: peliculaData.reviews || "No reviews yet"
        });
        console.log("this is imdbid", peliculaData.imdbid);
        console.log("this in state", this.state.imdbid);
      });
  }
*/

  render() {
    return (
      <React.Fragment>
        <CssBaseline />
        <Header />
        <Grid>
          <Box
            component="main"
            maxWidth={"auto"}
            margin="auto"
            padding="120px 30px 0"
          >
          </Box><Box></Box>
        </Grid>
      </React.Fragment>
    );
  }
}

export default withTheme(theme)(Result);
