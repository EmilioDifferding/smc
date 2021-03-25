import axios from 'axios';

// const API_URL = 'http://smc-fcal.duckdns.org/';
// const API_URL = 'http://localhost:5000/api/'
const API_URL = process.env.VUE_APP_API_URL
const client = axios.create({
    baseURL: API_URL,
});

client.defaults.headers.common['X-Requeted-With'] = 'XMLHttpRequest';

const configHandler = (config) => {
    return config;
};

const successHandler = (response) => {
    return response.data;
};

const errorHandler = (error) =>{
    console.error(error);
    let messageData = Object.create(null);
    messageData.title = 'Ocurrió un error en la solicitud';
    messageData.content = '';
    if(error.response){
        if(error.response.status === 401) {
            messageData.title = 'no autorizado';
        }
        if(error.response.status === 404) {
            messageData.title = 'dirección no encontrada!';
        }
        if(error.response.status === 422) {
            messageData.title = 'revisa los siguientes datos!';
            messageData.content = error.response.data.errors;
        }
    }  else if (error.request) {
        messageData.title = 'sin respuesta del servidor!';
    }
    return Promise.reject(messageData)
}

client.interceptors.request.use(
    config => configHandler(config),
    error => console.log(error)
);

client.interceptors.response.use(
    response => successHandler(response),
    error => errorHandler(error)
);

export default client;