<template>

<div
    class="offcanvas offcanvas-end"
    tabindex="-1"
    ref="offcanvasElement"
>

    <!-- Header -->

    <div class="offcanvas-header bg-success text-white">

        <h4 class="offcanvas-title">

            Booking Details

        </h4>

        <button
            class="btn-close btn-close-white"
            @click="closePanel"
        ></button>

    </div>

    <div class="offcanvas-body">

        <!-- Loading -->

        <div
            v-if="loading"
            class="text-center py-5"
        >

            <div class="spinner-border text-success"></div>

        </div>

        <!-- Content -->

        <template
            v-else-if="booking"
        >

            <!-- ======================================= -->
            <!-- User Information -->
            <!-- ======================================= -->

            <div class="card shadow-sm mb-4">

                <div class="card-header bg-success text-white">

                    User Information

                </div>

                <div class="card-body">

                    <div class="row">

                        <div class="col-md-6">

                            <p>

                                <strong>Name</strong>

                                <br>

                                {{ booking.user.name }}

                            </p>

                            <p>

                                <strong>Email</strong>

                                <br>

                                {{ booking.user.email }}

                            </p>

                            <p>

                                <strong>Phone</strong>

                                <br>

                                {{ booking.user.phone || "-" }}

                            </p>

                        </div>

                        <div class="col-md-6">

                            <p>

                                <strong>Age</strong>

                                <br>

                                {{ booking.user.age || "-" }}

                            </p>

                            <p>

                                <strong>Gender</strong>

                                <br>

                                {{ booking.user.gender || "-" }}

                            </p>

                            <p>

                                <strong>Account Status</strong>

                                <br>

                                <span
                                    class="badge"
                                    :class="{

                                        'bg-success':booking.user.status==='active',

                                        'bg-warning text-dark':booking.user.status==='inactive',

                                        'bg-danger':booking.user.status==='blacklisted'

                                    }"
                                >

                                    {{ booking.user.status }}

                                </span>

                            </p>

                        </div>

                    </div>

                </div>

            </div>

            <!-- ======================================= -->
            <!-- Trek Information -->
            <!-- ======================================= -->

            <div class="card shadow-sm mb-4">

                <div class="card-header bg-success text-white">

                    Trek Information

                </div>

                <div class="card-body">

                    <div class="row">

                        <div class="col-md-6">

                            <p>

                                <strong>Trek</strong>

                                <br>

                                {{ booking.trek.trek_name }}

                            </p>

                            <p>

                                <strong>Location</strong>

                                <br>

                                {{ booking.trek.location }}

                            </p>

                            <p>

                                <strong>Difficulty</strong>

                                <br>

                                {{ booking.trek.difficulty }}

                            </p>

                        </div>

                        <div class="col-md-6">

                            <p>

                                <strong>Price</strong>

                                <br>

                                ₹ {{ booking.trek.price }}

                            </p>

                            <p>

                                <strong>Start Date</strong>

                                <br>

                                {{ booking.trek.start_date }}

                            </p>

                            <p>

                                <strong>End Date</strong>

                                <br>

                                {{ booking.trek.end_date }}

                            </p>

                        </div>

                    </div>

                </div>

            </div>

            <!-- ======================================= -->
            <!-- Booking Information -->
            <!-- ======================================= -->

            <div class="card shadow-sm mb-4">

                <div class="card-header bg-success text-white">

                    Booking Information

                </div>

                <div class="card-body">

                    <p>

                        <strong>Booking Date :</strong>

                        {{ booking.booking_date }}

                    </p>

                    <p>

                        <strong>Booking Status :</strong>

                        <span
                            class="badge"
                            :class="{

                                'bg-success':booking.booking_status==='booked',

                                'bg-secondary':booking.booking_status==='completed',

                                'bg-danger':booking.booking_status==='cancelled'

                            }"
                        >

                            {{ booking.booking_status }}

                        </span>

                    </p>

                    <p>

                        <strong>Payment Status :</strong>

                        <span
                            class="badge"
                            :class="{

                                'bg-success':booking.payment_status==='paid',

                                'bg-warning text-dark':booking.payment_status==='pending',

                                'bg-info text-dark':booking.payment_status==='refunded'

                            }"
                        >

                            {{ booking.payment_status }}

                        </span>

                    </p>

                    <p>

                        <strong>Cancelled By :</strong>

                        {{ booking.cancelled_by || "-" }}

                    </p>

                    <p>

                        <strong>Reason :</strong>

                        {{ booking.status_reason || "-" }}

                    </p>

                </div>

            </div>

            <!-- ======================================= -->
            <!-- Booking Management -->
            <!-- ======================================= -->

            <div class="card shadow-sm">

                <div class="card-header bg-success text-white">

                    Booking Management

                </div>

                <div class="card-body">

                    <div class="mb-3">

                        <label class="form-label">

                            Booking Status

                        </label>

                        <select
                            class="form-select"
                            v-model="form.booking_status"
                            :disabled="booking.booking_status!=='booked'"
                        >

                            <option value="booked">

                                Booked

                            </option>

                            <option value="cancelled">

                                Cancelled

                            </option>

                        </select>

                    </div>

                    <div class="mb-3">

                        <label class="form-label">

                            Reason

                        </label>

                        <textarea
                            class="form-control"
                            rows="3"
                            placeholder="Reason for cancellation..."
                            v-model="form.reason"
                            :disabled="booking.booking_status!=='booked'"
                        ></textarea>

                    </div>

                    <button
                        class="btn btn-success w-100"
                        @click="updateBooking"
                        :disabled="booking.booking_status!=='booked'"
                    >

                        Update Booking

                    </button>

                </div>

            </div>

        </template>

    </div>

