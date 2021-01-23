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


const { Typography } = atoms;

class ValidarResult extends Component {
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

        <Box
          component="main"
          maxWidth={"auto"}
          margin="auto"
          padding="120px 30px 0"
        >
          <Grid container justify="center" alignItems="baseline">
            <Box mb="100px">
              <Grid item md={12}>
                <Typography variant="h4" gutterBottom>
                  Pisos de 5 Personas
                </Typography>
                <Grid
                  container
                  direction="column"
                  justify="center"
                  alignItems="flex-start"
                  spacing={4}
                >
                  <Grid item mb={6}>
                    <Card>
                      <CardContent>
                        <Typography variant="h5" component="h2">
                          Habitación 001
                        </Typography>
                        <Typography>UsuarioResidente 000X</Typography>
                        <Typography>UsuarioResidente 000X</Typography>
                        <Typography>UsuarioResidente 000X</Typography>
                        <Typography>UsuarioResidente 000X</Typography>
                        <Typography>UsuarioResidente 000X</Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                  <Grid item mb={6}>
                    <Card>
                      <CardContent>
                        <Typography variant="h5" component="h2">
                          Habitación 002
                        </Typography>
                        <Typography>UsuarioResidente 000X</Typography>
                        <Typography>UsuarioResidente 000X</Typography>
                        <Typography>UsuarioResidente 000X</Typography>
                        <Typography>UsuarioResidente 000X</Typography>
                        <Typography>UsuarioResidente 000X</Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                  <Grid item mb={6}>
                    <Card>
                      <CardContent>
                        <Typography variant="h5" component="h2">
                          Habitación 003
                        </Typography>
                        <Typography>UsuarioResidente 000X</Typography>
                        <Typography>UsuarioResidente 000X</Typography>
                        <Typography>UsuarioResidente 000X</Typography>
                        <Typography>UsuarioResidente 000X</Typography>
                        <Typography>UsuarioResidente 000X</Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                </Grid>
                
              </Grid>
            </Box>
            



            <Grid item md={3}></Grid>



            <Box mb="100px">
              <Grid item mb={12}>
                <Typography variant="h4" gutterBottom>
                  Estudios Compartidos
                </Typography>
                <Grid
                  container
                  direction="column"
                  justify="center"
                  alignItems="flex-start"
                  spacing={4}
                >
                  <Grid item mb={6}>
                    <Card>
                      <CardContent>
                        <Typography variant="h5" component="h2">
                          Estudio 001
                        </Typography>
                        <Typography>UsuarioResidente 000X</Typography>
                        <Typography>UsuarioResidente 000X</Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                  <Grid item mb={6}>
                    <Card>
                      <CardContent>
                        <Typography variant="h5" component="h2">
                        Estudio 002
                        </Typography>
                        <Typography>UsuarioResidente 000X</Typography>
                        <Typography>UsuarioResidente 000X</Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                  <Grid item mb={6}>
                    <Card>
                      <CardContent>
                        <Typography variant="h5" component="h2">
                        Estudio 003
                        </Typography>
                        <Typography>UsuarioResidente 000X</Typography>
                        <Typography>UsuarioResidente 000X</Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                </Grid>
                


              </Grid>
            </Box>



            <Box mb="40px">
              <Grid>
                <ButtonGroup
                  variant="contained"
                  color="primary"
                  aria-label="contained primary button group"
                >
                  <Grid item mb={3}>
                    <Button>Guardar</Button>
                  </Grid>
                  <Grid item mb={3}>
                    <Button>Validar</Button>
                  </Grid>
                </ButtonGroup>
              </Grid>
            </Box>
          </Grid>
        </Box>
      </React.Fragment>
    );
  }
}

export default withTheme(theme)(ValidarResult);
