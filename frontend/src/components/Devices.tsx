import React, {useEffect, useState} from "react";
import {send_request} from "../utils/requests";
import config from "../config.d/config.yaml";
import Grid from '@mui/material/Grid2';

import {Device} from '../utils/types';
import {DeviceCard} from "../utils/Devices/DeviceCard";
import Container from "@mui/material/Container";

interface DevicesProps {

}

export const Devices: React.FC<DevicesProps> = () => {
    const [devices, setDevices] = useState<Array<Device>>([]);

    const get_devices = async () => {
        const response = await send_request(config.backend_url, "devices", {});
        const json_response = await response.json();
        console.log(json_response);

        if ("devices" in json_response)
        {
            setDevices(json_response["devices"]);
        }
    }

    useEffect(() => {

        get_devices();
    }, [])

    return (
        <Container sx={{
          alignItems: 'center',
          width: "80%",
          padding: "10px",
          justifyContent: 'center',
          display: "flex"
        }}>
            <Grid padding={"10px"} container spacing={1} sx={{
                width: '90%',
                border: "1px solid",
            }}>
                {devices.map((device, index) => (
                    <Grid size={4} key={index} border={"1px solid"} spacing={1} sx={{
                        display: "flex",
                        justifyContent: 'center'
                    }}>
                        <DeviceCard device={device}></DeviceCard>
                    </Grid>
                ))}
            </Grid>
        </Container>
    )
}