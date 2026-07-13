<template>

<div
    class="offcanvas offcanvas-end"
    tabindex="-1"
    ref="offcanvasElement"
>

    <!-- HEADER -->

    <div class="offcanvas-header bg-success text-white">

        <h4 class="offcanvas-title">

            Staff Details

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

        <!-- CONTENT -->

        <template
            v-else-if="staff"
        >

            <!-- Personal Information -->

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

                                {{ staff.name }}

                            </p>

                            <p>

                                <strong>Email</strong>

                                <br>

                                {{ staff.email }}

                            </p>

                            <p>

                                <strong>Phone</strong>

                                <br>

                                {{ staff.phone || "-" }}

                            </p>

                        </div>

                        <div class="col-md-6">

                            <p>

                                <strong>Age</strong>

                                <br>

                                {{ staff.age || "-" }}

                            </p>

                            <p>

                                <strong>Gender</strong>

                                <br>

                                {{ staff.gender || "-" }}

                            </p>

                            <p>

                                <strong>Status</strong>

                                <br>

                                <span
                                    class="badge"
                                    :class="statusBadge"
                                >

                                    {{ staff.status }}

                                </span>

                            </p>

                        </div>

                    </div>

                </div>

            </div>

            <!-- Trek Statistics -->

            <div class="card shadow-sm mb-4">

                <div class="card-header bg-success text-white">

                    Trek Statistics

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

                                {{ statistics.active }}

                            </h3>

                            <small>

                                Active

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

            <!-- Recent Treks -->

            <div class="card shadow-sm mb-4">

                <div class="card-header bg-success text-white">

                    Recent Assigned Treks

                </div>

                <div class="card-body p-0">

                    <table class="table table-hover mb-0">

                        <thead>

                            <tr>

                                <th>Trek</th>

                                <th>Status</th>

                            </tr>

                        </thead>

                        <tbody>

                            <tr
                                v-for="trek in recentTreks"
                                :key="trek.trek_id"
                            >

                                <td>

                                    {{ trek.trek_name }}

                                </td>

                                <td>

                                    <span
                                        class="badge"
                                        :class="{

                                            'bg-primary':trek.status==='active',

                                            'bg-success':trek.status==='completed',

                                            'bg-danger':trek.status==='cancelled'

                                        }"
                                    >

                                        {{ trek.status }}

                                    </span>

                                </td>

                            </tr>

                            <tr
                                v-if="recentTreks.length===0"
                            >

                                <td
                                    colspan="2"
                                    class="text-center text-muted py-3"
                                >

                                    No assigned treks.

                                </td>

                            </tr>

                        </tbody>

                    </table>

                </div>

            </div>

            <!-- Account Management -->

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
                        v-if="staff.status_reason"
                        class="alert alert-warning"
                    >

                        <strong>

                            Previous Reason

                        </strong>

                        <br>

                        {{ staff.status_reason }}

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

import { getStaffDetails, updateStaffStatus } from "../../services/admin";

export default{

    name:"StaffDetailsPanel",

    props:{

        staffId:{

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

            staff:null,

            statistics:{

                total:0,

                active:0,

                completed:0,

                cancelled:0

            },

            recentTreks:[],

            form:{

                status:"",

                status_reason:""

            }

        }

    },

    computed:{

        statusBadge(){

            if(!this.staff){

                return "bg-secondary";

            }

            return this.staff.status==="active"

                ? "bg-success"

                : "bg-danger";

        }

    },

    methods:{

        //--------------------------------------------------

        async loadStaff(){

    this.loading = true;

    try{

        const response = await getStaffDetails(this.staffId);

        console.log("FULL RESPONSE", response);

        console.log("DATA", response.data);

        console.log("STATISTICS", response.data.statistics);

        this.staff = response.data.staff;

        this.statistics = response.data.statistics || {

            total:0,

            active:0,

            completed:0,

            cancelled:0

        };

        this.recentTreks = response.data.recent_treks || [];

        this.form = {

            status:this.staff.status,

            status_reason:""

        };

    }

    catch(error){

        console.error(error);

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

        async updateStatus(){

    if(

        this.form.status === this.staff.status &&

        this.form.status_reason.trim() === ""

    ){

        alert("No changes detected.");

        return;

    }

    try{

        const response = await updateStaffStatus(

            this.staff.id,

            {

                status:this.form.status,

                reason:this.form.status_reason

            }

        );

        alert(

            response.data.message

        );

        await this.loadStaff();

        this.$emit("updated");

    }

    catch(error){

        console.error(error);

        alert(

            error.response?.data?.message ||

            "Unable to update staff."

        );

    }

}

    },

    async mounted(){

        await this.loadStaff();

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

/* ==========================
   Offcanvas
========================== */

.offcanvas{

    width:600px;

}

/* ==========================
   Cards
========================== */

.card{

    border:none;

    border-radius:14px;

    overflow:hidden;

    transition:.25s;

}

.card:hover{

    box-shadow:0 8px 18px rgba(0,0,0,.08);

}

/* ==========================
   Headers
========================== */

.card-header{

    font-weight:600;

    font-size:16px;

}

/* ==========================
   Labels
========================== */

strong{

    color:#198754;

    font-weight:600;

}

/* ==========================
   Statistics
========================== */

.card-body h3{

    font-weight:700;

    margin-bottom:4px;

}

.card-body small{

    color:#6c757d;

    font-size:13px;

}

/* ==========================
   Table
========================== */

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

/* ==========================
   Badge
========================== */

.badge{

    font-size:12px;

    padding:7px 10px;

    border-radius:8px;

}

/* ==========================
   Form
========================== */

.form-control,

.form-select{

    border-radius:10px;

}

textarea{

    resize:none;

}

/* ==========================
   Previous Reason
========================== */

.alert{

    border-radius:10px;

    font-size:14px;

}

/* ==========================
   Button
========================== */

.btn-success{

    border-radius:10px;

    font-weight:600;

    padding:10px;

    transition:.25s;

}

.btn-success:hover{

    transform:translateY(-2px);

}

/* ==========================
   Loading Spinner
========================== */

.spinner-border{

    width:3rem;

    height:3rem;

}

/* ==========================
   Responsive
========================== */

@media (max-width:768px){

    .offcanvas{

        width:100%;

    }

    .card-body h3{

        font-size:22px;

    }

}

</style>