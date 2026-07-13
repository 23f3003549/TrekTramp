<template>

<div
    class="offcanvas offcanvas-end"
    tabindex="-1"
    ref="offcanvasElement"
>

    <!-- HEADER -->

    <div class="offcanvas-header bg-success text-white">

        <h4 class="offcanvas-title">

            {{ editMode ? "Update Profile" : "My Profile" }}

        </h4>

        <button
            class="btn-close btn-close-white"
            @click="closePanel"
        ></button>

    </div>

    <!-- BODY -->

    <div class="offcanvas-body">

        <!-- LOADER -->

        <div
            v-if="loading"
            class="text-center py-5"
        >

            <div class="spinner-border text-success"></div>

        </div>

        <!-- PROFILE -->

        <div v-else>

            <!-- ================= VIEW MODE ================= -->

            <div v-if="!editMode">

                <div class="text-center mb-4">

                    <div class="profile-avatar">

                        {{ initials }}

                    </div>

                    <h4 class="mt-3 mb-1">

                        {{ profile.name }}

                    </h4>

                    <span class="badge bg-success text-uppercase">

                        {{ profile.role }}

                    </span>

                </div>

                <div class="card shadow-sm mb-3">

                    <div class="card-body">

                        <p>

                            <strong>Email</strong>

                        </p>

                        <p class="text-muted">

                            {{ profile.email }}

                        </p>

                        <hr>

                        <p>

                            <strong>Phone</strong>

                        </p>

                        <p class="text-muted">

                            {{ profile.phone || "-" }}

                        </p>

                        <hr>

                        <p>

                            <strong>Age</strong>

                        </p>

                        <p class="text-muted">

                            {{ profile.age || "-" }}

                        </p>

                        <hr>

                        <p>

                            <strong>Gender</strong>

                        </p>

                        <p class="text-muted">

                            {{ profile.gender || "-" }}

                        </p>

                    </div>

                </div>

                <button
                    class="btn btn-success w-100"
                    @click="enableEdit"
                >

                    Update Profile

                </button>

            </div>

            <!-- ================= EDIT MODE ================= -->

            <div v-else>

                <form @submit.prevent="saveProfile">

                    <!-- NAME -->

                    <div class="mb-3">

                        <label class="form-label">

                            Name

                        </label>

                        <input

                            class="form-control"

                            v-model="form.name"

                            :readonly="profile.role !== 'trekker'"

                        >

                    </div>

                    <!-- EMAIL -->

                    <div class="mb-3">

                        <label class="form-label">

                            Email

                        </label>

                        <input

                            type="email"

                            class="form-control"

                            v-model="form.email"

                            :readonly="profile.role !== 'trekker'"

                        >

                    </div>

                    <!-- PHONE -->

                    <div class="mb-3">

                        <label class="form-label">

                            Phone Number

                        </label>

                        <input

                            class="form-control"

                            maxlength="10"

                            v-model="form.phone"

                        >

                    </div>

                    <!-- AGE -->

                    <div class="mb-3">

                        <label class="form-label">

                            Age

                        </label>

                        <input

                            type="number"

                            class="form-control"

                            v-model="form.age"

                        >

                    </div>

                    <!-- GENDER -->

                    <div class="mb-4">

                        <label class="form-label">

                            Gender

                        </label>

                        <select

                            class="form-select"

                            v-model="form.gender"

                        >

                            <option value="">

                                Select Gender

                            </option>

                            <option value="Male">

                                Male

                            </option>

                            <option value="Female">

                                Female

                            </option>

                            <option value="Other">

                                Other

                            </option>

                        </select>

                    </div>

                    <div class="d-flex justify-content-end">

                        <button
                            type="button"
                            class="btn btn-secondary me-2"
                            @click="cancelEdit"
                        >

                            Cancel

                        </button>

                        <button
                            class="btn btn-success"
                            :disabled="saving"
                        >

                            {{ saving ? "Saving..." : "Save Changes" }}

                        </button>

                    </div>

                </form>

            </div>

        </div>

    </div>

</div>

</template>

<script>

import * as bootstrap from "bootstrap";

import {

    getProfile,

    updateProfile

} from "../../services/profile";

