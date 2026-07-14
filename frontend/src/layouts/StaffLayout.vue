<template>

<div class="staff-layout">

    <!-- Sidebar -->

    <StaffSidebar />

    <!-- Main Section -->

    <div class="main-content">

        <!-- Navbar -->

        <StaffNavbar

            :title="title"

            :placeholder="placeholder"
            :searchEnabled="searchEnabled"

            @search="handleSearch"

        />

        <!-- Page Content -->

        <div class="page-content">

            <slot />

        </div>

    </div>

</div>

</template>

<script>

import StaffSidebar from "../components/staff/StaffSidebar.vue";

import StaffNavbar from "../components/staff/StaffNavbar.vue";

export default{

    name:"StaffLayout",

    components:{

        StaffSidebar,

        StaffNavbar

    },

    props:{

        title:{

            type:String,

            default:"Dashboard"

        },

        placeholder:{

            type:String,

            default:"Search Trek or Participant.."

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

        handleSearch(value){

            this.$emit(

                "search",

                value

            );

        }

    }

}

</script>

<style scoped>

.staff-layout{

    display:flex;

    background:#f5f7fb;

    min-height:100vh;

}

.main-content{

    margin-left:260px;

    width:100%;

    padding:20px;

}

.page-content{

    margin-top:20px;

}


</style>