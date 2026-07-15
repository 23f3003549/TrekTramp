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

   

        <div
            v-else-if="trek"
        >

     
            <div class="card shadow-sm mb-4">

                <div class="card-header bg-success text-white">

                    Basic Information

                </div>

                <div class="card-body">

                    <div class="row">

                        <div class="col-md-6">

                            <p>

                                <strong>Trek Name :</strong>

                                {{ trek.trek_name }}

                            </p>

                            <p>

                                <strong>Location :</strong>

                                {{ trek.location }}

                            </p>

                            <p>

                                <strong>Difficulty :</strong>

                                {{ trek.difficulty }}

                            </p>

                            <p>

                                <strong>Price :</strong>

                                ₹ {{ trek.price }}

                            </p>

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


            <div class="card shadow-sm mb-4">

                <div class="card-header bg-success text-white">

                    Description

                </div>

                <div class="card-body">

                    {{ trek.description }}

                </div>

            </div>

            <div class="card shadow-sm mb-4">

                <div class="card-header bg-success text-white">

                    Assigned Staff

                </div>

                <div class="card-body">

                    <template
                        v-if="trek.assigned_staff"
                    >

                        <h6>

                            {{ trek.assigned_staff.name }}

                        </h6>

                        <p class="mb-1">

                            {{ trek.assigned_staff.email }}

                        </p>

                        <small class="text-muted">

                            {{ trek.assigned_staff.phone }}

                        </small>

                    </template>

                    <template
                        v-else
                    >

                        <p class="text-muted mb-0">

                            No staff assigned.

                        </p>

                    </template>

                </div>

            </div>

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

                        <strong>Booked Participants :</strong>

                        {{ trek.max_slots - trek.available_slots }}

                    </p>

                    <p>

                        <strong>Available Slots :</strong>

                        {{ trek.available_slots }}

                    </p>

                </div>

            </div>


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
                            @click="openAssignPanel"
                        >

                            {{ trek.assigned_staff ? "Change Staff" : "Assign Staff" }}

                        </button>

                    </div>

                    <div
                        v-else-if="role==='staff'"
                    >

                        <div
                            v-if="trek.status==='open'"
                        >

                            <label class="form-label">

                                Maximum Capacity

                            </label>

                            <div class="input-group mb-3">

                                <input

                                    type="number"

                                    class="form-control"

                                    v-model="updatedCapacity"

                                    min="1"

                                >

                                <button

                                    class="btn btn-warning"

                                    @click="updateCapacity"

                                >

                                    Update Capacity

                                </button>

                            </div>

                            <hr>

                            <button

                                class="btn btn-primary"

                                @click="changeStatus('started')"

                            >

                                Start Trek

                            </button>

                            <button

                                class="btn btn-danger ms-2"

                                @click="changeStatus('cancelled')"

                            >

                                Cancel Trek

                            </button>

                        </div>

                        <div
                            v-else-if="trek.status==='started'"
                        >

                            <button

                                class="btn btn-success"

                                @click="changeStatus('completed')"

                            >

                                Complete Trek

                            </button>

                            <button

                                class="btn btn-danger ms-2"

                                @click="changeStatus('cancelled')"

                            >

                                Cancel Trek

                            </button>

                        </div>

                        <div
                            v-else
                        >

                            <div class="alert alert-secondary mb-0">

                                This trek is

                                <strong>

                                    {{ trek.status }}

                                </strong>

                                .

                                No further actions are available.

                            </div>

                        </div>

                    </div>

                    <div
                        v-else
                    >

                        <button
                            class="btn btn-success"
                            @click="bookCurrentTrek"
                            :disabled="trek.available_slots===0 || trek.status!== 'open'"
                        >

                            {{ trek.available_slots===0? "Fully Booked" : "Book Trek" }}

                        </button>

                    </div>

                </div>

            </div>

        </div>

    </div>

</div>

<AssignStaffPanel

    v-if="showAssignPanel"

    :trekId="trek.id"

    @close="showAssignPanel=false"

    @assigned="handleStaffAssigned"

/>

</template>

<script>

import * as bootstrap from "bootstrap";

import { getTrek } from "../../services/trek";
import { bookTrek } from "../../services/trekker";

import {

    updateTrekCapacity,

    updateTrekStatus

} from "../../services/staff";

import AssignStaffPanel from "../admin/AssignStaffPanel.vue";

