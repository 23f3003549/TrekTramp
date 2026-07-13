<template>

    <div class="card shadow-sm">

        <div class="card-header bg-success text-white">

            Staff Performance

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

    name:"StaffChart",

    components:{

        Bar

    },

    props:{

        staffStatistics:{

            type:Array,

            required:true

        }

    },

    computed:{

        chartData(){

            return{

                labels:this.staffStatistics.map(

                    staff=>staff.name

                ),

                datasets:[

                    {

                        label:"Completed Treks",

                        data:this.staffStatistics.map(

                            staff=>staff.completed

                        ),

                        backgroundColor:"#0d6efd",

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