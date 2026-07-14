<template>

<StaffLayout

    title="My Treks"

    placeholder="Search Trek..."

    @search="searchTreks"

>

    <!-- No Treks -->

    <div

        v-if="!loading &&
              activeTreks.length===0 &&
              completedTreks.length===0 &&
              cancelledTreks.length===0"

        class="text-center py-5"

    >

        <i

            class="bi bi-map"

            style="font-size:70px;color:#adb5bd;"

        ></i>

        <h3 class="mt-3">

            No Treks Found

        </h3>

        <p class="text-muted">

            No assigned trek matched your search.

        </p>

    </div>

    <!-- Accordion -->

    <div

        v-else

        class="accordion"

        id="trekAccordion"

    >

        <!-- ================= Active ================= -->

        <div class="accordion-item mb-3">

            <h2 class="accordion-header">

                <button

                    class="accordion-button"

                    type="button"

                    data-bs-toggle="collapse"

                    data-bs-target="#activeTreks"

                >

                    <span class="fw-bold">

                        Active Treks

                    </span>

                    <span class="badge bg-success ms-3">

                        {{ activeTreks.length }}

                    </span>

                </button>

            </h2>

            <div

                id="activeTreks"

                class="accordion-collapse collapse show"

                data-bs-parent="#trekAccordion"

            >

                <div class="accordion-body">

                    <table class="table table-hover align-middle">

                        <thead>

                            <tr>

                                <th>Trek Name</th>

                                <th>Date</th>

                                <th>Participants</th>

                                <th>Status</th>

                                <th>Action</th>

                            </tr>

                        </thead>

                        <tbody>

                            <tr

                                v-for="trek in activeTreks"

                                :key="trek.id"

                            >

                                <td>{{ trek.trek_name }}</td>

                                <td>

                                    {{ formatDate(trek.start_date) }}

                                    -

                                    {{ formatDate(trek.end_date) }}

                                </td>

                                <td>

                                    {{ trek.participants }}

                                    /

                                    {{ trek.max_slots }}

                                </td>

                                <td>

                                    <span

                                        class="badge"

                                        :class="statusClass(trek.status)"

                                    >

                                        {{ trek.status }}

                                    </span>

                                </td>

                                <td>

                                    <button

                                        class="btn btn-success btn-sm"

                                        @click="openDetails(trek.id)"

                                    >

                                        Manage

                                    </button>

                                </td>

                            </tr>

                            <tr v-if="activeTreks.length===0">

                                <td colspan="5" class="text-center text-muted">

                                    No Active Treks

                                </td>

                            </tr>

                        </tbody>

                    </table>

                </div>

            </div>

        </div>

        <!-- ================= Completed ================= -->

        <div class="accordion-item mb-3">

            <h2 class="accordion-header">

                <button

                    class="accordion-button collapsed"

                    type="button"

                    data-bs-toggle="collapse"

                    data-bs-target="#completedTreks"

                >

                    <span class="fw-bold">

                        Completed Treks

                    </span>

                    <span class="badge bg-primary ms-3">

                        {{ completedTreks.length }}

                    </span>

                </button>

            </h2>

            <div

                id="completedTreks"

                class="accordion-collapse collapse"

                data-bs-parent="#trekAccordion"

            >

                <div class="accordion-body">

                    <table class="table table-hover align-middle">
                        <thead>

                            <tr>
                        
                                <th>Trek Name</th>
                        
                                <th>Date</th>
                        
                                <th>Participants</th>
                        
                                <th>Status</th>
                        
                                <th>Action</th>
                        
                            </tr>

                        </thead>

                        <tbody>

                            <tr

                                v-for="trek in completedTreks"

                                :key="trek.id"

                            >

                                <td>{{ trek.trek_name }}</td>

                                <td>

                                    {{ formatDate(trek.start_date) }}

                                    -

                                    {{ formatDate(trek.end_date) }}

                                </td>

                                <td>

                                    {{ trek.participants }}

                                    /

                                    {{ trek.max_slots }}

                                </td>

                                <td>

                                    <span

                                        class="badge"

                                        :class="statusClass(trek.status)"

                                    >

                                        {{ trek.status }}

                                    </span>

                                </td>

                                <td>

                                    <button

                                        class="btn btn-outline-primary btn-sm"

                                        @click="openDetails(trek.id)"

                                    >

                                        View

                                    </button>

                                </td>

                            </tr>

                            <tr v-if="completedTreks.length===0">

                                <td colspan="5" class="text-center text-muted">

                                    No Completed Treks

                                </td>

                            </tr>

                        </tbody>

                    </table>

                </div>

            </div>

        </div>

        <!-- ================= Cancelled ================= -->

        <div class="accordion-item">

            <h2 class="accordion-header">

                <button

                    class="accordion-button collapsed"

                    type="button"

                    data-bs-toggle="collapse"

                    data-bs-target="#cancelledTreks"

                >

                    <span class="fw-bold">

                        Cancelled Treks

                    </span>

                    <span class="badge bg-danger ms-3">

                        {{ cancelledTreks.length }}

                    </span>

                </button>

            </h2>

            <div

                id="cancelledTreks"

                class="accordion-collapse collapse"

                data-bs-parent="#trekAccordion"

            >

                <div class="accordion-body">

                    <table class="table table-hover align-middle">
                        <thead>

                            <tr>
                        
                                <th>Trek Name</th>
                        
                                <th>Date</th>
                        
                                <th>Participants</th>
                        
                                <th>Status</th>
                        
                                <th>Action</th>
                        
                            </tr>

                        </thead>

                        <tbody>

                            <tr

                                v-for="trek in cancelledTreks"

                                :key="trek.id"

                            >

                                <td>{{ trek.trek_name }}</td>

                                <td>

                                    {{ formatDate(trek.start_date) }}

                                    -

                                    {{ formatDate(trek.end_date) }}

                                </td>

                                <td>

                                    {{ trek.participants }}

                                    /

                                    {{ trek.max_slots }}

                                </td>

                                <td>

                                    <span

                                        class="badge"

                                        :class="statusClass(trek.status)"

                                    >

                                        {{ trek.status }}

                                    </span>

                                </td>

                                <td>

                                    <button

                                        class="btn btn-outline-secondary btn-sm"

                                        @click="openDetails(trek.id)"

                                    >

                                        View

                                    </button>

                                </td>

                            </tr>

                            <tr v-if="cancelledTreks.length===0">

                                <td colspan="5" class="text-center text-muted">

                                    No Cancelled Treks

                                </td>

                            </tr>

                        </tbody>

                    </table>

                </div>

            </div>

        </div>

    </div>

    <TrekDetailsPanel

        v-if="selectedTrek"

        :trekId="selectedTrek"

        @close="selectedTrek=null"

    />

