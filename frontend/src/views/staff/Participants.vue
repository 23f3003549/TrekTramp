<template>

<StaffLayout

    title="Participants"

    placeholder="Search Trek or Participant..."

    @search="handleSearch"

>

    <div v-if="filteredTreks.length===0" class="text-center py-5">

        <h5 class="text-muted">

            No Participants Found

        </h5>

    </div>

    <div

        class="accordion"

        id="participantsAccordion"

        v-else

    >

        <div

            class="accordion-item mb-3 shadow-sm"

            v-for="(trek,index) in filteredTreks"

            :key="trek.trek_id"

        >

            <!-- Accordion Header -->

            <h2

                class="accordion-header"

                :id="'heading'+index"

            >

                <button

                    class="accordion-button"

                    :class="{collapsed:index!==0}"

                    type="button"

                    data-bs-toggle="collapse"

                    :data-bs-target="'#collapse'+index"

                >

                    <div

                        class="w-100 d-flex justify-content-between align-items-center"

                    >

                        <div>

                            <h5 class="mb-1">

                                {{ trek.trek_name }}

                            </h5>

                            <small class="text-muted">

                                {{ trek.start_date }}

                                -

                                {{ trek.end_date }}

                            </small>

                        </div>

                        <div class="text-end me-4">

                            <span

                                class="badge bg-primary me-2"

                            >

                                {{ trek.participant_count }}

                                Participants

                            </span>

                            <span

                                class="badge"

                                :class="statusClass(trek.status)"

                            >

                                {{ trek.status }}

                            </span>

                        </div>

                    </div>

                </button>

            </h2>

            <!-- Accordion Body -->

            <div

                :id="'collapse'+index"

                class="accordion-collapse collapse"

                :class="{show:index===0}"

                :aria-labelledby="'heading'+index"

                data-bs-parent="#participantsAccordion"

            >

                <div class="accordion-body">

                    <div class="table-responsive participant-table">

                        <table

                            class="table table-hover align-middle"

                        >

                            <thead>

                                <tr>

                                    <th>Name</th>

                                    <th>Email</th>

                                    <th>Phone</th>

                                    <th>Status</th>

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

                                        {{ participant.name }}

                                    </td>

                                    <td>

                                        {{ participant.email }}

                                    </td>

                                    <td>

                                        {{ participant.phone }}

                                    </td>

                                    <td>

                                        <span

                                            class="badge"

                                            :class="bookingStatusClass(participant.booking_status)"

                                        >

                                            {{ participant.booking_status }}

                                        </span>

                                    </td>

                                    <td>

                                        <span

                                            class="badge"

                                            :class="paymentStatusClass(participant.payment_status)"

                                        >

                                            {{ participant.payment_status }}

                                        </span>

                                    </td>

                                    <td class="text-center">

                                        <button

                                            class="btn btn-success btn-sm"

                                            @click="viewParticipant(participant.booking_id)"

                                        >

                                            View

                                        </button>

                                    </td>

                                </tr>

                                <tr

                                    v-if="trek.participants.length===0"

                                >

                                    <td

                                        colspan="6"

                                        class="text-center text-muted"

                                    >

                                        No Participants Found

                                    </td>

                                </tr>

                            </tbody>

                        </table>

                    </div>

                </div>

            </div>

        </div>

    </div>

    <!-- Participant Details -->

    <ParticipantDetailsPanel

        v-if="selectedBooking"

        :bookingId="selectedBooking"

        @close="selectedBooking=null"

        @refresh="loadParticipants"

    />

</StaffLayout>

</template>

<script>

import StaffLayout from "../../layouts/StaffLayout.vue";

import ParticipantDetailsPanel from "../../components/staff/ParticipantDetailsPanel.vue";

import {

    getAllAssignedParticipants

} from "../../services/staff";

