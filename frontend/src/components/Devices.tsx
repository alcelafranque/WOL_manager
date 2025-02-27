import React, {useEffect, useState} from "react";
import {send_request} from "../utils/requests";
import config from "../config.d/config.yaml";
import Grid from '@mui/material/Grid2';

import {Device} from '../utils/types';

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
        <Grid padding={"10px"} container rowSpacing={1} sx={{
                    justifyContent: 'center',
                    alignItems: 'center',
                    alignContent: 'center'
                }}>
            {devices.map((device, index) => (
                <Grid size={4} key={index}>
                    {device.hostname}
                </Grid>
            ))}
        </Grid>
    )
}