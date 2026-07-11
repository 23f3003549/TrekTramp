<template>

    <div
        class="offcanvas offcanvas-end"
        tabindex="-1"
        ref="offcanvasElement"
    >

        <div class="offcanvas-header bg-success text-white">

            <h4 class="offcanvas-title">

                Assign Staff

            </h4>

            <button
                class="btn-close btn-close-white"
                @click="closePanel"
            ></button>

        </div>

        <div class="offcanvas-body">

            <div
                v-if="loading"
                class="text-center mt-5"
            >

                <div class="spinner-border text-success"></div>

                <p class="mt-3">

                    Loading available staff...

                </p>

            </div>

            <div v-else>

                <div
                    v-if="staffs.length===0"
                    class="alert alert-warning"
                >

                    No available staff found.

                </div>

                <form
                    v-else
                    @submit.prevent="assignSelectedStaff"
                >

                    <div class="mb-4">

                        <label class="form-label fw-semibold">

                            Select Staff

                        </label>

                        <select
                            class="form-select"
                            v-model="selectedStaff"
                            required
                        >

                            <option
                                disabled
                                value=""
                            >

                                Choose Staff

                            </option>

                            <option
                                v-for="staff in staffs"
                                :key="staff.id"
                                :value="staff.id"
                            >

                                {{ staff.name }} ({{ staff.email }})

                            </option>

                        </select>

                    </div>

                    <div class="d-flex justify-content-end">

                        <button
                            type="button"
                            class="btn btn-secondary me-2"
                            @click="closePanel"
                        >

                            Cancel

                        </button>

                        <button
                            class="btn btn-success"
                            type="submit"
                        >

                            Assign Staff

                        </button>

                    </div>

                </form>

            </div>

        </div>

    </div>

</template>

<script>

import * as bootstrap from "bootstrap";

import {

    getAvailableStaff,

    assignStaff

} from "../../services/staff";

export default{

    name:"AssignStaffPanel",

    props:{

        trekId:{

            type:Number,

            required:true

        }

    },

    emits:[

        "close",

        "assigned"

    ],

    data(){

        return{

            offcanvas:null,

            staffs:[],

            selectedStaff:"",

            loading:false

        }

    },

    methods:{

        async loadStaff(){

            this.loading=true;

            try{

                const response=await getAvailableStaff();

                this.staffs=response.data.staffs;

            }

            catch(error){

                console.error(error);

                alert(

                    error.response?.data?.message ||

                    "Unable to load available staff."

                );

            }

            finally{

                this.loading=false;

            }

        },

        async assignSelectedStaff(){

            if(!this.selectedStaff){

                alert("Please select a staff.");

                return;

            }

            try{

                await assignStaff({

                    trek_id:this.trekId,

                    staff_id:this.selectedStaff

                });

                alert("Staff assigned successfully.");

                this.$emit("assigned");

                this.closePanel();

            }

            catch(error){

                console.error(error);

                alert(

                    error.response?.data?.message ||

                    "Unable to assign staff."

                );

            }

        },

        closePanel(){

            this.offcanvas.hide();

        }

    },

    async mounted(){

        this.offcanvas=new bootstrap.Offcanvas(

            this.$refs.offcanvasElement

        );

        this.offcanvas.show();

        await this.loadStaff();

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

    width:450px;

}

.form-label{

    font-weight:600;

}

</style>