export default{

    name:"Participants",

    components:{

        StaffLayout,

        ParticipantDetailsPanel

    },

    data(){

        return{

            treks:[],

            searchText:"",

            selectedBooking:null,

            loading:false

        }

    },

    computed:{

        filteredTreks(){

            if(!this.searchText){

                return this.treks;

            }

            const keyword = this.searchText.toLowerCase();

            return this.treks

                .map(trek=>{

                    const trekMatch =

                        trek.trek_name

                            .toLowerCase()

                            .includes(keyword);

                    const participants =

                        trek.participants.filter(

                            participant=>

                                participant.name

                                    .toLowerCase()

                                    .includes(keyword)

                        );

                    if(trekMatch){

                        return trek;

                    }

                    if(participants.length>0){

                        return{

                            ...trek,

                            participants

                        };

                    }

                    return null;

                })

                .filter(

                    trek=>trek!==null

                );

        }

    },

    methods:{

        // ---------------- Load Participants ----------------

        async loadParticipants(){

            this.loading=true;

            try{

                const response = await getAllAssignedParticipants();

                this.treks = response.data.treks;

            }

            catch(error){

                console.error(error);

                alert(

                    error.response?.data?.message ||

                    "Unable to load participants."

                );

            }

            finally{

                this.loading=false;

            }

        },

        // ---------------- Search ----------------

        handleSearch(value){

            this.searchText = value;

        },

        // ---------------- Open Details ----------------

        viewParticipant(bookingId){

            this.selectedBooking = bookingId;

        },

        // ---------------- Booking Status Badge ----------------

        bookingStatusClass(status){

            switch(status){

                case "booked":

                    return "bg-success";

                case "completed":

                    return "bg-primary";

                case "cancelled":

                    return "bg-danger";

                case "rejected":

                    return "bg-dark";

                default:

                    return "bg-secondary";

            }

        },

        // ---------------- Payment Status Badge ----------------

        paymentStatusClass(status){

            switch(status){

                case "paid":

                    return "bg-success";

                case "pending":

                    return "bg-warning text-dark";

                case "refunded":

                    return "bg-info text-dark";

                default:

                    return "bg-secondary";

            }

        },

        // ---------------- Trek Status Badge ----------------

        statusClass(status){

            switch(status){

                case "open":

                    return "bg-success";

                case "started":

                    return "bg-primary";

                case "completed":

                    return "bg-secondary";

                case "cancelled":

                    return "bg-danger";

                default:

                    return "bg-dark";

            }

        }

    },

    mounted(){

        this.loadParticipants();

    }

}

</script>

<style scoped>

/* ================= Page ================= */

.accordion{

    --bs-accordion-border-color:#e9ecef;

    --bs-accordion-btn-focus-box-shadow:none;

}

/* ================= Accordion ================= */

.accordion-item{

    border:none;

    border-radius:14px;

    overflow:hidden;

}

.accordion-button{

    background:#ffffff;

    padding:18px 22px;

    font-weight:600;

    transition:.25s;

}

.accordion-button:not(.collapsed){

    background:#eef8f2;

    color:#198754;

}

.accordion-button:hover{

    background:#f8f9fa;

}

.accordion-body{

    background:#ffffff;

    padding:0;

}

/* ================= Table ================= */

.participant-table{

    max-height:420px;

    overflow-y:auto;

    overflow-x:auto;

}

/* Sticky Header */

thead{

    position:sticky;

    top:0;

    z-index:2;

}

thead th{

    background:#f8f9fa;

    font-weight:700;

    color:#495057;

    border-bottom:2px solid #dee2e6;

    white-space:nowrap;

}

/* Table Rows */

tbody td{

    vertical-align:middle;

    white-space:nowrap;

}

tbody tr{

    transition:.2s;

}

tbody tr:hover{

    background:#f8fbfd;

}

/* ================= Badges ================= */

.badge{

    padding:8px 12px;

    font-size:12px;

    font-weight:600;

    border-radius:30px;

    text-transform:capitalize;

}

/* ================= Buttons ================= */

.btn-success{

    border-radius:8px;

    padding:6px 18px;

    font-size:14px;

    font-weight:600;

    transition:.25s;

}

.btn-success:hover{

    transform:translateY(-2px);

    box-shadow:0 6px 15px rgba(25,135,84,.25);

}

/* ================= Scrollbar ================= */

.participant-table::-webkit-scrollbar{

    width:8px;

    height:8px;

}

.participant-table::-webkit-scrollbar-thumb{

    background:#c7c7c7;

    border-radius:10px;

}

.participant-table::-webkit-scrollbar-track{

    background:#f1f1f1;

}

/* ================= Empty State ================= */

.text-muted{

    font-size:15px;

}

/* ================= Responsive ================= */

@media(max-width:768px){

    .accordion-button{

        padding:15px;

    }

    .accordion-button h5{

        font-size:17px;

    }

    .participant-table{

        max-height:350px;

    }

    .btn-success{

        width:100%;

    }

}

</style>