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
import axios from "axios";

const { Typography } = atoms;

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
          let roommatesD = response.data;
          let rommate2 = [];
          roommatesD.matches.map((x) => {
            rommate2.push({"roommate":x});
          });

          this.setState({ roommates: rommate2 });
          // console.log(this.state.roommates)
        }
      });
  }

  render() {
    const { roommates } = this.state;
    //console.log("1", { roomSS: roommates });

    roommates.forEach(mate => console.log(mate.roommate.lastNameR))

    // for (const mate in roommates ) {
    //    return (
    //     <div>{roommates[mate].lastNameR}</div>
    //     <div>{roommates[mate].nameR}</div>
    //     <div>{roommates[mate].room_id}</div>
    //    )
         
    // }
    // for (const [roommates, value] of elements.entries()) {
    //   items.push(<li key={index}>{value}</li>)
    // }

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
                <div>
                  {
                  roommates.map(mate=>
                    <Typography component="h1" variant="h3"> {mate.roommate.lastNameR}</Typography> 
                     )
                  
                  }

                </div>
                <Box>
               
                 
                </Box>
              </Container>
            </Grid>
          </Box>
        </Box>
      </React.Fragment>
    );
  }
}

export default withTheme(theme)(Result);
