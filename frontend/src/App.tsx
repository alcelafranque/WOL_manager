import { BrowserRouter, Routes, Route, Navigate} from 'react-router-dom';
import Box from '@mui/material/Box'
import ApplicationBar from './components/ApplicationBar';

import config from './config.d/config.yaml';
import {Devices} from "./components/Devices";

interface RouteCreatorInterface {
    name: string;
    url: string;
}

const RouteCreator: React.FC<RouteCreatorInterface> = ({name, url}) => {
    if (name == config.routes.devices) {
        return (
            <Box sx={{
                height: "100vh",
            }}>
                <ApplicationBar/>
                <Devices />
            </Box>
        )

    }
    return (
        <Box sx={{
                height: "100vh",
              }}>
            <ApplicationBar/>
        </Box>)
}

const App = () => {
  let routes: string[] = [];
  const url: string = config.backend_url;
  for (let key in config.routes) {
      routes.push(config.routes[key]);
  }

  return (
    <BrowserRouter>
      <Routes>
          {routes.map((route) => (
                <Route key={route} path={route} element={<RouteCreator name={route} url={url} />}/>
              ))
          }
          <Route path="/" element={<Navigate to={config.routes.devices} />} />
        <Route path="*" element={<Navigate to="/" replace={true} />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;