import {Device} from "../types";
import React from "react";
import {Box, TextField, Typography} from "@mui/material";
import Grid from '@mui/material/Grid2';
import {Button} from "@mui/material";

interface DeviceRegisterProps {
    setDevices: React.Dispatch<React.SetStateAction<Array<Device>>>;
}

export const DeviceRegister: React.FC<DeviceRegisterProps> = ({setDevices}) => {
    const fields = ["Hostname", "Mac", "interface"]

    return (
        <div style={{
            padding: '10px'
        }}>
            Register device
            <Grid container sx={{
                border: '1px solid'
            }}>
                {fields.map(field => (
                    <>
                        <Grid size={4} sx={{
                            display: 'flex',
                            alignContent: 'center',
                            alignItems: 'center',
                            justifyContent: 'center'
                        }}>
                            {field}:
                        </Grid>
                        <Grid size={8}>
                            <TextField sx={{
                            }}/>
                        </Grid>
                    </>
                ))}

            </Grid>
        </div>
    );
}