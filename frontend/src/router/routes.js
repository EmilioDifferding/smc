
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
        path: '/login',
        name: 'Login',
        component: Login
    },
    {   
        
        path: '/',
        name: 'dashboard',
        component: Dashboard,
        meta:{
            requiresAuth: true
        },
        children: [
            {
                path: '/usuarios',
                title: 'Usuarios',
                component: UsersIndex,
                meta:{
                    requiresAuth: true,
                    requiresPermissions:['administrador']
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
                        component: DeviceList,
                        meta:{
                            requiresPermissions: ['administrador', 'usuario']
                        }
                    },
                    {
                        path: 'crear',
                        name: 'devices.create',
                        component: DeviceCreate,
                        meta:{
                            requiresPermissions: ['administrador']
                        }
                    },
                    {
                        path: ':id/editar',
                        name: 'device.edit',
                        component: DeviceEdit,
                        meta:{
                            requiresPermissions: ['administrador']
                        }
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
                        component: PlacesList,
                        meta:{
                            requiresPermissions: ['administrador']
                        }
                    },
                    {
                        path: 'crear',
                        name: 'places.create',
                        component: PlacesCreate,
                        meta:{
                            requiresPermissions: ['administrador']
                        }
                    },
                    {
                        path: ':id/editar',
                        name: 'places.edit',
                        component: PlacesEdit,
                        meta:{
                            requiresPermissions: ['administrador']
                        }
                    }
                ]
            },
            {
                path: '/unidades',
                title: "Units",
                component: UnitsIndex,
                meta:{
                    requiresAuth: true
                },
                children: [
                    {
                        path: '',
                        name: 'units',
                        component: UnitsList,
                        meta:{
                            requiresPermissions: ['administrador']
                        }
                    },
                    {
                        path: 'crear',
                        name: 'units.create',
                        component: UnitsCreate,
                        meta:{
                            requiresPermissions: ['administrador']
                        }
                    },
                    {
                        path: ':id/editar',
                        name: 'units.edit',
                        component: UnitsEdit,
                        meta:{
                            requiresPermissions: ['administrador']
                        }
                    }
                ]
            }
        ]
    },
    
]