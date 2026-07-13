<template>

<div

    class="offcanvas offcanvas-end"

    tabindex="-1"

    ref="reviewCanvas"

>

    <!-- Header -->

    <div class="offcanvas-header">

        <div>

            <h4 class="mb-1">

                ⭐ Review Trek

            </h4>

            <small class="text-muted">

                Share your trekking experience

            </small>

        </div>

        <button

            class="btn-close"

            @click="closePanel"

        ></button>

    </div>

    <div class="offcanvas-body">

        <!-- Trek Information -->

        <div class="text-center mb-4">

            <h4 class="fw-bold">

                {{ booking?.trek_name }}

            </h4>

            <p class="text-muted">

                <i class="bi bi-geo-alt-fill"></i>

                {{ booking?.location }}

            </p>

        </div>

        <hr>

        <!-- Rating -->

        <div class="mb-4">

            <label class="form-label fw-semibold">

                How was your experience?

            </label>

            <div class="stars">

                <i

                    v-for="star in 5"

                    :key="star"

                    class="bi"

                    :class="

                        star <= hoverRating || star <= form.rating

                        ? 'bi-star-fill'

                        : 'bi-star'

                    "

                    @mouseenter="hoverRating = star"

                    @mouseleave="hoverRating = 0"

                    @click="form.rating = star"

                ></i>

            </div>

            <small

                class="text-danger"

                v-if="showRatingError"

            >

                Please select a rating.

            </small>

        </div>

        <!-- Comment -->

        <div class="mb-4">

            <label class="form-label fw-semibold">

                Your Experience

            </label>

            <textarea

                class="form-control"

                rows="6"

                maxlength="500"

                v-model="form.comment"

                placeholder="Tell future trekkers about your journey..."

            ></textarea>

            <div

                class="text-end mt-1"

            >

                <small class="text-muted">

                    {{ form.comment.length }}/500

                </small>

            </div>

        </div>

        <!-- Buttons -->

        <div class="d-grid gap-2">

            <button

                class="btn btn-success"

                @click="saveReview"

                :disabled="saving"

            >

                <span v-if="saving">

                    Saving...

                </span>

                <span v-else>

                    {{ booking?.has_review ? "Update Review" : "Submit Review" }}

                </span>

            </button>

            <button

                class="btn btn-outline-secondary"

                @click="closePanel"

            >

                Cancel

            </button>

        </div>

    </div>

</div>

</template>

<script>

import * as bootstrap from "bootstrap";

import{

    submitReview,

    getReview,

    updateReview

} from "../../services/trekker";

export default{

    name:"ReviewModal",

    props:{

        booking:{

            type:Object,

            required:true

        }

    },

    emits:[

        "close",

        "refresh"

    ],

    data(){

        return{

            offcanvas:null,

            saving:false,

            hoverRating:0,

            showRatingError:false,

            form:{

                rating:0,

                comment:""

            }

        }

    },

    methods:{

        // ---------------- Load Existing Review ----------------

        async loadReview(){

            if(!this.booking.has_review){

                this.form.rating = 0;

                this.form.comment = "";

                return;

            }

            try{

                const response = await getReview(

                    this.booking.trek_id

                );

                if(response.data.review){

                    this.form.rating = response.data.review.rating;

                    this.form.comment = response.data.review.comment || "";

                }

            }

            catch(error){

                console.error(error);

            }

        },

        // ---------------- Submit / Update ----------------

        async saveReview(){

            if(this.form.rating===0){

                this.showRatingError=true;

                return;

            }

            this.showRatingError=false;

            this.saving=true;

            try{

                if(this.booking.has_review){

                    await updateReview(

                        this.booking.trek_id,

                        this.form

                    );

                }

                else{

                    await submitReview(

                        this.booking.booking_id,

                        this.form

                    );

                }

                alert(

                    "Review saved successfully."

                );

                this.offcanvas.hide();

                this.$emit("refresh");

            }

            catch(error){

                alert(

                    error.response?.data?.message ||

                    "Unable to save review."

                );

            }

            finally{

                this.saving=false;

            }

        },

        // ---------------- Close ----------------

        closePanel(){

            this.offcanvas.hide();

        }

    },

    async mounted(){

        this.offcanvas = new bootstrap.Offcanvas(

            this.$refs.reviewCanvas

        );

        await this.loadReview();

        this.offcanvas.show();

        this.$refs.reviewCanvas.addEventListener(

            "hidden.bs.offcanvas",

            ()=>{

                this.$emit("close");

            }

        );

    }

}

</script>

<style scoped>

/* ================= Offcanvas ================= */

.offcanvas{

    width:500px;

    border-top-left-radius:20px;

    border-bottom-left-radius:20px;

}

/* ================= Header ================= */

.offcanvas-header{

    border-bottom:1px solid #e9ecef;

    padding:1.2rem 1.5rem;

}

.offcanvas-header h4{

    font-weight:700;

    color:#198754;

}

/* ================= Body ================= */

.offcanvas-body{

    padding:1.5rem;

}

/* ================= Trek Information ================= */

.text-center h4{

    font-weight:700;

    margin-bottom:.4rem;

}

.text-center p{

    font-size:.95rem;

}

/* ================= Divider ================= */

hr{

    opacity:.15;

    margin:1.2rem 0;

}

/* ================= Form Labels ================= */

.form-label{

    font-weight:600;

    color:#343a40;

    margin-bottom:.8rem;

}

/* ================= Rating Stars ================= */

.stars{

    display:flex;

    justify-content:center;

    gap:12px;

    margin-top:12px;

    margin-bottom:8px;

}

.stars i{

    font-size:2.1rem;

    color:#d6d6d6;

    cursor:pointer;

    transition:all .25s ease;

}

.stars i.bi-star-fill{

    color:#ffc107;

}

.stars i:hover{

    transform:scale(1.25);

}

/* ================= Textarea ================= */

textarea{

    resize:none;

    border-radius:14px;

    padding:14px;

    transition:.3s;

}

textarea:focus{

    border-color:#198754;

    box-shadow:0 0 0 .18rem rgba(25,135,84,.18);

}

/* ================= Character Counter ================= */

.text-end small{

    font-size:.82rem;

}

/* ================= Buttons ================= */

.btn{

    border-radius:12px;

    font-weight:600;

    padding:10px;

    transition:all .25s ease;

}

.btn-success:hover{

    transform:translateY(-2px);

    box-shadow:0 8px 18px rgba(25,135,84,.25);

}

.btn-outline-secondary:hover{

    transform:translateY(-2px);

}

/* ================= Validation ================= */

.text-danger{

    display:block;

    margin-top:8px;

    font-size:.88rem;

}

/* ================= Mobile ================= */

@media(max-width:768px){

    .offcanvas{

        width:100%;

        border-radius:0;

    }

    .stars{

        gap:8px;

    }

    .stars i{

        font-size:1.8rem;

    }

}

</style>