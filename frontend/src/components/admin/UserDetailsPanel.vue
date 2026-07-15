<template>

<div
    class="offcanvas offcanvas-end"
    tabindex="-1"
    ref="offcanvasElement"
>

    <div class="offcanvas-header bg-success text-white">

        <h4 class="offcanvas-title">

            User Details

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

        <template
            v-else-if="user"
        >

            <div class="card shadow-sm mb-4">

                <div class="card-header bg-success text-white">

                    Personal Information

                </div>

                <div class="card-body">

                    <div class="row">

                        <div class="col-md-6">

                            <p>

                                <strong>Name</strong>

                                <br>

                                {{ user.name }}

                            </p>

                            <p>

                                <strong>Email</strong>

                                <br>

                                {{ user.email }}

                            </p>

                            <p>

                                <strong>Phone</strong>

                                <br>

                                {{ user.phone || "-" }}

                            </p>

                        </div>

                        <div class="col-md-6">

                            <p>

                                <strong>Age</strong>

                                <br>

                                {{ user.age || "-" }}

                            </p>

                            <p>

                                <strong>Gender</strong>

                                <br>

                                {{ user.gender || "-" }}

                            </p>

                            <p>

                                <strong>Status</strong>

                                <br>

                                <span
                                    class="badge"
                                    :class="statusBadge"
                                >

                                    {{ user.status }}

                                </span>

                            </p>

                        </div>

                    </div>

                </div>

            </div>

            <div class="card shadow-sm mb-4">

                <div class="card-header bg-success text-white">

                    Booking Statistics

                </div>

                <div class="card-body">

                    <div class="row text-center">

                        <div class="col-3">

                            <h3 class="text-success">

                                {{ statistics.total }}

                            </h3>

                            <small>

                                Total

                            </small>

                        </div>

                        <div class="col-3">

                            <h3 class="text-primary">

                                {{ statistics.upcoming }}

                            </h3>

                            <small>

                                Upcoming

                            </small>

                        </div>

                        <div class="col-3">

                            <h3 class="text-success">

                                {{ statistics.completed }}

                            </h3>

                            <small>

                                Completed

                            </small>

                        </div>

                        <div class="col-3">

                            <h3 class="text-danger">

                                {{ statistics.cancelled }}

                            </h3>

                            <small>

                                Cancelled

                            </small>

                        </div>

                    </div>

                </div>

            </div>

            <div class="card shadow-sm mb-4">

                <div class="card-header bg-success text-white">

                    Recent Bookings

                </div>

                <div class="card-body p-0">

                    <table class="table table-hover mb-0">

                        <thead>

                            <tr>

                                <th>Trek</th>

                                <th>Booking</th>

                                <th>Payment</th>

                            </tr>

                        </thead>

                        <tbody>

                            <tr
                                v-for="booking in recentBookings"
                                :key="booking.booking_id"
                            >

                                <td>

                                    {{ booking.trek_name }}

                                </td>

                                <td>

                                    <span
                                        class="badge"
                                        :class="{

                                            'bg-primary': booking.booking_status==='booked',

                                            'bg-success': booking.booking_status==='completed',

                                            'bg-danger': booking.booking_status==='cancelled'

                                        }"
                                    >

                                        {{ booking.booking_status }}

                                    </span>

                                </td>

                                <td>

                                    <span
                                        class="badge"
                                        :class="{

                                            'bg-success': booking.payment_status==='paid',

                                            'bg-warning text-dark': booking.payment_status==='pending',

                                            'bg-info': booking.payment_status==='refunded'

                                        }"
                                    >

                                        {{ booking.payment_status }}

                                    </span>

                                </td>

                            </tr>

                            <tr
                                v-if="recentBookings.length===0"
                            >

                                <td
                                    colspan="3"
                                    class="text-center text-muted py-3"
                                >

                                    No bookings found.

                                </td>

                            </tr>

                        </tbody>

                    </table>

                </div>

            </div>

            <div class="card shadow-sm">

                <div class="card-header bg-success text-white">

                    Account Management

                </div>

                <div class="card-body">

                    <div class="mb-3">

                        <label class="form-label">

                            Account Status

                        </label>

                        <select
                            class="form-select"
                            v-model="form.status"
                        >

                            <option value="active">

                                Active

                            </option>

                            <option value="inactive">

                                Inactive

                            </option>

                            <option value="blacklisted">

                                Blacklisted

                            </option>

                        </select>

                    </div>

                    <div class="mb-3">

                        <label class="form-label">

                            Reason (Optional)

                        </label>

                        <textarea
                            class="form-control"
                            rows="3"
                            v-model="form.status_reason"
                            placeholder="Reason for changing account status..."
                        ></textarea>

                    </div>

                    <div
                        v-if="user.status_reason"
                        class="alert alert-warning"
                    >

                        <strong>

                            Previous Reason

                        </strong>

                        <br>

                        {{ user.status_reason }}

                    </div>

                    <button
                        class="btn btn-success w-100"
                        @click="updateStatus"
                    >

                        Update Status

                    </button>

                </div>

            </div>

        </template>

    </div>

