<template>

    <div class="card shadow-sm">

        <div class="card-header bg-success text-white">

            Monthly Booking Trend

        </div>

        <div class="card-body">

            <Line

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

    CategoryScale,

    LinearScale,

    PointElement,

    LineElement,

    Filler

}from "chart.js";

import{

    Line

}from "vue-chartjs";

ChartJS.register(

    Title,

    Tooltip,

    Legend,

    CategoryScale,

    LinearScale,

    PointElement,

    LineElement,

    Filler

);

export default{

    name:"MonthlyBookingChart",

    components:{

        Line

    },

    props:{

        monthlyBookings:{

            type:Array,

            required:true

        }

    },

    computed:{

        chartData(){

            return{

                labels:this.monthlyBookings.map(

                    month=>month.month

                ),

                datasets:[

                    {

                        label:"Bookings",

                        data:this.monthlyBookings.map(

                            month=>month.count

                        ),

                        borderColor:"#198754",

                        backgroundColor:"rgba(25,135,84,0.2)",

                        fill:true,

                        tension:0.4,

                        pointRadius:5,

                        pointHoverRadius:7

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

                        display:false

                    }

                },

                scales:{

                    y:{

                        beginAtZero:true,

                        ticks:{

                            precision:0

                        }

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

    height:400px;

}

</style>