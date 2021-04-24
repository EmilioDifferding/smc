
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
import UsersIndex from '../views/Users/UsersIndex'
import UsersList from '../views/Users/UsersList'
import UsersCreate from '../views/Users/UsersCreate'
import UsersEdit from '../views/Users/UsersEdit'
import Login from '../views/Login'

import store from '@/store'

export default [
    {   
        
        path: '/',
        name: 'dashboard',
        component: Dashboard,
        children: [
            {
                path: '/usuarios',
                title: 'Usuarios',
                component: UsersIndex,
                meta:{
                    requiresAuth: true
                },
                children:[
                    {
                        path:'',
                        name:'users',
                        component: UsersList
                    },
                    {
                        path: 'crear',
                        name: 'users.create',
                        component: UsersCreate
                    },
                    {
                        path: ':id/editar',
                        name: 'users.edit',
                        component: UsersEdit
                    }
                ]
            },
            {
                path: '/dispositivos',
                title: 'Dispositivos',
                component: DeviceIndex,
                meta:{
                    requiresAuth: true
                },
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
                meta:{
                    requiresAuth: true
                },
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
                meta:{
                    requiresAuth: true
                },
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
    {
        path: '/login',
        name: 'Login',
        component: Login
    },
]