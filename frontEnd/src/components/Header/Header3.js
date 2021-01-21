/**  Header1 
 * Header1 Icon User y Icon Logout -- Vista HomeUR
 * Header2 Icon User y Icon Home --  Vista Test, Resultados
 * Header3 Icon Home y Icon Logout -- Vista UR Info, Vista ValidarResultados
 * Header4 Icon Logout -- Vista HomeUA
 * **/
import React from "react";
import AppBar from "@material-ui/core/AppBar";
import Grid from "@material-ui/core/Grid";
import atoms from "../atoms";
import { Link, BrowserRouter as Router, Route } from "react-router-dom";
import { withRouter } from "react-router";
import IconButton from "@material-ui/core/IconButton";
import HomeIcon from "@material-ui/icons/Home";
import PowerSettingsNew from "@material-ui/icons/PowerSettingsNew";

const { Divider, Toolbar, Icon } = atoms;

const logo = "https://m.media-amazon.com/images/S/abs-image-upload-na/1/AmazonStores/ATVPDKIKX0DER/26d289aae25c4d966ec95b641935935d.w288.h288.png";
const label = "/static/themes/instapaper/logo.png";

const handleLogout = () => {
  sessionStorage.clear();
  localStorage.clear();
};

const Header = () => (
  <AppBar position="sticky" color="default" elevation={0}>
    <Toolbar narrow>
      <Grid container>
        <Grid item xs>
          <Grid container alignItems="center">
            

            <Divider vertical />

            <b>Match Roommates</b>
          </Grid>
        </Grid>
        
        <Grid item md>
          <Grid container>
            {/* <Link to={`/Profile/${user.id}`} id="link"> <Link to="/Profile/1" id="link"> */}
            <Link to={"/HomeUA"} id="link">
              <IconButton >
                <HomeIcon />
              </IconButton>
            </Link>
            <Divider vertical />
            <Link to={"/"} id="link">
              <IconButton onClick={handleLogout}>
                <PowerSettingsNew />
              </IconButton>
            </Link>
          </Grid>
        </Grid>
      </Grid>
    </Toolbar>
  </AppBar>
);

export default withRouter(Header);
