<template>

    <div class="card summary-card shadow-sm">

        <div class="card-body">

            <div class="d-flex justify-content-between align-items-center">

                <!-- Left -->

                <div>

                    <h6 class="text-muted mb-2">

                        {{ title }}

                    </h6>

                    <h2 class="fw-bold mb-0">

                        {{ value }}

                    </h2>

                </div>

                <!-- Right -->

                <div
                    class="icon-circle"
                    :class="'bg-'+color"
                >

                    <i
                        class="bi fs-3 text-white"
                        :class="icon"
                    ></i>

                </div>

            </div>

        </div>

    </div>

</template>

<script>

export default{

    name:"SummaryCard",

    props:{

        title:{

            type:String,

            required:true

        },

        value:{

            type:[

                String,

                Number

            ],

            required:true

        },

        icon:{

            type:String,

            required:true

        },

        color:{

            type:String,

            default:"success"

        }

    }

}

</script>

<style scoped>

.summary-card{

    border:none;

    border-radius:16px;

    transition:.25s;

    cursor:default;

}

.summary-card:hover{

    transform:translateY(-4px);

    box-shadow:0 10px 25px rgba(0,0,0,.12);

}

.icon-circle{

    width:65px;

    height:65px;

    border-radius:50%;

    display:flex;

    align-items:center;

    justify-content:center;

}

h6{

    font-size:.95rem;

    font-weight:600;

}

h2{

    color:#212529;

}

</style>