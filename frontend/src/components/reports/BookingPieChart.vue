<template>

    <div class="card shadow-sm">

        <div class="card-header bg-success text-white">

            Booking Status

        </div>

        <div class="card-body">

            <Pie

                :data="chartData"

                :options="chartOptions"

            />

        </div>

    </div>

</template>

<script>

import{

    Chart as ChartJS,

    Title,

    Tooltip,

    Legend,

    ArcElement

}from "chart.js";

import{

    Pie

}from "vue-chartjs";

ChartJS.register(

    Title,

    Tooltip,

    Legend,

    ArcElement

);

export default{

    name:"BookingPieChart",

    components:{

        Pie

    },

    props:{

        statistics:{

            type:Object,

            required:true

        }

    },

    computed:{

        chartData(){

            return{

                labels:[

                    "Booked",

                    "Completed",

                    "Cancelled"

                ],

                datasets:[

                    {

                        data:[

                            this.statistics.booked,

                            this.statistics.completed,

                            this.statistics.cancelled

                        ],

                        backgroundColor:[

                            "#198754",

                            "#0d6efd",

                            "#dc3545"

                        ],

                        borderWidth:1

                    }

                ]

            };

        },

        chartOptions(){

            return{

                responsive:true,

                maintainAspectRatio:false,

                plugins:{

                    legend:{

                        position:"bottom"

                    }

                }

            };

        }

    }

}

</script>

<style scoped>

.card{

    border:none;

    border-radius:14px;

}

.card-body{

    height:350px;

}

</style>