import React, { Component } from "react";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import IconButton from "@material-ui/core/IconButton";
import CssBaseline from "@material-ui/core/CssBaseline";
import { makeStyles } from "@material-ui/core/styles";
import useMediaQuery from "@material-ui/core/useMediaQuery";
import atoms from "../components/atoms";
import molecules from "../components/molecules";
import Header from "../components/Header/Header3";
import theme from "../theme/instapaper/theme";
import withTheme from "./withTheme";
import Box from "@material-ui/core/Box";
import { Router, Route, hashHistory, BrowserRouter, Link } from "react-router";
import EventSeat from "@material-ui/icons/EventSeat";
import Avatar1 from "@material-ui/core/Avatar";
import axios from "axios";

import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';
import token from "basic-auth-token";

const { Avatar, Icon  } = atoms;
const { Tabs, Tab } = molecules;
const useStyles = makeStyles({
  editButton: {
    marginLeft: 0,
    marginTop: 12,
    [theme.breakpoints.up("sm")]: {
      marginLeft: 20,
      marginTop: 0
    }
  },
  settings: {
    [theme.breakpoints.up("sm")]: {
      marginLeft: 5
    }
  },
  root: {
    minWidth: 275,
  },
  bullet: {
    display: 'inline-block',
    margin: '0 2px',
    transform: 'scale(0.8)',
  },
  title: {
    fontSize: 14,
  },
  pos: {
    marginBottom: 12,
  },
});

class Profile extends Component {


  constructor(props){
    super(props);
    this.state={
      name: "",
      lastname: "",
      sharedRoom: "- -"
    }
  }

  componentWillMount(){

    let token = sessionStorage.getItem("token");

    axios.get("/api/perfil", { headers : {
      "x-access-token" : token
    }})
    .then(response=>{
      if (!response.err) {
        let {resident} = response.data;
        this.setState({name : resident.name, lastname: resident.lastName, sharedRoom: resident.sharedRoom})
         
      }
    })


  }
  /*
  constructor(props) {
    super(props);
    this.state = {
      transactions: [],
      username: "",
      email: "",
      popcorns_global: 0,
      followers: [],
      following: [],
      favorites: [],
      watched: [],
      inTheWorks: [],
      messageButton: "",
      reviews: [],
      numPopcorns: 0
    };

    this.checkUser = this.checkUser.bind(this);
    this.handleOnClick = this.handleOnClick.bind(this);

  }
 
  componentDidUpdate(prevProps) {
    const {
      match: {
        params: { userId: prevUserId }
      }
    } = prevProps;

    const {
      match: {
        params: { userId }
      }
    } = this.props;
    if (userId !== prevUserId) {
      this.checkUser();
      this.fetchDataUser(userId);
    }
  }
  

  fetchDataUser = id => {
    Axios.get(`/user/${id}`)
      .then(response => {
        return response.data;
      })
      .then(dataUser => {
        this.setState({
          transactions: dataUser.transactions,
          username: dataUser.username,
          email: dataUser.email,
          popcorns_global: dataUser.popcorns_global,
          followers: dataUser.followers,
          following: dataUser.Following,
          reviews: dataUser.reviews
        });
        this.getFollowers(dataUser.followers);
        this.getFollowing(dataUser.Following);
        this.handlePopcorns();
        this.handleFavorites();
        this.handleWatched();
        this.handleInTheWorks();
      });
  };


  checkUser() {
    const {
      match: {
        params: { userId }
      }
    } = this.props;
    if (sessionStorage.getItem("idUser") !== userId) {
      if (
        JSON.parse(localStorage.getItem("Following")).filter(
          user => userId == user
        ).length > 0
      ) {
        this.setState({ messageButton: "Dejar de seguir" });
      } else {
        this.setState({ messageButton: "Seguir" });
      }
    }
  }

  handleOnClick(userId) {
    let oldFollowing = JSON.parse(localStorage.getItem("Following"));
    if (oldFollowing.filter(user => userId == user).length > 0) {
      oldFollowing = oldFollowing.filter(user => userId != user);
      localStorage.setItem("Following", JSON.stringify(oldFollowing));
      this.handleDejarDeSeguir(userId);
    } else {
      oldFollowing.push(userId);
      localStorage.setItem("Following", JSON.stringify(oldFollowing));
      this.handleSeguir(userId);
    }
  }

*/



  render() {

    
    const bull = <span className={"bullet"}>•</span>;
    const { name, lastname, sharedRoom } = this.state;
    const roomtext = (sharedRoom==0) ? "null" : sharedRoom;
    
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
            <Box>
            <Card className={"root"} variant="outlined">
              <CardContent>
                <Typography
                  className={"title"}
                  color="textSecondary"
                  gutterBottom
                >
                  Datos personales
                </Typography>
                <Typography variant="h5" component="h2">
                  {bull} Nombre: {name}
                </Typography>
                <Typography  variant="h5" component="h2">
                {bull} Apellidos: {lastname}
                </Typography>
                <Typography className={"pos"} color="textSecondary">
                Cuarto Compartido: {roomtext}
            </Typography>
              </CardContent>
              <CardActions>
                <Button size="small">Learn More</Button>
              </CardActions>
            </Card>
            </Box>
            
          </Box>
        </Grid>
      </React.Fragment>
    );
  }
}

export default withTheme(theme)(Profile);
