import React, { Component } from "react";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import CssBaseline from "@material-ui/core/CssBaseline";
import { makeStyles } from "@material-ui/core/styles";
import atoms from "../components/atoms";
import Header from "../components/Header/Header2";
import theme from "../theme/instapaper/theme";
import withTheme from "./withTheme";
import Box from "@material-ui/core/Box";
import { Link } from "react-router-dom";
import { Card, CardActions, Container } from "@material-ui/core";
import axios from "axios";

import CardContent from "@material-ui/core/CardContent";
const { Typography } = atoms;

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
    minWidth: 275,
  },
  bullet: {
    display: "inline-block",
    margin: "0 2px",
    transform: "scale(0.8)",
  },
  title: {
    fontSize: 14,
  },
  pos: {
    marginBottom: 12,
  },
});

class Result extends Component {
  //const [state,setState] = useState();
  constructor(props) {
    super(props);
    this.state = {
      roommates: [],
    };
  }

  componentWillMount() {
    let token = sessionStorage.getItem("token");
    axios
      .get("/api/result", {
        headers: {
          "x-access-token": token,
        },
      })
      .then((response) => {
        if (!response.err) {
          let roommatesD = response.data;
          let rommate2 = [];
          roommatesD.matches.map((x) => {
            rommate2.push({ roommate: x });
          });
          this.setState({ roommates: rommate2 });
        }
      });
  }

  render() {
    const { roommates } = this.state;
    //roommates.forEach((mate) => console.log(mate.roommate.lastNameR));

    return (
      <React.Fragment>
        <CssBaseline />
        <Header />
        <Grid >
          <Box
            component="main"
            maxWidth={"1000px"}
            margin="auto"
            padding="120px 30px 0"
          >
            <Box mb="25px">
              <Grid item xs={12}  >
                <Typography  component="h1" variant="h3" >
                  Resultados
                </Typography>
              </Grid>
            </Box>
            <Box mb="10px">
            <Grid container
                  direction="row"
                  justify="center"
                  alignItems="center"
                  spacing={4}>
              {roommates.map((mate) => (
                 <Grid item xs={6} sm={"auto"} >
                   <Card className={"root"} variant="outlined"  borderColor="primary.main">
                  <CardContent >
                    <Typography color="textPrimary" variant="h3" component="h3">
                      Roommate
                    </Typography>
                    <hr></hr>
                    <Typography variant="h5" component="h4" mt="4">
                      Nombre: {mate.roommate.nameR}
                    </Typography>
                    <br></br>
                    <Typography variant="h5" component="h4" mt="4">
                      Apellidos: {mate.roommate.lastNameR}
                    </Typography>
                    <br></br>
                  </CardContent>
                </Card>
               
                
                </Grid>
              ))}
              </Grid>
            </Box>
          </Box>
        </Grid>
      </React.Fragment>
    );
  }
}

export default withTheme(theme)(Result);
