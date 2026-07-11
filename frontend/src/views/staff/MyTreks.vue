<template>

<StaffLayout
    title="My Treks"
    placeholder="Search Trek..."
>

    <div class="card shadow-sm">

        <div class="card-body">

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
                        v-for="trek in treks"
                        :key="trek.id"
                    >

                        <td>

                            {{ trek.trek_name }}

                        </td>

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

                                {{ trek.status==="open" || trek.status==="started"
                                ? "Manage"
                                : "View" }}

                            </button>

                        </td>

                    </tr>

                    <tr
                        v-if="treks.length===0"
                    >

                        <td
                            colspan="5"
                            class="text-center text-muted py-4"
                        >

                            No assigned treks.

                        </td>

                    </tr>

                </tbody>

            </table>

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

import { getMyTreks } from "../../services/staff";

export default{

    components:{

        StaffLayout,

        TrekDetailsPanel

    },

    data(){

        return{

            treks:[],

            selectedTrek:null

        }

    },

    methods:{

        async loadTreks(){

            try{

                const response = await getMyTreks();

                this.treks = response.data.treks;

            }

            catch(error){

                console.error(error);

                alert("Unable to load treks.");

            }

        },

        openDetails(id){

            this.selectedTrek=id;

        },

        formatDate(date){

            return new Date(date).toLocaleDateString();

        },

        statusClass(status){

            return{

                "bg-success":status==="open",

                "bg-primary":status==="started",

                "bg-secondary":status==="completed",

                "bg-danger":status==="cancelled"

            }

        }

    },

    mounted(){

        this.loadTreks();

    }

}

</script>

<style scoped>

.badge{

    font-size:.85rem;

}

table{

    margin-bottom:0;

}

</style>