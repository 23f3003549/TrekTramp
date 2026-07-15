<template>

<div class="row g-4" style="place-items: center; padding-top: 13%;">


    <div class="col-lg-4 col-md-6" >

        <div class="card stat-card shadow-sm border-0">

            <div class="card-body">

                <div class="d-flex justify-content-between align-items-center">

                    <div>

                        <h6 class="text-muted fs-2">

                            Assigned Treks

                        </h6>

                        <h2 class="fw-bold" style="margin-top: 30px; font-size: 50px;">

                            {{ statistics.assigned_treks }}

                        </h2>

                    </div>

                    <div class="icon bg-primary">

                        <i class="bi bi-map-fill"></i>

                    </div>

                </div>

            </div>

        </div>

    </div>

    <div class="col-lg-4 col-md-6">

        <div class="card stat-card shadow-sm border-0">

            <div class="card-body">

                <div class="d-flex justify-content-between align-items-center">

                    <div>

                        <h6 class="text-muted fs-2">

                            Total Participants

                        </h6>

                        <h2 class="fw-bold " style="margin-top: 30px; font-size: 50px;">

                            {{ statistics.total_participants }}

                        </h2>

                    </div>

                    <div class="icon bg-success">

                        <i class="bi bi-people-fill"></i>

                    </div>

                </div>

            </div>

        </div>

    </div>

    <div class="col-lg-4 col-md-6" >

        <div class="card stat-card shadow-sm border-0">

            <div class="card-body">

                <div class="d-flex justify-content-between align-items-center">

                    <div>

                        <h6 class="text-muted fs-2">

                            Completed Treks

                        </h6>

                        <h2 class="fw-bold" style="margin-top: 30px; font-size: 50px;">

                            {{ statistics.completed_treks }}

                        </h2>

                    </div>

                    <div class="icon bg-warning">

                        <i class="bi bi-check-circle-fill"></i>

                    </div>

                </div>

            </div>

        </div>

    </div>

</div>

</template>

<script>

import {

    getDashboardStatistics

} from "../../services/staff";

export default{

    name:"DashboardCards",

    data(){

        return{

            statistics:{

                assigned_treks:0,

                total_participants:0,

                completed_treks:0

            }

        }

    },

    methods:{

        async loadStatistics(){

            try{

                const response=await getDashboardStatistics();
                console.log(response);
                this.statistics=response.data.statistics;

            }

            catch(error){

                console.error(error);

                alert("Unable to load dashboard statistics.");

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

    border-radius:18px;

    transition:.3s;

    cursor:pointer;
    height:40vh;
    


}

.stat-card:hover{

    transform:translateY(-6px);

    box-shadow:0 15px 25px rgba(0,0,0,.12);
    background-color: rgb(225, 246, 213);

}

.icon{

    width:150px;

    height:150px;

    border-radius:50%;

    display:flex;

    justify-content:center;

    align-items:center;

    color:white;

    font-size:28px;

}

.card-body{

    padding:30px;

}

</style>