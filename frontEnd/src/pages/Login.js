import React, { Component } from "react";
import Button from "@material-ui/core/Button";
import CssBaseline from "@material-ui/core/CssBaseline";
import TextField from "@material-ui/core/TextField";
import Grid from "@material-ui/core/Grid";
import Icon from "@material-ui/core/Icon";
import Typography from "@material-ui/core/Typography";
import Container from "@material-ui/core/Container";
import Box from "@material-ui/core/Box";
import { Link, Redirect } from "react-router-dom";
import Avatar from "@material-ui/core/Avatar";
import basic from "basic-auth-token";
import axios from "axios";

class Login extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      authenticated: false,
      defaultErrorMessage: "",
      id: "",
    };
    this.authenticate = this.authenticate.bind(this);
    this.renderRedirect = this.renderRedirect.bind(this);
  }


      authenticate(event) {
        event.preventDefault();

        const userName = event.target.userName.value;
        const password = event.target.password.value;
        let token = basic(userName, password)

        console.log({token})

        axios.get("/api/login", {
          headers: {
            Authorization: `Basic ${token}`
          }
        })
          .then(response => {
            if (!response.err) {
              console.log("perro", {response});
              sessionStorage.setItem("token", response.data.token);
              this.setState({ authenticated: true, id: response.data.id });
              this.renderRedirect();  
            }
          })
          .catch(e => {
            console.log(e.response.data.err);

            this.setState({ defaultErrorMessage: e.response.data.err });
          });
      }
  
      renderRedirect() {
        console.log("redirect", this.state);
        if (this.state.authenticated) {
          this.props.history.push("/Home");
        }
      }
      

      

  render() {

    return (
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Box
          component="main"
          maxWidth="auto"
          margin="auto"
          padding="220px 0px 0"
        >
          <div>
            <Icon className="fas fa-film" />
            <Avatar src="https://m.media-amazon.com/images/S/abs-image-upload-na/1/AmazonStores/ATVPDKIKX0DER/26d289aae25c4d966ec95b641935935d.w288.h288.png" />
            <Typography component="h1" variant="h5">
              Match Roommates
            </Typography>
            <form onSubmit={this.authenticate}>
              <TextField
                variant="outlined"
                margin="normal"
                required
                fullWidth
                id="userName"
                label="Nombre de Usuario"
                name="userName"
                autoComplete="username"
                autoFocus
              />
              <TextField
                variant="outlined"
                margin="normal"
                required
                fullWidth
                name="password"
                label="Constraseña"
                type="password"
                id="password"
                autoComplete="current-password"
              />
              <div>
                
                <Typography component="h2" variant="h5" color="error">
                  
                  {/* {this.state.defaultErrorMessage} */}
                </Typography>
              </div>
             
                <Button
                  type="submit"
                  fullWidth
                  variant="contained"
                  color="primary"
                >
                  INICIAR SESIÓN
                </Button>
             
            </form>
          </div>
        </Box>
      </Container>
    );
  }
}

export default Login;