</StaffLayout>

</template>

<script>

import StaffLayout from "../../layouts/StaffLayout.vue";
import TrekDetailsPanel from "../../components/trek/TrekDetailsPanel.vue";

import {

    getMyTreks

} from "../../services/staff";

export default{

    name:"MyTreks",

    components:{

        StaffLayout,

        TrekDetailsPanel

    },

    data(){

        return{

            loading:false,

            activeTreks:[],

            completedTreks:[],

            cancelledTreks:[],

            selectedTrek:null

        }

    },

    methods:{

        //--------------------------------------------------

        async loadTreks(search=""){

            this.loading = true;

            try{

                const response = await getMyTreks(

                    search

                );

                this.activeTreks =

                    response.data.active_treks;

                this.completedTreks =

                    response.data.completed_treks;

                this.cancelledTreks =

                    response.data.cancelled_treks;

            }

            catch(error){

                console.error(error);

                alert(

                    error.response?.data?.message ||

                    "Unable to load treks."

                );

            }

            finally{

                this.loading = false;

            }

        },

        //--------------------------------------------------

        async searchTreks(keyword){

            await this.loadTreks(

                keyword

            );

        },

        //--------------------------------------------------

        openDetails(id){

            this.selectedTrek = id;

        },

        //--------------------------------------------------

        formatDate(date){

            return new Date(date).toLocaleDateString(

                "en-IN",

                {

                    day:"2-digit",

                    month:"short",

                    year:"numeric"

                }

            );

        },

        //--------------------------------------------------

        statusClass(status){

            return{

                "bg-success":

                    status==="open",

                "bg-primary":

                    status==="started",

                "bg-secondary":

                    status==="completed",

                "bg-danger":

                    status==="cancelled"

            };

        }

    },

    mounted(){

        this.loadTreks();

    }

}

</script>

<style scoped>

/* ---------------- Page ---------------- */

.accordion-item{

    border:none;

    border-radius:14px;

    overflow:hidden;

    box-shadow:0 2px 12px rgba(0,0,0,.08);

}

.accordion-item:not(:last-child){

    margin-bottom:20px;

}

/* ---------------- Accordion Header ---------------- */

.accordion-button{

    background:#ffffff;

    font-weight:600;

    padding:18px 22px;

    box-shadow:none;

}

.accordion-button:not(.collapsed){

    background:#f8fff9;

    color:#198754;

}

.accordion-button:focus{

    box-shadow:none;

}

.accordion-button::after{

    transform:scale(.9);

}

/* ---------------- Accordion Body ---------------- */

.accordion-body{

    background:#ffffff;

    padding:0;

}

/* ---------------- Table ---------------- */

.table{

    margin-bottom:0;

}

.table thead{

    background:#f8f9fa;

}

.table thead th{

    font-weight:600;

    border-bottom:2px solid #dee2e6;

    padding:14px;

}

.table tbody td{

    vertical-align:middle;

    padding:14px;

}

.table tbody tr:hover{

    background:#f8fff9;

}

/* ---------------- Badges ---------------- */

.badge{

    font-size:.82rem;

    padding:7px 12px;

    border-radius:30px;

}

/* ---------------- Buttons ---------------- */

.btn{

    border-radius:8px;

    padding:5px 15px;

    font-weight:500;

}

/* ---------------- Empty State ---------------- */

.text-center i{

    opacity:.55;

}

.text-center h3{

    font-weight:700;

}

.text-center p{

    font-size:.95rem;

}

/* ---------------- Responsive ---------------- */

@media(max-width:992px){

    .table{

        font-size:.92rem;

    }

    .accordion-button{

        padding:15px;

    }

}

@media(max-width:768px){

    .table{

        min-width:700px;

    }

}

</style>