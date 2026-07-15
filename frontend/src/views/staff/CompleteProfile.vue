<template>

<div class="container py-5">

    <div class="row justify-content-center">

        <div class="col-lg-7">

            <div class="card shadow-lg border-0">

                <div class="card-header bg-success text-white">

                    <h3 class="mb-0">

                        Complete Your Profile

                    </h3>

                    <small>

                        Please complete your profile before accessing the dashboard.

                    </small>

                </div>

                <div class="card-body">

                    <form @submit.prevent="saveProfile">

                        <div class="mb-3">

                            <label class="form-label">

                                Name

                            </label>

                            <input

                                class="form-control"

                                v-model="form.name"

                                readonly

                            >

                        </div>

                        <div class="mb-3">

                            <label class="form-label">

                                Email

                            </label>

                            <input

                                class="form-control"

                                v-model="form.email"

                                readonly

                            >

                        </div>

                    
                        <div class="mb-3">

                            <label class="form-label">

                                Phone Number

                            </label>

                            <input

                                class="form-control"

                                v-model="form.phone"

                                maxlength="10"

                                required

                            >

                        </div>

                        <div class="mb-3">

                            <label class="form-label">

                                Age

                            </label>

                            <input

                                type="number"

                                class="form-control"

                                v-model="form.age"

                                required

                            >

                        </div>

                        <div class="mb-3">

                            <label class="form-label">

                                Gender

                            </label>

                            <select

                                class="form-select"

                                v-model="form.gender"

                                required

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

                        <div class="mb-3">

                            <label class="form-label">

                                New Password

                            </label>

                            <input

                                type="password"

                                class="form-control"

                                v-model="form.password"

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

                                v-model="confirmPassword"

                                required

                            >

                        </div>

                        <div class="text-end">

                            <button

                                class="btn btn-success"

                                :disabled="loading"

                            >

                                {{ loading ? "Saving..." : "Complete Profile" }}

                            </button>

                        </div>

                    </form>

                </div>

            </div>

        </div>

    </div>

</div>

</template>

<script>


import {

    getMyProfile,

    completeProfile

} from "../../services/staff";

export default{

    name:"CompleteProfile",

    data(){

        return{

            loading:false,

            confirmPassword:"",

            form:{

                name:"",

                email:"",

                phone:"",

                age:null,

                gender:"",

                password:""

            }

        }

    },

    methods:{

        async loadProfile(){

            try{

                const response=await getMyProfile();

                const profile=response.data.profile;

                this.form.name=profile.name;

                this.form.email=profile.email;

                this.form.phone=profile.phone || "";

                this.form.age=profile.age;

                this.form.gender=profile.gender || "";

            }

            catch(error){

                console.error(error);

                alert("Unable to load profile.");

            }

        },

        async saveProfile(){

            if(this.form.password!==this.confirmPassword){

                alert("Passwords do not match.");

                return;

            }

            this.loading=true;

            try{

                await completeProfile({

                    phone:this.form.phone,

                    age:this.form.age,

                    gender:this.form.gender,

                    password:this.form.password

                });

                alert("Profile completed successfully.");

                this.$router.push("/staff/dashboard");

            }

            catch(error){

                console.error(error);

                alert(

                    error.response?.data?.message ||

                    "Unable to complete profile."

                );

            }

            finally{

                this.loading=false;

            }

        }

    },

    mounted(){

        this.loadProfile();

    }

}

</script>

<style scoped>

.card{

    border-radius:16px;

}

.card-header{

    padding:20px;

}

.form-label{

    font-weight:600;

}

.btn{

    border-radius:10px;

    padding:10px 20px;

}

</style>