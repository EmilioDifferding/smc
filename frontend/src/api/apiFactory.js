//imports diferents apis known as repositories
import devicesApi from './apis/devices'
import placesApi from './apis/places'
import unitsApi from './apis/units'
const repositories = {
    devices: devicesApi,
    places: placesApi,
    units: unitsApi,
};

export const apiFactory = {
    get: name => repositories[name],
}