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

import axios from "axios";

const { Typography } = atoms;

class ValidarResult extends Component {


  constructor(props) {
    super(props);
    this.state = {
      rooms: []
    };
  }

  componentDidMount(){
    let token = sessionStorage.getItem("token");

    axios.get("/api/allMatchs",{
      headers: {
        "x-access-token" : token,
      },
    }).then((response)=>{
      if(!response.err){
        let matchesD = response.data;
        let rooms2 = [];
        matchesD.matches.map((x) =>{
          rooms2.push({ rooms: x});
        });
        this.setState({rooms: rooms2});
      }
    });
  }
  

  

  render() {

    
    const { rooms } = this.state;
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
          <Box>
          <Grid container spacing={3}>
            <Grid item xs={12}>
            <Typography variant="h4" gutterBottom>
                  Piso Hombres
                </Typography>
            </Grid>
            {rooms.map((mate) => (
                <Grid item xs={3}>
                <Card variant="outlined"  borderColor="primary.main">
                <CardContent >
                    <Typography color="textPrimary" variant="h3" component="h3">
                    Habitación: {mate.rooms.room_id}
                    </Typography>
                    <hr></hr>
                    <Typography variant="h5" component="h4" mt="4">
                      Nombre: {mate.rooms.nameR}
                    </Typography>
                    <br></br>
                    <Typography variant="h5" component="h4" mt="4">
                      Apellidos: {mate.rooms.lastNR}
                    </Typography>
                    <br></br>
                  </CardContent>
                </Card>
                </Grid>

            ))}
          

          </Grid>
          </Box>
          
        
        </Box>
      </React.Fragment>
    );
  }
}

export default withTheme(theme)(ValidarResult);

/*
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
         */