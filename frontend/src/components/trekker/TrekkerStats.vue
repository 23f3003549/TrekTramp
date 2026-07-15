<template>

<div class="row g-4">


    <div class="col-md-4">

        <div class="card stat-card shadow-sm">

            <div class="card-body">

                <div class="icon bg-success">

                    <i class="bi bi-calendar-check"></i>

                </div>

                <h6 class="text-muted mt-3">

                    Upcoming Bookings

                </h6>

                <h2>

                    {{ statistics.upcoming_bookings }}

                </h2>

            </div>

        </div>

    </div>

    <div class="col-md-4">

        <div class="card stat-card shadow-sm">

            <div class="card-body">

                <div class="icon bg-primary">

                    <i class="bi bi-flag-fill"></i>

                </div>

                <h6 class="text-muted mt-3">

                    Completed Treks

                </h6>

                <h2>

                    {{ statistics.completed_treks }}

                </h2>

            </div>

        </div>

    </div>

    <div class="col-md-4">

        <div class="card stat-card shadow-sm">

            <div class="card-body">

                <div class="icon bg-warning">

                    <i class="bi bi-star-fill"></i>

                </div>

                <h6 class="text-muted mt-3">

                    Reviews Given

                </h6>

                <h2>

                    {{ statistics.reviews_given }}

                </h2>

            </div>

        </div>

    </div>

</div>

</template>

<script>

import {

    getDashboardStatistics

} from "../../services/trekker";

export default{

    name:"TrekkerStats",

    data(){

        return{

            statistics:{

                upcoming_bookings:0,

                completed_treks:0,

                reviews_given:0

            }

        }

    },

    methods:{

        async loadStatistics(){

            try{

                const response = await getDashboardStatistics();

                this.statistics = response.data.statistics;

            }

            catch(error){

                console.error(error);

            }

        }

    },

    mounted(){

        this.loadStatistics();

    }

}

</script>

<style scoped>

.stat-card{

    border:none;

    border-radius:18px;

    transition:0.3s;

    cursor:pointer;

}

.stat-card:hover{

    transform:translateY(-6px);

}

.icon{

    width:60px;

    height:60px;

    border-radius:50%;

    display:flex;

    justify-content:center;

    align-items:center;

    color:white;

    font-size:24px;

}

h2{

    font-weight:700;

    margin-top:8px;

}

</style>