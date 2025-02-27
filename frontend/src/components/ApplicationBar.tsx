import * as React from 'react';
import { useNavigate } from 'react-router-dom';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid2';
import Container from "@mui/material/Container";
import config from "../config.d/config.yaml";

let pages = []

for (let key in config.routes) {
      pages.push(config.routes[key]);
}

const ApplicationBar = () => {
    const navigate = useNavigate();

    function Navigation(page: string) {
        const new_page = "/" + page;
        navigate(new_page);
    }

  return (
      <Container sx={{
          alignItems: 'center',
          width: "80%",
          padding: "10px"
        }}>
          <Grid container spacing={2} style={{justifyContent: "center"}} size={{md: 10, lg: 8, xl: 6}}>
                  <AppBar position="static" style={{backgroundColor: 'grey'}}>
                    <Toolbar>
                      <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' } }}>
                        {pages.map((page) => (
                          <Button
                            key={page}
                            sx={{ my: 2, color: 'white', display: 'block', fontSize: {
                                sm: '1.5rem',
                                md: '1.25rem',
                                lg: '0.9rem'
                              }
                            }}
                            onClick={() => {
                                Navigation(page);
                            }}
                          >
                            {page}
                          </Button>
                        ))}
                      </Box>
                    </Toolbar>
                  </AppBar>
          </Grid>
          </Container>
  );
};

export default ApplicationBar;
