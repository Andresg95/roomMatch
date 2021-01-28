import React, { Component,useEffect,useState} from "react";
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
import axios from "axios";

const { Typography } = atoms;

// const roommatesTest = [
//   {
//     name: "Douglas",
//     lastName: "rodriguez"
//   },
//   {
//     name: "Carlos",
//     lastName: "Garcia"
//   },
//   {
//     name: "Jose ",
//     lastName: "Aquino"
//   },
//   {
//     name: "Clara",
//     lastName: "Romes"
//   },
// ];
// let theArray = [
//   {
//     nameR: '',
//     latsName: '',
//   }
// ]
class Result extends Component {
  //const [state,setState] = useState();
  constructor(props) {
    super(props);
    this.state = {
      roommates: [],
    };
  }
  
  //useEffect((props) => {
    // Actualiza el título del documento usando la API del navegador
    
  //});
   // let token = sessionStorage.getItem("token");
   /* axios.get("/api/result", { headers: { "x-access-token" :token}})
    .then(res => res.json())
    .then((result)=>{
      //theArray[0].nameR = result.nameR;
      //console.log(result);

    })*/
  

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
          /*let tmArray = [];
          let [data] = response.data;
          for (let i = 0; i < data.result.lenght; i++) {
            tmArray.push(data.result[i].nameR,data.result[i].lastNameR);
          }
          this.setState({ roommates: tmArray });*/
          this.setState({roommates:response.data})
          let rommate2 = [] 
          this.state.roommates.matches.map(x=>{
            rommate2.push(x)
          })
          this.setState({roommates:rommate2})
          }
        }
      )
  }
  
  
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
              <Grid item ml={12}>
                <Typography component="h1" variant="h3">
                  Resultados
                </Typography>
              </Grid>
              <Container>
                <h1>
                {this.state.roommates[0]}
                </h1>
                {/* {this.state.roommates} */}
                {/* {this.state.roommates.map((option) => (
                  <Card  variant="outlined">
                  <Typography variant="h5" component="h2">
                  {option.nameR}
               </Typography>
               <Typography variant="h5" component="h2">
                  {option.lastNameR}
               </Typography>
                      </Card>
                    ))}    */}
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
