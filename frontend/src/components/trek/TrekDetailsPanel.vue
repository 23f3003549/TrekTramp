<template>

<div
    class="offcanvas offcanvas-end"
    tabindex="-1"
    ref="offcanvasElement"
>

    <div class="offcanvas-header bg-success text-white">

        <h4 class="offcanvas-title">

            Trek Details

        </h4>

        <button
            class="btn-close btn-close-white"
            @click="closePanel"
        ></button>

    </div>

    <div class="offcanvas-body">

        <div
            v-if="loading"
            class="text-center py-5"
        >

            <div class="spinner-border text-success"></div>

        </div>

        <div v-else-if="trek">

            <!-- BASIC INFORMATION -->

            <div class="card shadow-sm mb-4">

                <div class="card-header bg-success text-white">

                    Basic Information

                </div>

                <div class="card-body">

                    <div class="row">

                        <div class="col-md-6">

                            <p><strong>Trek Name :</strong> {{ trek.trek_name }}</p>

                            <p><strong>Location :</strong> {{ trek.location }}</p>

                            <p><strong>Difficulty :</strong> {{ trek.difficulty }}</p>

                            <p><strong>Price :</strong> ₹ {{ trek.price }}</p>

                        </div>

                        <div class="col-md-6">

                            <p>

                                <strong>Status :</strong>

                                <span
                                    class="badge"
                                    :class="statusBadge"
                                >
                                    {{ trek.status }}
                                </span>

                            </p>

                            <p>

                                <strong>Duration :</strong>

                                {{ trek.duration_days }} Days

                            </p>

                            <p>

                                <strong>Age Limit :</strong>

                                {{ trek.min_age }}

                                -

                                {{ trek.max_age }}

                                Years

                            </p>

                            <p>

                                <strong>Slots :</strong>

                                {{ trek.available_slots }}

                                /

                                {{ trek.max_slots }}

                            </p>

                        </div>

                    </div>

                    <hr>

                    <p>

                        <strong>Start Date :</strong>

                        {{ trek.start_date }}

                    </p>

                    <p>

                        <strong>End Date :</strong>

                        {{ trek.end_date }}

                    </p>

                </div>

            </div>

            <!-- DESCRIPTION -->

            <div class="card shadow-sm mb-4">

                <div class="card-header bg-success text-white">

                    Description

                </div>

                <div class="card-body">

                    {{ trek.description }}

                </div>

            </div>

            <!-- ASSIGNED STAFF -->

            <div class="card shadow-sm mb-4">

                <div class="card-header bg-success text-white">

                    Assigned Staff

                </div>

                <div class="card-body">

                    <div v-if="trek.staff_name">

                        <strong>{{ trek.staff_name }}</strong>

                    </div>

                    <div v-else>

                        No Staff Assigned

                    </div>

                </div>

            </div>

            <!-- BOOKING -->

            <div class="card shadow-sm mb-4">

                <div class="card-header bg-success text-white">

                    Booking Summary

                </div>

                <div class="card-body">

                    <p>

                        <strong>Total Slots :</strong>

                        {{ trek.max_slots }}

                    </p>

                    <p>

                        <strong>Available Slots :</strong>

                        {{ trek.available_slots }}

                    </p>

                </div>

            </div>

            <!-- ACTION -->

            <div class="card shadow-sm">

                <div class="card-header bg-success text-white">

                    Actions

                </div>

                <div class="card-body">

                    <div
                        v-if="role==='admin'"
                    >

                        <button
                            class="btn btn-success"
                            @click="assignStaff"
                        >

                            Assign Staff

                        </button>

                    </div>

                    <div
                        v-else-if="role==='staff'"
                    >

                        <button
                            class="btn btn-primary me-2"
                        >

                            Start Trek

                        </button>

                        <button
                            class="btn btn-success me-2"
                        >

                            Complete Trek

                        </button>

                        <button
                            class="btn btn-danger"
                        >

                            Cancel Trek

                        </button>

                    </div>

                    <div
                        v-else
                    >

                        <button
                            class="btn btn-success"
                        >

                            Book Trek

                        </button>

                    </div>

                </div>

            </div>

        </div>

    </div>

</div>

</template>

<script>

import * as bootstrap from "bootstrap";
import { getTrek } from "../../services/trek";

export default{

    name:"TrekDetailsPanel",

    props:{

        trekId:Number

    },

    emits:["close"],

    data(){

        return{

            trek:null,

            loading:true,

            offcanvas:null,

            role:localStorage.getItem("role")

        }

    },

    computed:{

        statusBadge(){

            return{

                "bg-success":this.trek.status==="open",

                "bg-warning text-dark":this.trek.status==="pending",

                "bg-danger":this.trek.status==="cancelled",

                "bg-secondary":this.trek.status==="completed"

            }

        }

    },

    methods:{

        async loadTrek(){

            try{

                const response=await getTrek(this.trekId);

                this.trek=response.data.trek;

            }

            catch(error){

                console.error(error);

                alert("Unable to load trek.");

            }

            finally{

                this.loading=false;

            }

        },

        closePanel(){

            this.offcanvas.hide();

        },

        assignStaff(){

            alert("Assign Staff Modal");

        }

    },

    async mounted(){

        await this.loadTrek();

        this.offcanvas=new bootstrap.Offcanvas(this.$refs.offcanvasElement);

        this.offcanvas.show();

        this.$refs.offcanvasElement.addEventListener(

            "hidden.bs.offcanvas",

            ()=>{

                this.$emit("close");

            }

        );

    }

}

</script>

<style scoped>

.offcanvas{

    width:650px;

}

.card{

    border:none;

    border-radius:14px;

}

.card-header{

    font-weight:600;

}

.badge{

    font-size:.85rem;

    padding:8px 14px;

}

.btn{

    border-radius:10px;

}

.offcanvas-body{

    background:#f8f9fa;

}

</style>