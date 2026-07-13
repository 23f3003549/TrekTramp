<template>

    <div class="card shadow-sm">

        <div class="card-header bg-success text-white">

            Payment Status

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

    name:"PaymentPieChart",

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

                    "Paid",

                    "Pending",

                    "Refunded"

                ],

                datasets:[

                    {

                        data:[

                            this.statistics.paid,

                            this.statistics.pending,

                            this.statistics.refunded

                        ],

                        backgroundColor:[

                            "#198754",

                            "#ffc107",

                            "#0dcaf0"

                        ],

                        borderColor:[

                            "#ffffff",

                            "#ffffff",

                            "#ffffff"

                        ],

                        borderWidth:2

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

                        position:"bottom",

                        labels:{

                            padding:20,

                            font:{

                                size:13

                            }

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

    height:350px;

}

</style>