<template>

<div

    class="offcanvas offcanvas-end"

    tabindex="-1"

    ref="offcanvasElement"

>


    <div class="offcanvas-header">

        <div>

            <h4 class="mb-1">

                Participant Details

            </h4>

            <small class="text-muted">

                Manage Booking

            </small>

        </div>

        <button

            class="btn-close"

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

        <div v-else>

            <div class="card shadow-sm mb-4">

                <div class="card-header bg-success text-white">

                    Personal Information

                </div>

                <div class="card-body">

                    <div class="row mb-3">

                        <div class="col-md-6">

                            <label>Name</label>

                            <input

                                class="form-control"

                                :value="participant.name"

                                disabled

                            >

                        </div>

                        <div class="col-md-6">

                            <label>Email</label>

                            <input

                                class="form-control"

                                :value="participant.email"

                                disabled

                            >

                        </div>

                    </div>

                    <div class="row mb-3">

                        <div class="col-md-6">

                            <label>Phone</label>

                            <input

                                class="form-control"

                                :value="participant.phone"

                                disabled

                            >

                        </div>

                        <div class="col-md-6">

                            <label>Gender</label>

                            <input

                                class="form-control"

                                :value="participant.gender"

                                disabled

                            >

                        </div>

                    </div>

                    <div>

                        <label>Age</label>

                        <input

                            class="form-control"

                            :value="participant.age"

                            disabled

                        >

                    </div>

                </div>

            </div>

            <div class="card shadow-sm mb-4">

                <div class="card-header bg-primary text-white">

                    Booking Information

                </div>

                <div class="card-body">

                    <div class="row mb-3">

                        <div class="col-md-6">

                            <label>Trek</label>

                            <input

                                class="form-control"

                                :value="participant.trek_name"

                                disabled

                            >

                        </div>

                        <div class="col-md-6">

                            <label>Booking Date</label>

                            <input

                                class="form-control"

                                :value="participant.booking_date"

                                disabled

                            >

                        </div>

                    </div>

                    <div class="row">

                        <div class="col-md-6">

                            <label>Total Amount</label>

                            <input

                                class="form-control"

                                :value="'₹ '+participant.total_amount"

                                disabled

                            >

                        </div>

                    </div>

                </div>

            </div>

            <div class="card shadow-sm">

                <div class="card-header bg-warning">

                    Booking Actions

                </div>

                <div class="card-body">

                    <div class="mb-3">

                        <label>

                            Booking Status

                        </label>

                        <select

                            class="form-select"

                            v-model="form.booking_status"

                            :disabled="form.user_status === 'inactive' || participant.booking_status==='completed' || participant.booking_status==='cancelled'"
                        >

                            <option value="booked">

                                Booked

                            </option>

                            <option value="completed">

                                Completed

                            </option>

                            <option value="cancelled">

                                Cancelled

                            </option>

                        </select>

                    </div>
                    <div class="mb-3">

                        <label>
                    
                            Account Status
                    
                        </label>
                    
                        <select
                    
                            class="form-select"
                    
                            v-model="form.user_status"

                            :disabled="form.user_status === 'inactive' || participant.booking_status==='completed' || participant.booking_status==='cancelled'"
                    
                        >
                    
                            <option value="active">
                    
                                Active
                    
                            </option>
                    
                            <option value="inactive">
                    
                                Inactive
                    
                            </option>
                    
                        </select>

                    </div>

                    <div class="mb-3">

                        <label>

                            Payment Status

                        </label>
                        
                        <input

                            class="form-control"
                    
                            :value="participant.payment_status"
                    
                            :disabled="participant.booking_status==='completed' || participant.booking_status==='cancelled'"

                    </div>

                    <div class="mb-4" v-if="
                        participant.booking_status!=='completed' &&
                        participant.booking_status!=='cancelled'
                    ">

                        <label>

                            Reason

                        </label>

                        <textarea

                            rows="4"

                            class="form-control"

                            v-model="form.status_reason"

                            placeholder="Enter reason..."

                        ></textarea>

                    </div>

                    <button
                        v-if="
                            participant.booking_status!=='completed' &&
                            participant.booking_status!=='cancelled'
                        "                    


                        class="btn btn-success w-100"

                        @click="updateParticipant"

                        :disabled="saving"

                    >

                        {{ saving ? "Updating..." : "Update Details" }}

                    </button>

                    <div
                        v-if="
                            participant.booking_status==='completed' ||
                            participant.booking_status==='cancelled'
                        "
                        class="alert alert-secondary"

                    >

                        <i class="bi bi-lock-fill me-2"></i>
                    
                        This booking is closed. Participant details can only be viewed.

                    </div>

                </div>

            </div>

        </div>

    </div>

