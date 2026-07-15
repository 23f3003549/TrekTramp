<template>

    <MainLayout
    
    placeholder="Search Bookings..."

    @search="searchBookings">


        <div class="d-flex justify-content-between align-items-center mb-4">

            <h2 class="fw-bold">

                Booking Management

            </h2>

        </div>


        <div

            v-if="treks.length===0"

            class="alert alert-info"

        >

            No bookings available.

        </div>

        <div

            class="accordion"

            id="bookingAccordion"

        >

            <div

                class="accordion-item mb-3"

                v-for="trek in treks"

                :key="trek.trek_id"

            >


                <h2

                    class="accordion-header"

                    :id="'heading'+trek.trek_id"

                >

                    <button

                        class="accordion-button collapsed"

                        type="button"

                        data-bs-toggle="collapse"

                        :data-bs-target="'#collapse'+trek.trek_id"

                    >

                        <div class="w-100">

                            <div class="d-flex justify-content-between align-items-center">

                                <div>

                                    <h5 class="mb-1">

                                        {{ trek.trek_name }}

                                    </h5>

                                    <small class="text-muted">

                                        {{ trek.location }}

                                    </small>

                                </div>

                                <div class="text-end me-3">

                                    <small>

                                        {{ trek.start_date }}

                                        -

                                        {{ trek.end_date }}

                                    </small>

                                </div>

                            </div>

                        </div>

                    </button>

                </h2>

                <div

                    :id="'collapse'+trek.trek_id"

                    class="accordion-collapse collapse"

                    :aria-labelledby="'heading'+trek.trek_id"

                    data-bs-parent="#bookingAccordion"

                >

                    <div class="accordion-body">

                        <div class="row mb-4">

                            <div class="col-md-3">

                                <div class="card text-center shadow-sm">

                                    <div class="card-body">

                                        <h4 class="text-primary">

                                            {{ trek.statistics.total }}

                                        </h4>

                                        <small>

                                            Total Bookings

                                        </small>

                                    </div>

                                </div>

                            </div>

                            <div class="col-md-3">

                                <div class="card text-center shadow-sm">

                                    <div class="card-body">

                                        <h4 class="text-success">

                                            {{ trek.statistics.booked }}

                                        </h4>

                                        <small>

                                            Booked

                                        </small>

                                    </div>

                                </div>

                            </div>

                            <div class="col-md-3">

                                <div class="card text-center shadow-sm">

                                    <div class="card-body">

                                        <h4 class="text-secondary">

                                            {{ trek.statistics.completed }}

                                        </h4>

                                        <small>

                                            Completed

                                        </small>

                                    </div>

                                </div>

                            </div>

                            <div class="col-md-3">

                                <div class="card text-center shadow-sm">

                                    <div class="card-body">

                                        <h4 class="text-danger">

                                            {{ trek.statistics.cancelled }}

                                        </h4>

                                        <small>

                                            Cancelled

                                        </small>

                                    </div>

                                </div>

                            </div>

                        </div>

                        <div class="table-responsive">

                            <table class="table table-hover align-middle">

                                <thead class="table-success">

                                    <tr>

                                        <th>Name</th>

                                        <th>Email</th>

                                        <th>Booking</th>

                                        <th>Payment</th>

                                        <th class="text-center">

                                            Action

                                        </th>

                                    </tr>

                                </thead>

                                <tbody>

                                    <tr

                                        v-for="participant in trek.participants"

                                        :key="participant.booking_id"

                                    >

                                        <td>

                                            {{ participant.user_name }}

                                        </td>

                                        <td>

                                            {{ participant.email }}

                                        </td>

                                        <td>

                                            <span

                                                class="badge"

                                                :class="{

                                                    'bg-success':participant.booking_status==='booked',

                                                    'bg-secondary':participant.booking_status==='completed',

                                                    'bg-danger':participant.booking_status==='cancelled'

                                                }"

                                            >

                                                {{ participant.booking_status }}

                                            </span>

                                        </td>

                                        <td>

                                            <span

                                                class="badge"

                                                :class="{

                                                    'bg-success':participant.payment_status==='paid',

                                                    'bg-warning text-dark':participant.payment_status==='pending',

                                                    'bg-info text-dark':participant.payment_status==='refunded'

                                                }"

                                            >

                                                {{ participant.payment_status }}

                                            </span>

                                        </td>

                                        <td class="text-center">

                                            <button

                                                class="btn btn-info btn-sm"

                                                @click="viewBooking(participant.booking_id)"

                                            >

                                                View

                                            </button>

                                        </td>

                                    </tr>

                                </tbody>

                            </table>

                        </div>

                    </div>

                </div>

            </div>

        </div>


        <BookingDetailsPanel

            v-if="selectedBookingId"

            :bookingId="selectedBookingId"

            @close="selectedBookingId=null"

            @updated="loadBookings"

        />

    </MainLayout>

</template>

<script>

import MainLayout from "../layouts/MainLayout.vue";

import BookingDetailsPanel from "../components/admin/BookingDetailsPanel.vue";

import{

    getAllBookings

}from "../services/admin";

export default{

    name:"ManageBookings",

    components:{

        MainLayout,

        BookingDetailsPanel

    },

    data(){

        return{

            treks:[],

            selectedBookingId:null,

            loading:false

        }

    },

    methods:{
        async loadBookings(search=""){

            this.loading=true;

            try{

                const response = await getAllBookings(search);

                this.treks = response.data.treks;

            }

            catch(error){

                console.error(error);

                alert(

                    error.response?.data?.message ||

                    "Unable to load bookings."

                );

            }

            finally{

                this.loading=false;

            }

        },

        viewBooking(bookingId){

            this.selectedBookingId = bookingId;

        },

        async searchBookings(keyword){

            await this.loadBookings(
        
                keyword
        
            );

        }

    },

    mounted(){

        this.loadBookings();

    }

}

</script>

<style scoped>

h2{

    color:#198754;

}


.card{

    border:none;

    border-radius:14px;

}

.accordion-item{

    border:none;

    border-radius:14px !important;

    overflow:hidden;

    box-shadow:0 2px 10px rgba(0,0,0,.08);

}

.accordion-button{

    background:#f8f9fa;

    font-weight:600;

    padding:18px;

}

.accordion-button:not(.collapsed){

    background:#198754;

    color:white;

}

.accordion-button:focus{

    box-shadow:none;

}

.accordion-body{

    background:#fff;

}

.card h4{

    font-weight:700;

    margin-bottom:4px;

}

.card small{

    color:#6c757d;

}

.table th{

    font-weight:600;

}

.table td{

    vertical-align:middle;

}

.table-hover tbody tr:hover{

    background:#f8f9fa;

}


.badge{

    padding:8px 12px;

    border-radius:20px;

    font-size:.78rem;

    font-weight:500;

}

.btn{

    border-radius:8px;

}

.btn-info{

    color:white;

}

.table-responsive{

    border-radius:10px;

    overflow:hidden;

}

</style>