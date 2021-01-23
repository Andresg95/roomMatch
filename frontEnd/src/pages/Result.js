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
import { Card, CardActions, Container } from "@material-ui/core";



const { Typography } = atoms;

const roommatesTest = [
  {
    name: "Douglas",
    lastName: "rodriguez"
  },
  {
    name: "Carlos",
    lastName: "Garcia"
  },
  {
    name: "Jose ",
    lastName: "Aquino"
  },
  {
    name: "Clara",
    lastName: "Romes"
  },
];

class Result extends Component {
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
                <Grid item  ml={12}>
                  <Typography component="h1" variant="h3">
                    Resultados
                  </Typography>
                </Grid>
                <Container>
                {roommatesTest.map((option) => (
                  <Card key={option.value} value={option.value} variant="outlined">
                  <Typography variant="h5" component="h2">
                  {option.name}
               </Typography>
               <Typography variant="h5" component="h2">
                  {option.lastName}
               </Typography>
                      </Card>
                    ))}
                </Container>
                {/* <Card variant="outlined">
               
                <Typography variant="h5" component="h2">
                  Nombre de tu compañero de habitación 
               </Typography>
               <br>
               </br>
       <br></br>
       <br></br>
       <br></br>                </Card> */}
       

                </Grid>
              
                </Box>
          </Box>
      </React.Fragment>
    );
  }
}

export default withTheme(theme)(Result);