</div>

</template>

<script>

import * as bootstrap from "bootstrap";

import {

    getParticipantDetails,

    updateParticipant

} from "../../services/staff";

export default{

    name:"ParticipantDetailsPanel",

    props:{

        bookingId:{

            type:Number,

            required:true

        }

    },

    emits:[

        "close",

        "refresh"

    ],

    data(){

        return{

            offcanvas:null,

            loading:false,

            saving:false,

            participant:{},

            form:{

                booking_status:"",

                user_status:"",

                status_reason:""

            }

        }

    },

    methods:{

        async loadParticipant(){

            this.loading = true;

            try{

                const response = await getParticipantDetails(

                    this.bookingId

                );

                this.participant = response.data.participant;

                this.form = {

                    booking_status:

                        this.participant.booking_status,

                    user_status:

                        this.participant.user_status,

                    status_reason:""

                };

            }

            catch(error){

                console.error(error);

                alert(

                    error.response?.data?.message ||

                    "Unable to load participant."

                );

            }

            finally{

                this.loading = false;

            }

        },

        async updateParticipant(){

            this.saving = true;

            try{

                const response = await updateParticipant(

                    this.bookingId,

                    this.form

                );

                alert(

                    response.data.message

                );

                this.offcanvas.hide();

                this.$emit(

                    "refresh"

                );

            }

            catch(error){

                console.error(error);

                alert(

                    error.response?.data?.message ||

                    "Unable to update participant."

                );

            }

            finally{

                this.saving = false;

            }

        },

        closePanel(){

            this.offcanvas.hide();

        }

    },

    watch:{

        "form.user_status"(value){
    
            if(value==="inactive"){
    
                this.form.booking_status="cancelled";
    
            }

            else if(
                this.form.booking_status==="cancelled"
            ){
                this.form.booking_status="booked"
            }
    
        }

    },

    async mounted(){

        this.offcanvas = new bootstrap.Offcanvas(

            this.$refs.offcanvasElement

        );

        await this.loadParticipant();

        this.offcanvas.show();

        this.$refs.offcanvasElement.addEventListener(

            "hidden.bs.offcanvas",

            ()=>{

                this.$emit(

                    "close"

                );

            }

        );

    }

}

</script>

<style scoped>

.offcanvas{

    width:550px;

    border-top-left-radius:18px;

    border-bottom-left-radius:18px;

}

.offcanvas-header{

    border-bottom:1px solid #e9ecef;

    padding:18px 22px;

}

.offcanvas-header h4{

    font-weight:700;

    color:#198754;

}

.offcanvas-body{

    padding:22px;

    background:#f8f9fa;

}

.card{

    border:none;

    border-radius:14px;

    overflow:hidden;

    margin-bottom:20px;

}

.card-header{

    font-weight:600;

    font-size:15px;

    padding:12px 18px;

}

.card-body{

    padding:20px;

}

label{

    font-size:13px;

    font-weight:600;

    color:#495057;

    margin-bottom:6px;

    display:block;

}

.form-control,

.form-select{

    border-radius:10px;

    min-height:45px;

    border:1px solid #dcdcdc;

    transition:.25s;

}

.form-control:focus,

.form-select:focus{

    border-color:#198754;

    box-shadow:0 0 0 .18rem rgba(25,135,84,.15);

}



.form-control:disabled{

    background:#f8f9fa;

    color:#495057;

    opacity:1;

}

textarea.form-control{

    min-height:110px;

    resize:none;

}

.btn-success{

    border-radius:10px;

    font-weight:600;

    padding:11px;

    transition:.25s;

}

.btn-success:hover{

    transform:translateY(-2px);

    box-shadow:0 8px 20px rgba(25,135,84,.22);

}

.spinner-border{

    width:3rem;

    height:3rem;

}


.offcanvas-body::-webkit-scrollbar{

    width:8px;

}

.offcanvas-body::-webkit-scrollbar-thumb{

    background:#c8c8c8;

    border-radius:10px;

}

.offcanvas-body::-webkit-scrollbar-track{

    background:#f1f1f1;

}

@media(max-width:768px){

    .offcanvas{

        width:100%;

        border-radius:0;

    }

    .offcanvas-body{

        padding:16px;

    }

    .card-body{

        padding:16px;

    }

}

</style>