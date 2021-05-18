import api from '../api'

const resource = '/places';

export default {
    get(params){
        params = {
            'params': params,
        };
        return api.get(`${resource}`)
    },
    find (id, params) {
        params = {
            'params': params,
        };
        return api.get(`${resource}/${id}`, params);
    },
    create(data) {
        return api.post(`${resource}`, data)
    },
    update(id, data){
        if(data.constructor.name === 'FormData')
            data.append('_method', 'put');
        if(data.constructor.name === 'Object')
            data.method = 'put';
        return api.put(`${resource}/${id}`, data);
    },
    delete(id) {
        return api.delete(`${resource}/${id}`);
    },
}