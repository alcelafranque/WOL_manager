import {Device} from "../types";
import React from "react";
import {Box} from "@mui/material";
import {Button} from "@mui/material";

interface DeviceCardProps {
    device: Device;
}

export const DeviceCard: React.FC<DeviceCardProps> = ({device}) => {

    return (
        <Box>
            <div>
                {device.hostname}
            </div>
            <div>
                status: OFF
            </div>
            <Button sx={{backgroundColor: "pink", color: 'white'}}>
                Start
            </Button>
        </Box>
    )
}