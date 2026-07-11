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

                    {{ staffName }}

                </div>

                <small class="text-muted">

                    {{ today }}

                </small>

            </div>

            <div class="profile-circle">

                {{ initials }}

            </div>

        </div>

    </div>

</nav>

</template>

<script>

export default{

    name:"StaffNavbar",

    props:{

        title:{

            type:String,

            default:"Dashboard"

        },

        placeholder:{

            type:String,

            default:"Search..."

        }

    },

    emits:[

        "search"

    ],

    data(){

        return{

            searchText:"",

            staffName:localStorage.getItem("name") || "Staff"

        }

    },

    computed:{

        initials(){

            return this.staffName

                .split(" ")

                .map(word=>word.charAt(0))

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

        }

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

}

</style>