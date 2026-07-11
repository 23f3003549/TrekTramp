import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import ManageTreks from '../views/ManageTreks.vue'
import CreateTrek from '../views/CreateTrek.vue'
import TrekDetails from '../views/TrekDetails.vue'
import ManageStaff from '../views/ManageStaff.vue'
import CompleteProfile from '../views/staff/CompleteProfile.vue'
import StaffDashboard from '../views/staff/Dashboard.vue'
import MyTreks from "../views/staff/MyTreks.vue";
import TrekkerDashboard from "../views/trekker/Dashboard.vue"
import BrowseTreks from "../views/trekker/BrowseTreks.vue";
import MyBookings from "../views/trekker/MyBookings.vue";
import History from "../views/trekker/History.vue";
import TrekkerProfile from "../views/trekker/Profile.vue";

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
        component: TrekDetails
    },
    {
        path : '/admin/staff',
        name : 'ManageStaff',
        component: ManageStaff
    },
    {
        path: "/staff/complete-profile",
        name: "CompleteProfile",
        component: CompleteProfile
    },
    {
        path:"/staff/dashboard",
        name:"StaffDashboard",
        component:StaffDashboard
    },
    {
        path: "/staff/my-treks",
        name: "MyTreks",
        component: MyTreks
    },
    {
        path: "/trekker/dashboard",
        name: "trekker-dashboard",
        component: TrekkerDashboard
    },
    {
        path: "/trekker/browse",
        name: "browse-treks",
        component: BrowseTreks
    },
    {
        path: "/trekker/bookings",
        name: "my-bookings",
        component: MyBookings
    },
    {
        path: "/trekker/history",
        name: "trekker-history",
        component: History
    },
    {
        path: "/trekker/profile",
        name: "trekker-profile",
        component: TrekkerProfile
    },




]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router