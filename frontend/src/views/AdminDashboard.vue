<template>

    <MainLayout>

        <div class="container py-4">

            <h2>Dashboard</h2>

        </div>
        <div class="row">
            <div class="col-md-3">
                <DashboardCards
                   title="Total Treks"
                   :count="dashboard.total_treks"
                />

            </div>
            <div class="col-md-3">
                <DashboardCards
                   title="Total User"
                   :count="dashboard.total_users"
                />

            </div>
            <div class="col-md-3">
                <DashboardCards
                   title="Total Staff"
                   :count="dashboard.total_staff"
                />

            </div>
            <div class="col-md-3">
                <DashboardCards
                   title="Total Bookings"
                   :count="dashboard.total_bookings"
                />

            </div>
        </div>
        
    </MainLayout>

</template>

<script>
import MainLayout from '../layouts/MainLayout.vue';
import DashboardCards from '../components/admin/DashboardCards.vue';

import { getDashboardStats } from '../services/admin.js';

export default{
    name: "AdminDashboard",
    components : {
        MainLayout,
        DashboardCards
    },
    data(){
        return {
            dashboard :{
                total_treks: 0,
                total_users: 0,
                total_staff: 0,
                total_bookings: 0,
            }
        }
    },
    methods:{

    },
    async mounted(){
        try{
            const response = await getDashboardStats();
            console.log(response.data);
            this.dashboard = response.data;

        }
        catch(error){
            console.log("Unable to fetch the stats", error);
        }

    }

}

</script>

<style>

</style>