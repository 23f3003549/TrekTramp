<template>

    <div class="card shadow-sm dashboard-card">

        <div class="card-body">

            <h6 class="card-title">

                {{ title }}

            </h6>

            <h2 class="card-value">

                {{ count }}

            </h2>

        </div>

    </div>

</template>

<script>

export default{

    name:"DashboardCard",

    props:{

        title:{
            type:String,
            required : true

        },
        count:{
            type : Number,
            required : true
        }


    }

}

</script>

<style scoped>

.dashboard-card{

    background:rgba(255,255,255,0.85);

    backdrop-filter:blur(10px);

    -webkit-backdrop-filter:blur(10px);

    border:1px solid rgba(255,255,255,0.5);

    border-top:4px solid #198754;

    border-radius:16px;

    box-shadow:0 8px 20px rgba(0,0,0,0.08);

    transition:all .3s ease;

}

.dashboard-card:hover{

    transform:translateY(-5px);
    box-shadow:0 14px 30px rgba(25,135,84,0.15);

}

.card-title{

    color:#6c757d;

    font-weight:600;

}

.card-value{

    color:#198754;

    font-size:2rem;

    font-weight:bold;

    margin-top:10px;

}

</style>