import axios from 'axios'

const baseDomain = "http://backend:5000";
const baseURL = `${baseDomain}/api/`;
const APIHandler = axios.create({
    baseURL,
    timeout: 10000,
});

export default APIHandler;