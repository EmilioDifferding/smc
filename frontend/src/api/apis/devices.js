import api from '../api';

const resource = '/devices'

export default {
    get(params) {
        params = {
            'params': params,
        };
        // console.log(api.get('get-devices'))
        return api.get(`${resource}`, params);
    },
    create(data) {
        return api.post(`${resource}`, data);
    },
    find(id, params) {
        params = {
            'params': params,
        };
        return api.get(`${resource}/${id}`, params);
    },
    update(id, data) {
        if (data.constructor.name === "FormData")
            data.append('_method', 'put');
        if (data.constructor.name === "Object")
            data._method = 'put';
        return api.put(`${resource}/${id}`, data);
    },
    delete(id) {
        return api.delete(`${resource}/${id}`);
    },
    getData(id, params) {
        params = {
            'params': params,
        };
        return api.get(`${resource}/${id}/data`, params)
    },
}