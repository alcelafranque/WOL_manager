import {Device} from "../types";
import React, {useState, ChangeEvent} from "react";
import {TextField} from "@mui/material";
import Grid from '@mui/material/Grid2';


interface FieldEntryProps {
    title: string;
    inputData: string;
    setInputData: React.Dispatch<React.SetStateAction<string>>;
}


const FieldEntry: React.FC<FieldEntryProps> = ({inputData, setInputData, title}) => {
    const handleInput = (event: React.ChangeEvent<HTMLInputElement>) => {
        setInputData(event.target.value);
    };

    return (
        <>
            <Grid size={4} sx={{
                display: 'flex',
                alignContent: 'center',
                alignItems: 'center',
                justifyContent: 'center'
            }}>
                {title}:
            </Grid>
            <Grid size={8} >
                <TextField value={inputData} onChange={handleInput}/>
            </Grid>
        </>
    )
}



interface DeviceRegisterProps {
    setDevices: React.Dispatch<React.SetStateAction<Array<Device>>>;
}

export const DeviceRegister: React.FC<DeviceRegisterProps> = ({setDevices}) => {
  const [hostname, setHostname] = useState<string>("");
  const [mac, setMac] = useState<string>("");
  const [deviceInterface, setDeviceInterface] = useState<string>("");

    return (
        <div style={{
            padding: '10px'
        }}>
            Register device
            <Grid container sx={{
                border: '1px solid',
                padding: '10px'
            }}>
                <FieldEntry inputData={hostname} setInputData={setHostname} title={"Hostname"}/>
                <FieldEntry inputData={mac} setInputData={setMac} title={"Mac"}/>
                <FieldEntry inputData={deviceInterface} setInputData={setDeviceInterface} title={"Interface"}/>
            </Grid>
        </div>
    );
}
