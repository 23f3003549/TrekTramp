<template>

    <MainLayout>

        <!-- Header -->

        <div class="d-flex justify-content-between align-items-center mb-4">

            <h2 class="fw-bold">

                Manage Users

            </h2>

        </div>

        <!-- Users Table -->

        <div class="card shadow-sm">

            <div class="card-body">

                <table class="table table-hover align-middle">

                    <thead class="table-success">

                        <tr>

                            <th>Name</th>

                            <th>Email</th>

                            <th>Status</th>

                            <th>Total Bookings</th>

                            <th class="text-center">

                                Action

                            </th>

                        </tr>

                    </thead>

                    <tbody>

                        <tr
                            v-for="user in users"
                            :key="user.id"
                        >

                            <td>

                                {{ user.name }}

                            </td>

                            <td>

                                {{ user.email }}

                            </td>

                            <td>

                                <span
                                    class="badge"
                                    :class="{

                                        'bg-success':user.status==='active',

                                        'bg-warning text-dark':user.status==='inactive',

                                        'bg-danger':user.status==='blacklisted'

                                    }"
                                >

                                    {{ user.status }}

                                </span>

                            </td>

                            <td>

                                {{ user.total_bookings }}

                            </td>

                            <td class="text-center">

                                <button
                                    class="btn btn-info btn-sm"
                                    @click="viewUser(user.id)"
                                >

                                    View / Manage

                                </button>

                            </td>

                        </tr>

                        <tr
                            v-if="users.length===0"
                        >

                            <td
                                colspan="5"
                                class="text-center text-muted py-4"
                            >

                                No users found.

                            </td>

                        </tr>

                    </tbody>

                </table>

            </div>

        </div>

        <!-- User Details -->

        <UserDetailsPanel

            v-if="selectedUserId"

            :userId="selectedUserId"

            @close="selectedUserId=null"

            @updated="loadUsers"

        />

    </MainLayout>

</template>

<script>

import MainLayout from "../layouts/MainLayout.vue";

import UserDetailsPanel from "../components/admin/UserDetailsPanel.vue";

import{

    getAllUsers

}from "../services/admin";

export default{

    name:"ManageUsers",

    components:{

        MainLayout,

        UserDetailsPanel

    },

    data(){

        return{

            users:[],

            selectedUserId:null

        }

    },

    methods:{

        //--------------------------------------------------

        async loadUsers(){

            try{

                const response=await getAllUsers();

                this.users=response.data.users;

            }

            catch(error){

                console.error(error);

                alert(

                    error.response?.data?.message ||

                    "Unable to load users."

                );

            }

        },

        //--------------------------------------------------

        viewUser(id){

            this.selectedUserId=id;

        }

    },

    mounted(){

        this.loadUsers();

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