<template>

    <MainLayout
       placeholder="Search Treks..."

       @search="searchTreks">

        <div class="d-flex justify-content-between align-items-center mb-4">

            <h2 class="fw-bold">
                Manage Treks
            </h2>

            <button class="btn btn-success" @click=openCreateModal()>
                + Create Trek
            </button>

        </div>

        <div class="card shadow-sm">

            <div class="card-body">

                <table class="table table-hover align-middle mb-0">

                    <thead class="table-success">

                        <tr>

                            <th>Trek Name</th>

                            <th>Location</th>

                            <th>Difficulty</th>

                            <th>Available Slots</th>

                            <th>Status</th>

                            <th class="text-center">Actions</th>

                        </tr>

                    </thead>

                    <tbody>

                        <tr
                            v-for="trek in treks"
                            :key="trek.id"
                            class="trek-row"
                            @click="viewTrek(trek.id)"
                        >

                            <td>{{ trek.trek_name }}</td>

                            <td>{{ trek.location }}</td>

                            <td>{{ trek.difficulty }}</td>

                            <td>{{ trek.available_slots }}</td>

                            <td>

                                <span
                                    class="badge"
                                    :class="{
                                        'bg-success': trek.status==='open',
                                        'bg-warning text-dark': trek.status==='pending',
                                        'bg-danger': trek.status==='cancelled',
                                        'bg-secondary': trek.status==='completed'
                                    }"
                                >
                                    {{ trek.status }}

                                </span>

                            </td>

                            <td class="text-center">

                                <button
                                    class="btn btn-warning btn-sm me-2"
                                    @click.stop="editTrek(trek)"
                                >
                                    ✏️Edit
                                </button>

                                <button
                                    class="btn btn-danger btn-sm"
                                    @click.stop=" deleteTrek(trek.id)"
                                >
                                    🗑 Delete
                                </button>

                            </td>

                        </tr>

                    </tbody>

                </table>

                <TrekFormModal v-if ="showModal" :trek="selectedTrek" @close="showModal= false" @trekSaved="handleTrekSaved"/>
                <TrekDetailsPanel v-if="showDetails" :trekId="selectedTrekId" @close="showDetails=false"
/>

            </div>

        </div>

    </MainLayout>

</template>

<script>


import MainLayout from '../layouts/MainLayout.vue';
import TrekFormModal from '../components/admin/TrekFormModal.vue';
import TrekDetailsPanel from '../components/trek/TrekDetailsPanel.vue';
import StaffDetailsPanel from '../components/admin/StaffDetailsPanel.vue';

import { RouterLink } from 'vue-router';
import { getAllTreks , getTrek } from '../services/trek.js';
import { deleteTrek as deleteapi} from '../services/trek.js';



export default {
    name: "ManageTreks",

    components: {
        MainLayout,
        TrekFormModal,
        TrekDetailsPanel,
        StaffDetailsPanel
    },

    data(){
        return{
            treks: [],
            showModal : false,
            selectedTrek:null,
            showDetails:false,
            selectedTrekId:null,
            selectedStaff:null
        }
        
    },
    methods:{

        async loadTreks(search=""){
        
            try{
        
                const response = await getAllTreks(
        
                    search
        
                );
        
                this.treks = response.data.treks;
        
            }
        
            catch(error){
        
                console.error(error);
        
                alert(
        
                    error.response?.data?.message ||
        
                    "Unable to load treks."
        
                );
        
            }
        
        },

        async handleTrekSaved(search=""){
            this.showModal = false;
            const response = await this.loadTreks();
            this.treks=response.data.treks;
        },

        async deleteTrek(id){
            try{
                await deleteapi(id);
                alert("Trek deleted successfully.");
                const response = await this.loadTreks();
                this.treks = response.data.treks;

            }
            catch(error){
                console.error(error)
                alert(
                    error.response?.data?.message || "Unable to delete"
                );
            }
        },

        openCreateModal(){
            this.selectedTrek=null;

            this.showModal=true;

        },
        viewTrek(id){
            this.selectedTrekId = id;
            this.showDetails = true;
        },

        async editTrek(trek){

            try{
        
                const response = await getTrek(trek.id);
        
                this.selectedTrek = response.data.trek;
        
                this.showModal = true;
        
            }
        
            catch(error){
        
                console.error(error);
        
                alert("Unable to load trek details.");
        
            }

        },

        async searchTreks(keyword){
        
            await this.loadTreks(
        
                keyword
        
            );
        
        },
       


    },

    mounted(){
        this.loadTreks();
    }


}
</script>

<style scoped>

h2{

    color:#198754;

}

.card{

    border:none;

    border-radius:12px;

}

.table{

    margin-bottom:0;

}

.table th{

    font-weight:600;

    vertical-align:middle;

}

.table td{

    vertical-align:middle;

}

.trek-row{

    cursor:pointer;

    transition:0.2s;

}

.trek-row:hover{

    background:#f4fdf7;

}

.btn{

    border-radius:8px;

}

.badge{

    padding:8px 12px;

    font-size:0.8rem;

}

</style>