export default{

    name:"TrekDetailsPanel",

    components:{

        AssignStaffPanel

    },

    props:{

        trekId:Number

    },

    emits:["close","refresh"],

    data(){

        return{

            trek:null,

            loading:true,

            offcanvas:null,

            role:localStorage.getItem("role"),

            showAssignPanel:false,

            updatedCapacity:0

        }

    },

    computed:{

        statusBadge(){

            if(!this.trek){

                return {};

            }

            return{

                "bg-success":this.trek.status==="open",

                "bg-primary":this.trek.status==="started",

                "bg-secondary":this.trek.status==="completed",

                "bg-danger":this.trek.status==="cancelled"

            }

        }

    },

    methods:{

        async loadTrek(){

            this.loading=true;

            try{

                const response=await getTrek(this.trekId);

                this.trek=response.data.trek;

                this.updatedCapacity=this.trek.max_slots;

            }

            catch(error){

                console.error(error);

                alert(

                    error.response?.data?.message ||

                    "Unable to load trek."

                );

            }

            finally{

                this.loading=false;

            }

        },

        async bookCurrentTrek(){

            try{
        
                const response = await bookTrek(
        
                    this.trek.id
        
                );
        
                alert(
        
                    response.data.message
        
                );
        
                await this.loadTrek();
                window.dispatchEvent(
                    new CustomEvent("trek-updated")
                );
        
                this.$emit("refresh");
        
            }
        
            catch(error){

                const message = error.response?.data?.message;
            
                if(message==="Please complete your profile before booking."){
            
                    const openProfile = confirm(
                       "Please complete your profile before booking.\n\nOpen your profile now?"
                    );

                    if(openProfile){
                        this.$emit("close")
                        setTimeout(()=>{
                            window.dispatchEvent(

                            new CustomEvent(
                        
                                "open-profile",
                        
                                {
                        
                                    detail:{
                        
                                        trekId:this.trek.id
                        
                                    }
                        
                                }
                        
                            )
                        
                        );

                        },200);
                                                
                        
                    }

                    return;
            
                }
            
                alert(message || "Unable to book trek.");
                                        
            }
        },    
            
        closePanel(){

            this.offcanvas.hide();

        },

        openAssignPanel(){

            this.showAssignPanel=true;

        },

        async handleStaffAssigned(){

            this.showAssignPanel=false;

            await this.loadTrek();

        },

        async updateCapacity(){

            if(this.updatedCapacity<0){

                alert("Capacity cannot be negative.");

                return;

            }

            try{

                await updateTrekCapacity(

                    this.trek.id,

                    {

                        max_slots:this.updatedCapacity

                    }

                );

                alert("Slots updated successfully.");

                await this.loadTrek();

            }

            catch(error){

                console.error(error);

                alert(

                    error.response?.data?.message ||

                    "Unable to update slots."

                );

            }

        },

        async changeStatus(status){

            if(

                !confirm(

                    `Are you sure you want to mark this trek as ${status}?`

                )

            ){

                return;

            }

            try{

                await updateTrekStatus(

                    this.trek.id,

                    {

                        status:status

                    }

                );

                alert("Trek status updated.");

                await this.loadTrek();

            }

            catch(error){

                console.error(error);

                alert(

                    error.response?.data?.message ||

                    "Unable to update trek status."

                );

            }

        }

    },

    async mounted(){

        await this.loadTrek();

        this.offcanvas=new bootstrap.Offcanvas(

            this.$refs.offcanvasElement

        );

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

</style><style scoped>

.offcanvas{

    width:650px;

    background:#f8f9fa;

}

.offcanvas-header{

    border-bottom:none;

}

.card{

    border:none;

    border-radius:14px;

    overflow:hidden;

}

.card-header{

    font-weight:600;

    font-size:1rem;

}

.badge{

    padding:8px 14px;

    font-size:.85rem;

    border-radius:20px;

}

.btn{

    border-radius:10px;

}

.btn-primary,
.btn-success,
.btn-danger,
.btn-warning{

    min-width:140px;

}

.form-label{

    font-weight:600;

}

.form-control{

    border-radius:10px;

}

.input-group .btn{

    border-top-left-radius:0;

    border-bottom-left-radius:0;

}

.input-group .form-control{

    border-top-right-radius:0;

    border-bottom-right-radius:0;

}

.alert{

    border-radius:12px;

    font-size:.95rem;

}

.card-body p{

    margin-bottom:.6rem;

}

.card-body strong{

    color:#198754;

}

h6{

    margin-bottom:.25rem;

    font-weight:600;

}

small{

    font-size:.85rem;

}

.spinner-border{

    width:3rem;

    height:3rem;

}

</style>