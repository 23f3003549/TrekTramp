<template>

    <MainLayout>

        <div class="d-flex justify-content-between align-items-center mb-4">

            <h2 class="fw-bold">
                Manage Staff
            </h2>

            <button
                class="btn btn-success"
                @click="openCreatePanel"
            >
                + Create Staff
            </button>

        </div>

        <div class="card shadow-sm">

            <div class="card-body">

                <table class="table table-hover align-middle">

                    <thead class="table-success">

                        <tr>

                            <th>Name</th>

                            <th>Email</th>

                            <th>Status</th>

                            <th>Assigned Trek</th>

                            <th class="text-center">
                                Actions
                            </th>

                        </tr>

                    </thead>

                    <tbody>

                        <tr
                            v-for="staff in staffs"
                            :key="staff.id"
                        >

                            <td>

                                {{ staff.name }}

                            </td>

                            <td>

                                {{ staff.email }}

                            </td>

                            <td>

                                <span
                                    class="badge"
                                    :class="{
                                        'bg-success': staff.status === 'active',
                                        'bg-warning text-dark': staff.status === 'inactive',
                                        'bg-danger': staff.status === 'blacklisted'

                                    }"
                                >

                                    {{ staff.status }}

                                </span>

                            </td>

                            <td>

                                {{ staff.assigned_treks.length ? staff.assigned_treks.join(", ") : "-" }}

                            </td>

                            <td class="text-center">

                                <button
                                    class="btn btn-info btn-sm me-2"
                                    @click="viewStaff(staff.id)"
                                >

                                    View

                                </button>

                                <button
                                    class="btn btn-warning btn-sm me-2"
                                    @click="editStaff(staff)"
                                >

                                    Edit

                                </button>

                                <div
                                    class="dropdown d-inline"
                                >                                
                                
                                    <button
                                        class="btn btn-secondary btn-sm dropdown-toggle"
                                        data-bs-toggle="dropdown"
                                    >
                                
                                        Action
                                
                                    </button>
                                
                                    <ul
                                        class="dropdown-menu"
                                    >
                                
                                        <li
                                            v-if="staff.status!='active'"
                                        >
                                
                                            <button
                                                class="dropdown-item"
                                                @click.stop="changeStatus(staff,'active')"
                                            >
                                
                                                🟢 Active
                                
                                            </button>
                                
                                        </li>
                                
                                        <li
                                            v-if="staff.status!='inactive'"
                                        >
                                
                                            <button
                                                class="dropdown-item"
                                                @click.stop="changeStatus(staff,'inactive')"
                                            >
                                
                                                🟡 Inactive
                                
                                            </button>
                                
                                        </li>
                                
                                        <li
                                            v-if="staff.status!='blacklisted'"
                                        >
                                
                                            <button
                                                class="dropdown-item text-danger"
                                                @click.stop="changeStatus(staff,'blacklisted')"
                                            >
                                
                                                🔴 Blacklist
                                
                                            </button>
                                
                                        </li>
                                
                                    </ul>

                                </div>

                            </td>

                        </tr>

                    </tbody>

                </table>

            </div>

        </div>

        <StaffFormPanel

            v-if="showPanel"

            :staff="selectedStaff"

            @close="showPanel=false"

            @staffSaved="handleStaffSaved"

        />

    </MainLayout>

</template>

<script>

import MainLayout from "../layouts/MainLayout.vue";

import StaffFormPanel from "../components/staff/StaffFormPanel.vue";

import {

    getAllStaff,

    getStaff,

    changeStaffStatus

} from "../services/staff";

export default{

    name:"ManageStaff",

    components:{

        MainLayout,

        StaffFormPanel

    },

    data(){

        return{

            staffs:[],

            showPanel:false,

            selectedStaff:null

        }

    },

    methods:{

        async loadStaff(){

            try{

                const response=await getAllStaff();

                this.staffs=response.data.staffs;

            }

            catch(error){

                console.error(error);

            }

        },

        openCreatePanel(){

            this.selectedStaff=null;

            this.showPanel=true;

        },

        async editStaff(staff){

            try{

                const response=await getStaff(staff.id);

                this.selectedStaff=response.data.staff;

                this.showPanel=true;

            }

            catch(error){

                console.error(error);

                alert("Unable to load staff.");

            }

        },

        async changeStatus(staff,status){

            try{
        
                await changeStaffStatus(
        
                    staff.id,
        
                    status
        
                );
        
                alert("Status updated successfully.");
        
                await this.loadStaff();
        
            }
        
            catch(error){
        
                console.error(error);
        
                alert(
        
                    error.response?.data?.message ||
        
                    "Unable to update status."
        
                );
        
            }

        },

        viewStaff(id){

            alert("Staff Details Panel (Coming Next)");

        },

        async handleStaffSaved(){

            this.showPanel=false;

            await this.loadStaff();

        }

    },

    mounted(){

        this.loadStaff();

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

.table th{

    font-weight:600;

}

.table td{

    vertical-align:middle;

}

.btn{

    border-radius:8px;

}

.badge{

    padding:8px 12px;

    font-size:.8rem;

}

</style>