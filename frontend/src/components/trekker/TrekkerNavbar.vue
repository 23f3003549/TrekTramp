<template>

<nav class="navbar navbar-expand-lg bg-white shadow-sm px-4">

    <div class="container-fluid">

        <!-- Page Title -->

        <h4 class="fw-bold mb-0">

            {{ title }}

        </h4>

        <!-- Search -->

        <div class="mx-auto search-box">

            <div class="input-group">

                <span class="input-group-text bg-white">

                    <i class="bi bi-search"></i>

                </span>

                <input

                    type="text"

                    class="form-control"

                    :placeholder="placeholder"

                    v-model="searchText"

                    @input="search"

                >

            </div>

        </div>

        <!-- Right Section -->

        <div class="d-flex align-items-center">

            <div class="text-end me-3">

                <div class="fw-semibold">

                    {{ trekkerName }}

                </div>

                <small class="text-muted">

                    {{ today }}

                </small>

            </div>

            <div class="profile-circle"
            @click="showProfile=true">

                {{ initials }}

            </div>

        </div>

    </div>

</nav>

<ProfilePanel

    v-if="showProfile"

    @close="showProfile=false"

/>

</template>

<script>

import ProfilePanel from "../common/ProfilePanel.vue";

export default{

    name:"TrekkerNavbar",
    components :{
        ProfilePanel
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

    data(){

        return{

            searchText:"",

            trekkerName:localStorage.getItem("name") || "Trekker",

            showProfile:false

        }

    },

    computed:{

        initials(){

            return this.trekkerName

                .split(" ")

                .map(word => word.charAt(0))

                .join("")

                .substring(0,2)

                .toUpperCase();

        },

        today(){

            return new Date().toLocaleDateString(

                "en-IN",

                {

                    day:"numeric",

                    month:"long",

                    year:"numeric"

                }

            );

        }

    },

    methods:{

        search(){

            this.$emit(

                "search",

                this.searchText

            );

        },
        openProfile(){

            this.showProfile = true;

        }

    },
    mounted(){

        window.addEventListener(
            "open-profile",
            this.openProfile
        );

    },
    beforeUnmount(){

        window.removeEventListener(
            "open-profile",
            this.openProfile
        );

    }

}

</script>

<style scoped>

.navbar{

    height:72px;

    border-radius:14px;

}

.search-box{

    width:420px;

}

.input-group-text{

    border-right:none;

}

.form-control{

    border-left:none;

}

.form-control:focus{

    box-shadow:none;

}

.profile-circle{

    width:45px;

    height:45px;

    border-radius:50%;

    background:#198754;

    color:white;

    display:flex;

    justify-content:center;

    align-items:center;

    font-weight:bold;

    font-size:16px;

    cursor:pointer;

    transition:.3s;

}

.profile-circle:hover{

    transform:scale(1.08);

    box-shadow:0 0 10px rgba(0,0,0,.2);

}

</style>