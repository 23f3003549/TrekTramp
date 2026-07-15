<template>
    <div
        class="offcanvas offcanvas-end"
        tabindex="-1"
        ref="offcanvasElement"
    >

        <div class="offcanvas-header bg-success text-white">

            <h4 class="offcanvas-title">

                {{ isEdit ? "Update Staff" : "Create Staff" }}

            </h4>

            <button
                class="btn-close btn-close-white"
                @click="closePanel"
            ></button>

        </div>

        <div class="offcanvas-body">

            <form @submit.prevent="submitForm">

                <div class="mb-3">

                    <label class="form-label fw-semibold">

                        Staff Name

                    </label>

                    <input
                        type="text"
                        class="form-control"
                        placeholder="Enter Staff Name"
                        v-model="form.name"
                        required
                    >

                </div>

                <div class="mb-4">

                    <label class="form-label fw-semibold">

                        Email Address

                    </label>

                    <input
                        type="email"
                        class="form-control"
                        placeholder="Enter Email Address"
                        v-model="form.email"
                        required
                    >

                    <small class="text-muted">

                        A temporary password will be generated automatically
                        and sent to this email.

                    </small>

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
                        type="submit"
                        class="btn btn-success"
                    >

                        {{ isEdit ? "Update Staff" : "Create Staff" }}

                    </button>

                </div>

            </form>

        </div>

    </div>
</template>

<script>
import * as bootstrap from "bootstrap";
import {
    createStaff,
    updateStaff
} from "../../services/staff";

export default{

    name:"StaffFormPanel",

    props:{

        staff:{
            type:Object,
            default:null
        }

    },

    emits:["close","staffSaved"],

    data(){

        return{

            offcanvas:null,

            form:{

                id:null,

                name:"",

                email:""

            }

        }

    },

    computed:{

        isEdit(){

            return this.staff!==null;

        }

    },

    watch:{

        staff:{

            immediate:true,

            handler(newStaff){

                if(newStaff){

                    this.form={

                        id:newStaff.id,

                        name:newStaff.name,

                        email:newStaff.email

                    };

                }

                else{

                    this.form={

                        id:null,

                        name:"",

                        email:""

                    };

                }

            }

        }

    },

    methods:{

        closePanel(){

            this.offcanvas.hide();

        },

        async submitForm(){

            try{

                if(this.isEdit){

                    await updateStaff(

                        this.form.id,

                        this.form

                    );

                    alert("Staff updated successfully.");

                }

                else{

                    await createStaff(this.form);

                    alert(
                        "Staff created successfully.\n\nTemporary password has been generated and emailed."
                    );

                }

                this.$emit("staffSaved");

                this.closePanel();

            }

            catch(error){

                console.error(error);

                alert(

                    error.response?.data?.message ||

                    "Unable to save staff."

                );

            }

        }

    },

    mounted(){

        this.offcanvas=new bootstrap.Offcanvas(

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

    width:500px;

}

.offcanvas-body{

    background:#f8f9fa;

}

.form-control{

    border-radius:10px;

}

.btn{

    border-radius:10px;

}

.form-label{

    font-weight:600;

}

</style>