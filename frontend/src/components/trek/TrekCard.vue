<template>

<div class="card trek-card shadow-sm h-100">


    <img

        :src="getImage()"
    
        class="card-img-top"
    
        :alt="trek.trek_name"

    />

    <div class="card-body d-flex flex-column">

        <h5 class="fw-bold">

            {{ trek.trek_name }}

        </h5>

        <p class="text-muted mb-2">

            <i class="bi bi-geo-alt-fill"></i>

            {{ trek.location }}

        </p>

        <div class="mb-3">

            <span
                class="badge bg-success me-2"
            >

                {{ trek.difficulty }}

            </span>

            <span
                class="badge bg-primary"
            >

                {{ trek.duration_days }} Days

            </span>

        </div>

        <div class="mb-2">

            <strong>

                ₹ {{ trek.price }}

            </strong>

        </div>

        <div class="mb-3 text-muted">

            Slots Left

            <strong>

                {{ trek.available_slots }}

            </strong>

            /

            {{ trek.max_slots }}

        </div>

        <button

            class="btn btn-success mt-auto"

            @click="viewDetails"

        >

            View Details

        </button>

    </div>

</div>

</template>

<script>

export default{

    name:"TrekCard",

    props:{

        trek:{

            type:Object,

            required:true

        }

    },

    methods:{

        getImage(){
    
            switch(this.trek.difficulty.toLowerCase()){
    
                case "easy":
    
                    return "/image/treks/easy.jpg";
    
                case "medium":
    
                    return "/image/treks/medium.jpg";
                case "hard":
    
                    return "/image/treks/hard.jpg";
    
                default:
    
                    return "/image/treks/hard.jpg";
    
            }
    
        },

    viewDetails(){

        this.$emit(

            "view",

            this.trek.id

        );

    }

    }    

}

</script>

<style scoped>

.trek-card{

    border:none;

    border-radius:18px;

    transition:.3s;

}

.trek-card:hover{

    transform:translateY(-6px);

}

.card-img-top{

    height:220px;

    object-fit:cover;

}

.badge{

    font-size:13px;

}

button{

    border-radius:10px;

}

</style>