</div>

</template>

<script>

import * as bootstrap from "bootstrap";

import{

    getBookingDetails,

    updateBooking

}from "../../services/admin";

export default{

    name:"BookingDetailsPanel",

    props:{

        bookingId:{

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

            booking:null,

            form:{

                booking_status:"",

                reason:""

            }

        }

    },

    methods:{

        //--------------------------------------------------

        async loadBooking(){

            this.loading=true;

            try{

                const response = await getBookingDetails(

                    this.bookingId

                );

                this.booking = response.data.booking;

                this.form = {

                    booking_status:

                        this.booking.booking_status,

                    reason:""

                };

            }

            catch(error){

                console.error(error);

                alert(

                    error.response?.data?.message ||

                    "Unable to load booking."

                );

            }

            finally{

                this.loading=false;

            }

        },

        //--------------------------------------------------

        closePanel(){

            this.offcanvas.hide();

        },

        //--------------------------------------------------

        async updateBooking(){

            if(

                this.form.booking_status===

                this.booking.booking_status

            ){

                alert(

                    "No changes detected."

                );

                return;

            }

            if(

                this.form.booking_status==="cancelled"

                &&

                !confirm(

                    "Are you sure you want to cancel this booking?"

                )

            ){

                return;

            }

            try{

                const response = await updateBooking(

                    this.booking.booking_id,

                    this.form

                );

                alert(

                    response.data.message

                );

                await this.loadBooking();

                this.$emit(

                    "updated"

                );

            }

            catch(error){

                console.error(error);

                alert(

                    error.response?.data?.message ||

                    "Unable to update booking."

                );

            }

        }

    },

    async mounted(){

        await this.loadBooking();

        this.offcanvas = new bootstrap.Offcanvas(

            this.$refs.offcanvasElement

        );

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

/* ---------------- Offcanvas ---------------- */

.offcanvas{

    width:550px;

}

.offcanvas-body{

    background:#f8f9fa;

}

/* ---------------- Card ---------------- */

.card{

    border:none;

    border-radius:14px;

    overflow:hidden;

}

.card-header{

    font-weight:600;

    font-size:1rem;

}

/* ---------------- Typography ---------------- */

strong{

    color:#198754;

}

p{

    margin-bottom:1rem;

}

.form-label{

    font-weight:600;

}

/* ---------------- Form ---------------- */

.form-control,

.form-select{

    border-radius:10px;

}

textarea{

    resize:none;

}

/* ---------------- Buttons ---------------- */

.btn{

    border-radius:10px;

    font-weight:500;

}

/* ---------------- Badge ---------------- */

.badge{

    padding:8px 12px;

    border-radius:20px;

    font-size:.8rem;

    text-transform:capitalize;

}

/* ---------------- Loading ---------------- */

.spinner-border{

    width:3rem;

    height:3rem;

}

/* ---------------- Disabled ---------------- */

.form-select:disabled,

.form-control:disabled{

    background:#e9ecef;

    opacity:1;

    cursor:not-allowed;

}

.btn:disabled{

    cursor:not-allowed;

}

/* ---------------- Responsive ---------------- */

@media (max-width:768px){

    .offcanvas{

        width:100%;

    }

}

</style>