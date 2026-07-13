<template>

<TrekkerLayout

    title="Browse Treks"

    placeholder="Search Trek..."

    @search="handleSearch"
    
>
    <h3 class="text-danger">

       Browse Treks Page Loaded

    </h3>
    <p>Total Treks : {{ treks.length }}</p>
    <div class="row">

        <div

            class="col-lg-4 col-md-6 mb-4"

            v-for="trek in filteredTreks"

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

            search:"",

            lastOpenedTrek:null

        }

    },

    computed:{

        filteredTreks(){

            if(!this.search){

                return this.treks;

            }

            return this.treks.filter(trek=>

                trek.trek_name

                    .toLowerCase()

                    .includes(

                        this.search.toLowerCase()

                    )

            );

        }

    },

    methods:{

        async loadTreks(){

            try{

                const response=await getTreks();
                console.log("API Response:", response.data);

                this.treks=response.data.treks;
                console.log("Treks:", this.treks);

            }

            catch(error){

                console.error(error);

                alert("Unable to load treks.");

            }

        },

        openDetails(id){

            this.selectedTrek=id;
            this.lastOpenedTrek = id;

        },

        reopenLastTrek(){

            if(this.lastOpenedTrek){

                 this.selectedTrek = this.lastOpenedTrek;

            }

        },

        handleSearch(value){

            this.search=value;

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