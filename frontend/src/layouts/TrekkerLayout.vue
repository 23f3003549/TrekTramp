<template>

<div class="d-flex">

    <!-- Sidebar -->

    <TrekkerSidebar />

    <!-- Main Content -->

    <div class="flex-grow-1 bg-light min-vh-100">

        <!-- Navbar -->

        <div class="p-3 pb-0">

            <TrekkerNavbar

                :title="title"

                :placeholder="placeholder"

                @search="handleSearch"

            />

        </div>

        <!-- Page Content -->

        <div class="p-3">

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

</style>