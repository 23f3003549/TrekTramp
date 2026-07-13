<template>

    <div
        class="card export-card shadow-sm h-100"
    >

        <div class="card-body text-center">

            <div
                class="icon-circle mx-auto mb-3"
                :class="'bg-'+color"
            >

                <i
                    class="bi fs-2 text-white"
                    :class="icon"
                ></i>

            </div>

            <h5 class="fw-bold">

                {{ title }}

            </h5>

            <p class="text-muted small">

                {{ description }}

            </p>

            <button
                class="btn btn-success"
                @click="$emit('download')"
            >

                <i class="bi bi-download me-2"></i>

                Download CSV

            </button>

        </div>

    </div>

</template>

<script>

export default{

    name:"ExportCard",

    props:{

        title:{

            type:String,

            required:true

        },

        description:{

            type:String,

            default:""

        },

        icon:{

            type:String,

            required:true

        },

        color:{

            type:String,

            default:"success"

        }

    },

    emits:[

        "download"

    ]

}

</script>

<style scoped>

.export-card{

    border:none;

    border-radius:16px;

    transition:.25s;

}

.export-card:hover{

    transform:translateY(-5px);

    box-shadow:0 10px 25px rgba(0,0,0,.12);

}

.icon-circle{

    width:70px;

    height:70px;

    border-radius:50%;

    display:flex;

    align-items:center;

    justify-content:center;

}

.btn{

    border-radius:10px;

}

</style>