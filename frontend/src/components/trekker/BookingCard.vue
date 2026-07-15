<template>

<div class="card booking-card shadow-sm h-100">

    <img
    :src="getImage()"

        class="card-img-top"

        :alt="booking.trek_name">

    <div class="card-body d-flex flex-column">

        <div class="d-flex justify-content-between align-items-start mb-2">

            <div>

                <h5 class="fw-bold mb-1">

                    {{ booking.trek_name }}

                </h5>

                <p class="text-muted mb-0">

                    <i class="bi bi-geo-alt-fill"></i>

                    {{ booking.location }}

                </p>

            </div>

            <span

                class="badge"

                :class="statusClass"

            >

                {{ booking.status }}

            </span>

        </div>

        <hr>

        <div class="d-flex justify-content-between mb-3">

            <span class="badge bg-dark">

                {{ booking.difficulty }}

            </span>

            <span class="badge bg-primary">

                {{ booking.duration_days }} Days

            </span>

        </div>

        <div class="info-row">

            <span>

                <i class="bi bi-calendar-event"></i>

                Trek Dates

            </span>

            <span>

                {{ booking.start_date }}

                -

                {{ booking.end_date }}

            </span>

        </div>

        <div class="info-row">

            <span>

                <i class="bi bi-journal-check"></i>

                Booked On

            </span>

            <span>

                {{ booking.booking_date }}

            </span>

        </div>

        <div class="info-row">

            <span>

                <i class="bi bi-cash-stack"></i>

                Amount

            </span>

            <strong>

                ₹ {{ booking.total_amount }}

            </strong>

        </div>

        <div class="info-row mb-4">

            <span>

                <i class="bi bi-credit-card"></i>

                Payment

            </span>

            <span

                class="badge"

                :class="paymentClass"

            >

                {{ booking.payment_status }}

            </span>

        </div>

        <button

            class="btn btn-outline-success w-100 mb-2"

            @click="$emit('view', booking.trek_id)"

        >

            <i class="bi bi-eye"></i>

            View Details

        </button>

        <div class="d-grid gap-2 mt-auto">

            <button

                v-if="booking.payment_status==='pending' && booking.status!=='Cancelled'"

                class="btn btn-warning"

                @click="$emit('pay', booking.booking_id)"

            >

                <i class="bi bi-credit-card-fill"></i>

                Pay Now

            </button>

            <button

                v-if="booking.status==='Upcoming'"

                class="btn btn-danger"

                @click="$emit('cancel', booking.booking_id)"

            >

                <i class="bi bi-x-circle"></i>

                Cancel Booking

            </button>

            <button

                v-if="booking.status==='Completed' && !booking.has_review"

                class="btn btn-success"

                @click="$emit('review', booking)"

            >

                <i class="bi bi-star-fill"></i>

                Write Review

            </button>

            <button

                v-if="booking.status==='Completed' && booking.has_review"

                class="btn btn-success"

                @click="$emit('review', booking)"

            >

                <i class="bi bi-star-fill"></i>

                View / Edit Review 

            </button>

            <button

                v-if="booking.status==='Cancelled'"

                class="btn btn-primary"

                @click="$emit('bookAgain', booking.trek_id)"

            >

                <i class="bi bi-arrow-repeat"></i>

                Book Again

            </button>

        </div>

    </div>

</div>

</template>


<script>

export default{

    name:"BookingCard",

    props:{

        booking:{

            type:Object,

            required:true

        }

    },

    emits:[

        "view",

        "cancel",

        "pay",

        "review",

        "bookAgain"

    ],

    computed:{

        statusClass(){

            switch(this.booking.status){

                case "Upcoming":

                    return "bg-success";

                case "Ongoing":

                    return "bg-primary";

                case "Completed":

                    return "bg-secondary";

                case "Cancelled":

                    return "bg-danger";

                default:

                    return "bg-dark";

            }

        },

        paymentClass(){

            switch(this.booking.payment_status){

                case "paid":

                    return "bg-success";

                case "pending":

                    return "bg-warning text-dark";

                case "refunded":

                    return "bg-info text-dark";

                case "failed":

                    return "bg-danger";

                default:

                    return "bg-secondary";

            }

        }

    },

    methods:{

        getImage(){

            const difficulty = this.booking.difficulty?.toLowerCase();
            console.log(this.booking.difficulty);

            switch(difficulty){

                case "easy":

                    return "/image/treks/easy.jpg";

                case "medium":

                    return "/image/treks/medium.jpg";

                case "hard":

                    return "/image/treks/hard.jpg";

                default:

                    return "/image/treks/hard.jpg";

            }

        }

    }

}

</script>

<style scoped>

.booking-card{

    border:none;

    border-radius:8px;

    overflow:hidden;

    transition:all .3s ease;

    background:#fff;

}

.booking-card:hover{

    transform:translateY(-8px);

    box-shadow:0 15px 35px rgba(0,0,0,.12);

}

.card-img-top{

    height:220px;

    object-fit:cover;

    transition:transform .4s ease;

}

.booking-card:hover .card-img-top{

    transform:scale(1.05);

}

.card-body{

    padding:1.3rem;

}

h5{

    font-size:1.15rem;

    margin-bottom:.2rem;

}

.text-muted{

    font-size:.92rem;

}


hr{

    margin:.9rem 0;

    opacity:.15;

}

.info-row{

    display:flex;

    justify-content:space-between;

    align-items:center;

    padding:.45rem 0;

    font-size:.95rem;

    border-bottom:1px dashed #e9ecef;

}

.info-row:last-child{

    border-bottom:none;

}

.info-row span:first-child{

    color:#6c757d;

    font-weight:500;

}

.info-row strong{

    color:#198754;

    font-size:1rem;

}

.badge{

    font-size:.78rem;

    padding:.45rem .75rem;

    border-radius:50px;

    font-weight:600;

    letter-spacing:.3px;

}

.btn{

    border-radius:12px;

    font-weight:600;

    transition:all .25s ease;

}

.btn:hover{

    transform:translateY(-2px);

}

.bi{

    margin-right:5px;

}

</style>