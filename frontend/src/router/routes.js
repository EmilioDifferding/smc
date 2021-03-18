
import Dashboard from '../views/Dashboard'
import DeviceIndex from '../views/Devices/DeviceIndex'
import DeviceList from '../views/Devices/DeviceList'
import DeviceCreate from '../views/Devices/DeviceCreate'
import DeviceEdit from '../views/Devices/DeviceEdit'
import DataList from '../views/Devices/DataList'
import PlacesIndex from '../views/Places/PlacesIndex'
import PlacesList from '../views/Places/PlacesList'
import PlacesCreate from '../views/Places/PlacesCreate'
import PlacesEdit from '../views/Places/PlacesEdit'
import UnitsIndex from '../views/Units/UnitsIndex'
import UnitsList from '../views/Units/UnitsList'
import UnitsCreate from '../views/Units/UnitsCreate'
import UnitsEdit from '../views/Units/UnitsEdit'


export default [
    {
        path: '/',
        name: 'Home',
        component: Dashboard,
        children: [

            {
                path: '/about',
                name: 'About',
                // route level code-splitting
                // this generates a separate chunk (about.[hash].js) for this route
                // which is lazy-loaded when the route is visited.
                component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
            },
            {
                path: '/dispositivos',
                title: 'Dispositivos',
                component: DeviceIndex,
                children: [
                    {
                        path: '',
                        name: 'devices',
                        component: DeviceList
                    },
                    {
                        path: 'crear',
                        name: 'create',
                        component: DeviceCreate
                    },
                    {
                        path: ':id/editar',
                        name: 'device.edit',
                        component: DeviceEdit
                    },
                    {
                        path:':id/data',
                        name:'device.data',
                        component:DataList
                    }
                ]
            },
            {
                path: '/lugares',
                component: PlacesIndex,
                children: [
                    {
                        path: '',
                        name: 'places',
                        component: PlacesList
                    },
                    {
                        path: 'crear',
                        name: 'places.create',
                        component: PlacesCreate
                    },
                    {
                        path: ':id/editar',
                        name: 'places.edit',
                        component: PlacesEdit,
                    }
                ]
            },
            {
                path: '/units',
                title: "Units",
                component: UnitsIndex,
                children: [
                    {
                        path: '',
                        name: 'units',
                        component: UnitsList
                    },
                    {
                        path: 'crear',
                        name: 'units.create',
                        component: UnitsCreate,
                    },
                    {
                        path: ':id/editar',
                        name: 'units.edit',
                        component: UnitsEdit
                    }
                ]
            }
        ]
    },
]