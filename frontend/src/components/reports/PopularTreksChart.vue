<template>

    <div class="card shadow-sm">

        <div class="card-header bg-success text-white">

            Top 5 Most Popular Treks

        </div>

        <div class="card-body">

            <Bar

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

    BarElement

}from "chart.js";

import{

    Bar

}from "vue-chartjs";

ChartJS.register(

    Title,

    Tooltip,

    Legend,

    CategoryScale,

    LinearScale,

    BarElement

);

export default{

    name:"PopularTreksChart",

    components:{

        Bar

    },

    props:{

        treks:{

            type:Array,

            required:true

        }

    },

    computed:{

        chartData(){

            return{

                labels:this.treks.map(

                    trek=>trek.name

                ),

                datasets:[

                    {

                        label:"Bookings",

                        data:this.treks.map(

                            trek=>trek.bookings

                        ),

                        backgroundColor:"#198754",

                        borderRadius:8,

                        barThickness:24

                    }

                ]

            };

        },

        chartOptions(){

            return{

                responsive:true,

                maintainAspectRatio:false,

                indexAxis:"y",

                plugins:{

                    legend:{

                        display:false

                    },

                    title:{

                        display:false

                    }

                },

                scales:{

                    x:{

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