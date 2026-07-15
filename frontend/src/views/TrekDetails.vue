<template>
    <div class="card shadow-sm mt-4">
    
        <div class="card-header">
    
            <h5>Actions</h5>
    
        </div>
    
        <div class="card-body">
    
            <div v-if="role==='admin'">
                <div class="mb-3">

                    <label class="form-label fw-semibold">
            
                        Assign Staff
            
                    </label>

                    <select
                        class="form-select"
                        v-model="selectedStaff"
                    >
            
                        <option
                            value=""
                            disabled
                        >
            
                            Select Staff
            
                        </option>
            
                        <option
                            v-for="staff in availableStaff"
                            :key="staff.id"
                            :value="staff.id"
                        >
            
                            {{ staff.name }}
            
                        </option>
            
                    </select>

                </div>

                <button
                    class="btn btn-success"
                    @click="assignSelectedStaff"
                >
            
                    Assign Staff
                </button>
                
            </div>
    
            <div v-else-if="role==='staff'">

       
            
                <div v-if="trekStatus==='open'">
            
                    <div class="row mb-3">
            
                        <div class="col-md-6">
            
                            <label class="form-label">
            
                                Available Slots
            
                            </label>
            
                            <input
            
                                type="number"
            
                                class="form-control"
            
                                v-model="availableSlots"
            
                            >
            
                        </div>
            
                        <div class="col-md-6 d-flex align-items-end">
            
                            <button
            
                                class="btn btn-warning"
            
                                @click="updateSlots"
            
                            >
            
                                Update Slots
            
                            </button>
            
                        </div>
            
                    </div>
            
                    <button
            
                        class="btn btn-primary"
            
                        @click="changeStatus('started')"
            
                    >
            
                        Start Trek
            
                    </button>
            
                    <button
            
                        class="btn btn-danger ms-2"
            
                        @click="changeStatus('cancelled')"
            
                    >
            
                        Cancel Trek
            
                    </button>
            
                </div>
            
        
            
                <div v-else-if="trekStatus==='started'">
            
                    <button
            
                        class="btn btn-success"
            
                        @click="changeStatus('completed')"
            
                    >
            
                        Complete Trek
            
                    </button>
            
                    <button
            
                        class="btn btn-danger ms-2"
            
                        @click="changeStatus('cancelled')"
            
                    >
            
                        Cancel Trek
            
                    </button>
            
                </div>
            
                <div v-else>
            
                    <div class="alert alert-secondary mb-0">
            
                        This trek is {{ trekStatus }}.
                        No further actions are available.
            
                    </div>
            
                </div>
            
            </div>
                
            <div v-else>
    
                <button class="btn btn-success">
                    Book Trek
                </button>
    
            </div>
    
        </div>

    </div>
</template>

<script>

import {

    getAvailableStaff,

    assignStaff

} from "../services/staff";



export default{

    props:{

        trekId:Number,
        role:String,
        trekStatus:String,
         currentSlots:Number

    },

    data(){

        return{

            availableStaff:[],
            selectedStaff:null,
            availableSlots:this.currentSlots


        }

    },

    methods:{

        async loadAvailableStaff(){

            try{

                const response = await getAvailableStaff();

                this.availableStaff = response.data.staffs;

            }

            catch(error){

                console.error(error);

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

                this.loadAvailableStaff();

                this.$emit("refresh");

            }

            catch(error){

                console.error(error);

                alert(

                    error.response?.data?.message ||

                    "Unable to assign staff."

                );

            }

        }

    },

    mounted(){

        if(this.role==="admin"){

            this.loadAvailableStaff();

        }

    }

}

</script>