//imports diferents apis known as repositories
import devicesApi from './apis/devices'
import placesApi from './apis/places'
import unitsApi from './apis/units'
import usersApi from './apis/users'
const repositories = {
    devices: devicesApi,
    places: placesApi,
    units: unitsApi,
    users: usersApi
};

export const apiFactory = {
    get: name => repositories[name],
}