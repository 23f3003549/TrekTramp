<template>

<TrekkerLayout

    title="Browse Treks"

    placeholder="Search Trek or Location..."

    @search="handleSearch"
    
>
    <!-- Empty State -->

<div

    v-if="!loading && treks.length===0"

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

        No trek matched your search.

    </p>

</div>

<!-- Trek Cards -->

<div

    v-else

    class="row"

>

    <div

        class="col-lg-4 col-md-6 mb-4"

        v-for="trek in treks"

        :key="trek.id"

    >

        <TrekCard

            :trek="trek"

            @view="openDetails"

        />

    </div>

</div>
    

    <TrekDetailsPanel

        v-if="selectedTrek"

        :trekId="selectedTrek"

        @close="selectedTrek=null"

    />

</TrekkerLayout>

</template>

<script>

import TrekkerLayout from "../../layouts/TrekkerLayout.vue";

import TrekCard from "../../components/trek/TrekCard.vue";

import TrekDetailsPanel from "../../components/trek/TrekDetailsPanel.vue";

import {

    getTreks

} from "../../services/trekker";

export default{

    name:"BrowseTreks",

    components:{

        TrekkerLayout,

        TrekCard,

        TrekDetailsPanel

    },

    data(){

        return{

            treks:[],

            selectedTrek:null,

            lastOpenedTrek:null,
            loading:false,

        }

    },


    methods:{

        async loadTreks(search=""){
            this.loading = true;

            try{

                const response=await getTreks( search);
                console.log("API Response:", response.data);

                this.treks=response.data.treks;
                console.log("Treks:", this.treks);

            }

            catch(error){

                console.error(error);

                alert("Unable to load treks.");

            }
            finally{
                this.loading=false;
            }

        },
        // async searchTreks(keyword){

        //     await this.loadTreks(
        
        //         keyword
        
        //     );

        // },

        openDetails(id){

            this.selectedTrek=id;
            this.lastOpenedTrek = id;

        },

        reopenLastTrek(){

            if(this.lastOpenedTrek){

                 this.selectedTrek = this.lastOpenedTrek;

            }

        },

        async handleSearch(value){

            await this.loadTreks(

             value

        );

        }

        

    },

    mounted(){

        this.loadTreks();
        window.addEventListener(
            "profile-updated",
             this.reopenLastTrek
        );

    },

    beforeUnmount(){

        window.removeEventListener(
            "profile-updated",
            this.reopenLastTrek
        );

    }

}

</script>

<style scoped>

.row{

    margin-top:10px;

}

</style>