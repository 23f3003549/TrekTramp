<template>

    <div
        class="offcanvas offcanvas-end"
        tabindex="-1"
        ref="offcanvasElement"
    >

        <div class="offcanvas-header bg-success text-white">

            <h4 class="offcanvas-title">

                {{
                    mode==="view"
                    ? "My Profile"
                    : mode==="edit"
                    ? "Update Profile"
                    : "Change Password"
                }}

            </h4>

            <button
                class="btn-close btn-close-white"
                @click="closePanel"
            ></button>

        </div>


        <div class="offcanvas-body">

            <div
                v-if="loading"
                class="text-center py-5"
            >

                <div class="spinner-border text-success"></div>

            </div>

            
            <div
                v-else-if="mode==='view'"
            >

                <div class="text-center mb-4">

                    <div class="profile-avatar">

                        {{ initials }}

                    </div>

                    <h4 class="mt-3 mb-1">

                        {{ profile.name }}

                    </h4>

                    <p class="text-muted mb-2">

                        {{ profile.email }}

                    </p>

                    <span class="badge bg-success text-uppercase">

                        {{ profile.role }}

                    </span>

                </div>

                <div class="card shadow-sm mb-4">

                    <div class="card-body">

                        <p>

                            <strong>Name</strong>

                        </p>

                        <p class="text-muted">

                            {{ profile.name }}

                        </p>

                        <hr>

                        <p>

                            <strong>Email</strong>

                        </p>

                        <p class="text-muted">

                            {{ profile.email }}

                        </p>

                        <hr>

                        <p>

                            <strong>Role</strong>

                        </p>

                        <p class="text-muted text-uppercase">

                            {{ profile.role }}

                        </p>

                    </div>

                </div>

                <button
                    class="btn btn-success w-100 mb-3"
                    @click="mode='edit'"
                >

                    Edit Profile

                </button>

                <button
                    class="btn btn-outline-dark w-100"
                    @click="mode='password'"
                >

                    Change Password

                </button>

            </div>

            <div
                v-else-if="mode==='edit'"
            >

                <form @submit.prevent="saveProfile">

                    <div class="mb-3">

                        <label class="form-label">

                            Name

                        </label>

                        <input
                            class="form-control"
                            v-model="form.name"
                            required
                        >

                    </div>

                    <div class="mb-4">

                        <label class="form-label">

                            Email

                        </label>

                        <input
                            type="email"
                            class="form-control"
                            v-model="form.email"
                            required
                        >

                    </div>

                    <div class="d-flex justify-content-end">

                        <button
                            type="button"
                            class="btn btn-secondary me-2"
                            @click="mode='view'"
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

            <div
                v-else
            >

                <form @submit.prevent="updatePassword">

                    <div class="mb-3">

                        <label class="form-label">

                            Current Password

                        </label>

                        <input
                            type="password"
                            class="form-control"
                            v-model="password.current_password"
                            required
                        >

                    </div>

                    <div class="mb-3">

                        <label class="form-label">

                            New Password

                        </label>

                        <input
                            type="password"
                            class="form-control"
                            v-model="password.new_password"
                            required
                        >

                    </div>

                    <div class="mb-4">

                        <label class="form-label">

                            Confirm Password

                        </label>

                        <input
                            type="password"
                            class="form-control"
                            v-model="password.confirm_password"
                            required
                        >

                    </div>

                    <div class="d-flex justify-content-end">

                        <button
                            type="button"
                            class="btn btn-secondary me-2"
                            @click="mode='view'"
                        >

                            Cancel

                        </button>

                        <button
                            class="btn btn-success"
                            :disabled="saving"
                        >

                            {{ saving ? "Updating..." : "Update Password" }}

                        </button>

                    </div>

                </form>

            </div>

        </div>

    </div>

</template>

<script>

import * as bootstrap from "bootstrap";

import{

    getAdminProfile,

    updateAdminProfile,

    changeAdminPassword

}from "../../services/admin";

export default{

    name:"AdminProfilePanel",

    emits:[

        "close"

    ],

    data(){

        return{

            loading:false,

            saving:false,

            mode:"view",

            offcanvas:null,

            profile:{},

            form:{

                name:"",

                email:""

            },

            password:{

                current_password:"",

                new_password:"",

                confirm_password:""

            }

        }

    },

    computed:{

        initials(){

            if(!this.profile.name){

                return "A";

            }

            return this.profile.name

                .split(" ")

                .map(

                    word=>word.charAt(0)

                )

                .join("")

                .substring(0,2)

                .toUpperCase();

        }

    },

    methods:{

        async loadProfile(){

            this.loading = true;

            try{

                const response = await getAdminProfile();

                this.profile = response.data.admin;

                this.form = {

                    name:this.profile.name,

                    email:this.profile.email

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

                this.loading = false;

            }

        },

        async saveProfile(){

            this.saving = true;

            try{

                const response = await updateAdminProfile(

                    this.form

                );

                alert(

                    response.data.message

                );

                await this.loadProfile();

                this.mode = "view";

            }

            catch(error){

                console.error(error);

                alert(

                    error.response?.data?.message ||

                    "Unable to update profile."

                );

            }

            finally{

                this.saving = false;

            }

        },

        async updatePassword(){

            this.saving = true;

            try{

                const response = await changeAdminPassword(

                    this.password

                );

                alert(

                    response.data.message

                );

                this.password = {

                    current_password:"",

                    new_password:"",

                    confirm_password:""

                };

                this.mode = "view";

            }

            catch(error){

                console.error(error);

                alert(

                    error.response?.data?.message ||

                    "Unable to update password."

                );

            }

            finally{

                this.saving = false;

            }

        },

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

            }

        );

    }

}

</script>

<style scoped>

.offcanvas{

    width:430px;

}

.offcanvas-header{

    border-bottom:1px solid #dee2e6;

}

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

    box-shadow:0 6px 18px rgba(25,135,84,.25);

}

.card{

    border:none;

    border-radius:15px;

}

.card-body{

    padding:22px;

}

.card-body p{

    margin-bottom:6px;

}

.card-body strong{

    color:#495057;

}

.form-label{

    font-weight:600;

    color:#495057;

}

.form-control{

    border-radius:10px;

    padding:10px 14px;

}

.form-control:focus{

    border-color:#198754;

    box-shadow:0 0 0 .15rem rgba(25,135,84,.2);

}

.btn{

    border-radius:10px;

    padding:9px 18px;

    font-weight:500;

}

.badge{

    font-size:13px;

    padding:7px 16px;

    border-radius:20px;

}

h5{

    color:#198754;

    font-weight:700;

}

hr{

    opacity:.15;

}

.spinner-border{

    width:3rem;

    height:3rem;

}

@media(max-width:576px){

    .offcanvas{

        width:100%;

    }

}

</style>