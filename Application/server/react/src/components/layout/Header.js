import React, { Component, Fragment } from 'react';
import {AppBar, Toolbar, Typography, IconButton, Snackbar } from '@material-ui/core'
import { Menu, AccountCircle, Close } from '@material-ui/icons'

class Header extends Component {
    constructor(props) {
        super(props);

        this.state = {
            snackbarOpen: true
        }
    }

    styles = {
        navBar: {
            backgroundColor: "#313131",
            color: "#eceff1"
        },
        navMenu: {
            marginRight: 15,
            marginLeft: -10
        },
        navBrand: {
            flexGrow: 1
        }
    }

    onSnackbarClose = () => {
        this.setState({
            snackbarOpen: false
        });
    }

    render() {
        return (
            <Fragment>
                <AppBar position="static" style={this.styles.navBar}>
                    <Toolbar>
                        <IconButton color="inherit" style={this.styles.navMenu}>
                            <Menu />
                        </IconButton>
                        <Typography variant="h6" color="inherit" style={this.styles.navBrand}>
                            Мистерија.мк
                        </Typography>
                        <IconButton color="inherit">
                            <AccountCircle />
                        </IconButton>
                    </Toolbar>
                </AppBar>
                <Snackbar
                    anchorOrigin={{ vertical: 'bottom', horizontal: 'left' }}
                    open={this.state.snackbarOpen}
                    autoHideDuration={6000}
                    onClose={this.onSnackbarClose}
                    message={"Добредојдовте во развојната верзија на Мистерија.мк"}
                    action={[
                        <IconButton key="close" aria-label="Close" color="inherit" onClick={this.onSnackbarClose}>
                            <Close/>
                        </IconButton>
                    ]}
                />
            </Fragment>
        )
    }
}

export default Header;