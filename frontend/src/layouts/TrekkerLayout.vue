<template>

<div class="d-flex">


    <TrekkerSidebar />

    <div class="main-content">
      

        <div class="p-3 pb-0">

            <TrekkerNavbar 

                :title="title"

                :placeholder="placeholder"

                :searchEnabled="searchEnabled"

                @search="handleSearch"

            />

        </div>


        <div class="page-content">

            <slot></slot>

        </div>

    </div>

</div>

</template>

<script>

import TrekkerSidebar from "../components/trekker/TrekkerSidebar.vue";

import TrekkerNavbar from "../components/trekker/TrekkerNavbar.vue";

export default{

    name:"UserLayout",

    components:{

        TrekkerSidebar,

        TrekkerNavbar

    },

    props:{

        title:{

            type:String,

            default:"Dashboard"

        },

        placeholder:{

            type:String,

            default:"Search Treks..."

        },
        searchEnabled:{

            type:Boolean,
    
            default:true

        }

    },

    emits:[

        "search"

    ],

    methods:{

        handleSearch(searchText){

            this.$emit(

                "search",

                searchText

            );

        }

    }

}

</script>

<style scoped>

.bg-light{

    background:#f8f9fa !important;

}
.main-content{
    margin-left: 260px;
    width: 100%;
    min-height: 100vh;
    background: #f8f9fa;

}
.page-content{
    padding:25px
}

</style>