import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'

import AdminDashboard from '../views/AdminDashboard.vue'
import ManageTreks from '../views/ManageTreks.vue'
import ManageStaff from '../views/ManageStaff.vue'
import ManageUsers from '../views/ManageUsers.vue'
import ManageBookings from '../views/ManageBookings.vue'
import Reports from "../views/Reports.vue";

import CreateTrek from '../views/CreateTrek.vue'
import TrekDetails from '../views/TrekDetails.vue'
import CompleteProfile from '../views/staff/CompleteProfile.vue'

import StaffDashboard from '../views/staff/Dashboard.vue'
import StaffMyTreks from "../views/staff/MyTreks.vue";
import TrekkerDashboard from "../views/trekker/Dashboard.vue"
import BrowseTreks from "../views/trekker/BrowseTreks.vue";
// import TrekkerProfile from "../views/trekker/Profile.vue";
import TrekkerMyTreks from '../views/trekker/MyTreks.vue'
import StaffParticipants from '../views/staff/Participants.vue'

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
        path : '/admin/users',
        name : 'ManageUsers',
        component: ManageUsers
    },
    {
        path : '/admin/bookings',
        name : 'ManageBookings',
        component: ManageBookings
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
        name: "staff-my-Treks",
        component: StaffMyTreks
    },
    // {   path: "/staff/profile",
    //     name: "staff-profile",
    //     component : Profile

    // },
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
        path: "/trekker/my-treks",
        name: "trekker-my-treks",
        component: TrekkerMyTreks
    },
    {
        path: "/staff/participants",
    
        name: "StaffParticipants",
    
        component: StaffParticipants
    },
    {
        path: "/admin/reports",
    
        name: "Reports",
    
        component: Reports
    },




]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router