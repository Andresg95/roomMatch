import React from "react";
import App from "./App";
import Login from "./pages/Login";
import Result from "./pages/Result";
import Profile from "./pages/Profile";
import HomeUR from "./pages/HomeUR";
import HomeUA from "./pages/HomeUA";
import TestUR from "./pages/Test";
import ValidarResult from "./pages/ValidarResult"
import ReactDOM from "react-dom";
import { BrowserRouter, Route } from "react-router-dom";

ReactDOM.render(
  <BrowserRouter>
    <div>
      <Route exact path="/" component={Login}/>
      <Route path="/Home" component={HomeUR}/>
      <Route path="/Login" component ={Login}/>
      <Route path="/Test" component={TestUR}/>
      <Route path ="/Result" component={Result}/>
      <Route path="/Profile" component={Profile}/>
      <Route path="/HomeUA" component={HomeUA} />
      <Route path = "/ValidarR" component={ValidarResult}/>
    </div>
  </BrowserRouter>,
  document.getElementById("root")
);
