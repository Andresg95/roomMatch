import React, { Component } from "react";
import Home from "./pages/HomeUR";
//import Axios from "./api/Axios";

class App extends Component {

  /*constructor(props) {
    super(props);
    this.state = {
      peliculasDrama: [],
      peliculasAction: [],
      peliculasComedia: []
    };
  }*/

/*
  componentWillMount() {
    Axios.get("/movies/landing/?genre=Drama").then(response => {
      console.log("axios fetching response drama", response.data);
      this.setState({ peliculasDrama: response.data });
    });

    Axios.get("/movies/landing/?genre=Action").then(response => {
      this.setState({ peliculasAction: response.data });
    });

    Axios.get("/movies/landing/?genre=Comedy").then(response => {
      this.setState({ peliculasComedia: response.data });
    });
  }
*/

  render() {
    return (
      <div className="app">
        <Home/>
      </div>
    );
  }
}

export default App;