export default{

    name:"ProfilePanel",

    emits:[

        "close"

    ],

    data(){

        return{

            loading:false,

            saving:false,

            editMode:false,

            offcanvas:null,

            profile:{},

            form:{

                name:"",

                email:"",

                phone:"",

                age:null,

                gender:""

            }

        }

    },

    computed:{

        initials(){

            if(!this.profile.name){

                return "";

            }

            return this.profile.name

                .split(" ")

                .map(word=>word.charAt(0))

                .join("")

                .substring(0,2)

                .toUpperCase();

        }

    },

    methods:{

        // ---------------- Load Profile ----------------

        async loadProfile(){

            this.loading=true;

            try{

                const response = await getProfile();

                this.profile = response.data.profile;

                this.form = {

                    name:this.profile.name,

                    email:this.profile.email,

                    phone:this.profile.phone || "",

                    age:this.profile.age,

                    gender:this.profile.gender || ""

                };

            }

            catch(error){

                console.error(error);

                alert(

                    error.response?.data?.message ||

                    "Unable to load profile."

                );

            }

            finally{

                this.loading=false;

            }

        },

        // ---------------- Enable Edit ----------------

        enableEdit(){

            this.editMode=true;

        },

        // ---------------- Cancel Edit ----------------

        cancelEdit(){

            this.editMode=false;

            this.form = {

                name:this.profile.name,

                email:this.profile.email,

                phone:this.profile.phone || "",

                age:this.profile.age,

                gender:this.profile.gender || ""

            };

        },

        // ---------------- Save Profile ----------------

        async saveProfile(){

            this.saving=true;

            try{

                const response = await updateProfile(
            
                    this.form
            
                );
            
                // Update localStorage if the name changed
                if(response.data.profile){
            
                    localStorage.setItem(
            
                        "name",
            
                        response.data.profile.name
            
                    );
            
                }
            
                alert(
            
                    response.data.message
            
                );
            
                this.editMode = false;
            // --------------------------------------------------------------------
                await this.loadProfile();
                this.offcanvas.hide()
               
            
            }

            catch(error){

                console.error(error);

                alert(

                    error.response?.data?.message ||

                    "Unable to update profile."

                );

            }

            finally{

                this.saving=false;

            }

        },

        // ---------------- Close Panel ----------------

        closePanel(){

            this.offcanvas.hide();

        }

    },

    async mounted(){

        await this.loadProfile();

        this.offcanvas = new bootstrap.Offcanvas(

            this.$refs.offcanvasElement

        );

        this.offcanvas.show();

        this.$refs.offcanvasElement.addEventListener(

            "hidden.bs.offcanvas",

            ()=>{

                this.$emit("close");
                window.dispatchEvent(
                    new CustomEvent(
                        "Profile-updated"

                    )
                );

            }

        );

    }

}

</script>

<style scoped>

.offcanvas{

    width:430px;

}


/* ================= HEADER ================= */

.offcanvas-header{

    border-bottom:1px solid #dee2e6;

}


/* ================= AVATAR ================= */

.profile-avatar{

    width:90px;

    height:90px;

    margin:auto;

    border-radius:50%;

    background:#198754;

    color:white;

    display:flex;

    justify-content:center;

    align-items:center;

    font-size:32px;

    font-weight:bold;

    letter-spacing:1px;

}


/* ================= CARD ================= */

.card{

    border:none;

    border-radius:15px;

}


.card-body p{

    margin-bottom:6px;

}


/* ================= LABELS ================= */

.form-label{

    font-weight:600;

    color:#495057;

}


/* ================= INPUTS ================= */

.form-control,

.form-select{

    border-radius:10px;

}


.form-control:focus,

.form-select:focus{

    border-color:#198754;

    box-shadow:0 0 0 .15rem rgba(25,135,84,.2);

}


/* ================= BUTTONS ================= */

.btn{

    border-radius:10px;

    padding:9px 18px;

}


/* ================= BADGE ================= */

.badge{

    font-size:13px;

    padding:7px 14px;

    border-radius:20px;

}


/* ================= MOBILE ================= */

@media(max-width:576px){

    .offcanvas{

        width:100%;

    }

}

</style>