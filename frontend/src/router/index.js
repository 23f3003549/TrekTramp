import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import ManageTreks from '../views/ManageTreks.vue'
import CreateTrek from '../views/CreateTrek.vue'
import TrekDetails from '../views/TrekDetails.vue'

const routes = [

    {
        path: '/',
        name: 'home',
        component: HomeView
    },

    {
        path: '/login',
        name: 'login',
        component: LoginView
    },

    {
        path: '/register',
        name: 'register',
        component: RegisterView
    },

    {
        path: '/admin',
        name: 'admin',
        component: AdminDashboard
    },
    {
        path: '/admin/treks',
        name: 'manage-treks',
        component: ManageTreks
    },
    {
        path: '/admin/treks/create',
        name: 'create-trek',
        component: CreateTrek
    },
    {
        path: '/admin/treks/:id',
        name: 'TrekDetails',
        component: 'TrekDetails'
    }



]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router