export default interface Device {
    hostname: string;
    mac: string;
    ip?: string;
}

export interface Config {
    backend_url?: string,
    routes?: Array<Object>,
    backend_api_key?: string
}