</div>

</template>

<script>

import * as bootstrap from "bootstrap";

import {

    getUserDetails,

    updateUserStatus

} from "../../services/admin";

export default{

    name:"UserDetailsPanel",

    props:{

        userId:{

            type:Number,

            required:true

        }

    },

    emits:[

        "close",

        "updated"

    ],

    data(){

        return{

            loading:true,

            offcanvas:null,

            user:null,

            statistics:{

                total:0,

                upcoming:0,

                completed:0,

                cancelled:0

            },

            recentBookings:[],

            form:{

                status:"",

                status_reason:""

            }

        }

    },

    computed:{

        statusBadge(){

            if(!this.user){

                return {};

            }

            return{

                "bg-success":this.user.status==="active",

                "bg-warning text-dark":this.user.status==="inactive",

                "bg-danger":this.user.status==="blacklisted"

            };

        }

    },

    methods:{

        async loadUser(){

            this.loading=true;

            try{

                const response = await getUserDetails(

                    this.userId

                );

                this.user = response.data.user;

                this.statistics = response.data.statistics;

                this.recentBookings = response.data.recent_bookings;

                this.form = {

                    status:this.user.status,

                    status_reason:""

                };

            }

            catch(error){

                console.error(error);

                alert(

                    error.response?.data?.message ||

                    "Unable to load user details."

                );

            }

            finally{

                this.loading=false;

            }

        },

        closePanel(){

            this.offcanvas.hide();

        },

        async updateStatus(){

            if(

                this.form.status===this.user.status &&

                this.form.status_reason.trim()===""

            ){

                alert(

                    "No changes detected."

                );

                return;

            }

            try{

                const response = await updateUserStatus(

                    this.user.id,

                    {

                        status:this.form.status,

                        reason:this.form.status_reason

                    }

                );

                alert(

                    response.data.message

                );

                await this.loadUser();

                this.$emit("updated");

            }

            catch(error){

                console.error(error);

                alert(

                    error.response?.data?.message ||

                    "Unable to update user."

                );

            }

        }

    },

    async mounted(){

        await this.loadUser();

        this.offcanvas = new bootstrap.Offcanvas(

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

    width:600px;

}

.card{

    border:none;

    border-radius:14px;

    overflow:hidden;

    transition:.25s;

}

.card:hover{

    box-shadow:0 8px 18px rgba(0,0,0,.08);

}

.card-header{

    font-weight:600;

    font-size:16px;

}

strong{

    color:#198754;

    font-weight:600;

}

.card-body h3{

    font-weight:700;

    margin-bottom:4px;

}

.card-body small{

    color:#6c757d;

    font-size:13px;

}

.table{

    margin-bottom:0;

}

.table thead{

    background:#f8f9fa;

}

.table th{

    font-size:14px;

    font-weight:600;

}

.table td{

    vertical-align:middle;

}

.badge{

    font-size:12px;

    padding:7px 10px;

    border-radius:8px;

}

.form-control,

.form-select{

    border-radius:10px;

}

textarea{

    resize:none;

}

.alert{

    border-radius:10px;

    font-size:14px;

}

.btn-success{

    border-radius:10px;

    font-weight:600;

    padding:10px;

    transition:.25s;

}

.btn-success:hover{

    transform:translateY(-2px);

}

.spinner-border{

    width:3rem;

    height:3rem;

}

@media (max-width:768px){

    .offcanvas{

        width:100%;

    }

    .card-body h3{

        font-size:22px;

    }

}

</style>