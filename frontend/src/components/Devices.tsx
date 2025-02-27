import React, {useEffect} from "react";
import {send_request} from "../utils/requests";
import config from "../config.d/config.yaml";


interface DevicesProps {

}

export const Devices: React.FC<DevicesProps> = () => {

    const get_devices = async () => {
        const response = await send_request(config.backend_url, "devices", {});
        console.log(await response.json());
    }

    useEffect(() => {

        get_devices();
    }, [])

    return (
        <>
        </>
    )
}