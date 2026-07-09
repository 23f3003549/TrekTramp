<template>
    <div class="modal-overlay">
        <div class="modal-card">
            <div class="modal-header">
                <h3>{{ isEdit ? "Update Trek" : "Create New Trek" }}</h3>
            </div>


            <div class="modal-body">
                <div class="row">
                    <div class="col-md-6 mb-3">
                        <label class="form-label"> Trek Name </label>
                        <input type="text" class="form-control" v-model="form.trek_name" placeholder="Enter Trek Name">
                    </div>
    
                    <div class="col-md-6 mb-3">
                        <label class="form-label"> Location </label>
                        <input type="text" class="form-control" v-model="form.location" placeholder="Enter Location">
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6 mb-3">
                        <label class="form-label"> Difficulty </label>
                        <select class="form-select" v-model="form.difficulty">
                            <option value="" disabled> Select Difficulty</option>
                            <option value="easy">Easy</option>
                            <option value="medium">Medium</option>
                            <option value="hard">Hard</option>
                        </select>
                    </div>
    
                    <div class="col-md-6 mb-3">
                        <label class="form-label fw-semibold"> Maximum Slots </label>
                        <input type="number" class="form-control" placeholder="Enter Maximum Slots" v-model="form.max_slots" min="1">
                
                    </div>
                </div>
    
                <div class="row">
                    <div class="col-md-6 mb-3">
                        <label class="form-label fw-semibold"> Minium Age</label>
                        <input type="number" class="form-control" placeholder="Minimum age" v-model="form.min_age" min="5">
                    </div>
    
                    <div class="col-md-6 mb-3">
                        <label class="form-label fw-semibold"> Maxximum Age</label>
                        <input type="number" class="form-control" placeholder="Maximum age" v-model="form.max_age" min="5">
                    </div>
                </div>
    
                <div class="row">
    
                    <div class="col-md-6 mb-3">
                
                        <label class="form-label fw-semibold"> Price (₹) </label>
                        <input type="number" class="form-control" placeholder="Enter Trek Price" v-model="form.price" min="0" >
                
                    </div>
    
                </div>
    
                <div class ="row">
    
                    <div class="col-md-6 mb-3">
                
                        <label class="form-label fw-semibold">
                            Start Date
                        </label>
                
                        <input
                            type="date"
                            class="form-control"
                            v-model="form.start_date"
                        >
                
                    </div>
                
                    <div class="col-md-6 mb-3">
                
                        <label class="form-label fw-semibold">
                            End Date
                        </label>
                
                        <input
                            type="date"
                            class="form-control"
                            v-model="form.end_date"
                        >
                
                    </div>
    
                </div>
    
                <div class="mb-3">
    
                    <label class="form-label fw-semibold">
                
                        Duration
                
                    </label>
                
                    <input
                        type="text"
                        class="form-control"
                        :value="durationText"
                        readonly
                    >
    
                </div>
    
                <div class="mb-3">
    
                    <label class="form-label fw-semibold">
                
                        Description
                
                    </label>
                
                    <textarea
                        rows="4"
                        class="form-control"
                        placeholder="Enter Trek Description..."
                        v-model="form.description"
                    ></textarea>
    
                </div>
            </div>


            <div class="modal-footer">
                <button class="btn btn-secondary" @click="closeModal">
                    Cancel
    
                </button>
    
                <button class="btn btn-success" @click="submitForm">
                    {{ isEdit ? "Update Trek" : "Create Trek" }}
                </button>
    
            </div>
        </div>    
    </div>
</template>

<script>
import { createTrek } from '../../services/trek';
import { updateTrek } from '../../services/trek';

export default{
    name: "TrekModalForm",
    props:{
        trek:{
            type:Object,
            default: null
        }

    },
    data(){
        return {
            form:{
                id:null,
                trek_name: "",
                location: "",
                difficulty : "",
                min_age:null,
                max_age:null,
                max_slots:null,
                price:null,
                start_date:"",
                end_date:"",
                description:""
            }

        }
    },
    methods : {
        closeModal(){
            this.$emit("close")
        },

        async submitForm(){

            try{
        
                if(this.isEdit){
           
                    await updateTrek(
                        this.form.id,
                        this.form
                    );
           
                }
           
                else{
           
                    await createTrek(this.form);
           
                }
           
                this.$emit("trekSaved");
           
            }
           
            catch(error){
           
                console.error(error);
           
                alert(
                    error.response?.data?.message ||
                    "Operation failed."
                );
           
            }

        }

        
    },

    computed:{
        durationText(){
            if(!this.form.start_date || !this.form.end_date){
                return "";
            }

            const start = new Date(this.form.start_date);
            const end = new Date(this.form.end_date);
            const difference = end-start;
            const days = Math.floor(difference/(1000*60*60*24))+1
            return `${days} Day${days>1?"s":""}`;

        },
        isEdit(){
            return this.trek !== null;
        }

    },

    watch:{
    
        trek:{
    
            immediate:true,
    
            handler(newValue){
    
                if(newValue){
    
                    this.form = {
    
                        ...newValue,
    
                        start_date:newValue.start_date.substring(0,10),
    
                        end_date:newValue.end_date.substring(0,10)
    
                    };
    
                }
    
                else{
    
                    this.form = {
    
                        id:null,
    
                        trek_name:"",
    
                        location:"",
    
                        difficulty:"",
    
                        min_age:null,
    
                        max_age:null,
    
                        max_slots:null,
    
                        price:null,
    
                        start_date:"",
    
                        end_date:"",
    
                        description:""
    
                    };
    
                }
    
            }
    
        }
    
    },    
    
    mounted(){
        document.body.style.overflow = "hidden"
    },

    beforeUnmount(){
        document.body.style.overflow = "";
    }
}

</script>

<style scoped>
.modal-overlay{

    position:fixed;

    inset:0;

    background:rgba(0,0,0,0.6);

    display:flex;

    justify-content:center;

    align-items:center;

    z-index:999;

}

.modal-card{

    width:850px;

    max-width:90%;

    max-height:90vh;

    background:white;

    border-radius:18px;
    display:flex;
    flex-direction:column;


}

.modal-header{

    background:#198754;
    color:white;
    padding:18px 24px;
    border-bottom:1px solid #e9ecef;

}

.modal-body{

    padding:25px;
    overflow-y:auto;
    flex:1;
    min-height:0;

}

.modal-footer{

    padding:20px 25px;

    display:flex;

    justify-content:flex-end;

    gap:10px;

    border-top:1px solid #e9ecef;

}

.form-label{
    font-weight:600;
}

.form-control,
.form-select{
    border-radius:10px;
}

.btn{
    border-radius:10px;
}
</style>