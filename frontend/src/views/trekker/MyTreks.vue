<template>

<TrekkerLayout

    title="My Treks"

    placeholder="Search your treks by name/location..."

    @search="searchBookings"

>

    <div class="d-flex flex-wrap gap-2 mb-4">

        <button

            class="btn"

            :class="selectedFilter==='All'
                ? 'btn-success'
                : 'btn-outline-success'"

            @click="selectedFilter='All'"

        >

            All ({{ summary.all }})

        </button>

        <button

            class="btn"

            :class="selectedFilter==='Upcoming'
                ? 'btn-success'
                : 'btn-outline-success'"

            @click="selectedFilter='Upcoming'"

        >

            Upcoming ({{ summary.upcoming }})

        </button>

        <button

            class="btn"

            :class="selectedFilter==='Ongoing'
                ? 'btn-success'
                : 'btn-outline-success'"

            @click="selectedFilter='Ongoing'"

        >

            Ongoing ({{ summary.ongoing }})

        </button>

        <button

            class="btn"

            :class="selectedFilter==='Completed'
                ? 'btn-success'
                : 'btn-outline-success'"

            @click="selectedFilter='Completed'"

        >

            Completed ({{ summary.completed }})

        </button>

        <button

            class="btn"

            :class="selectedFilter==='Cancelled'
                ? 'btn-success'
                : 'btn-outline-success'"

            @click="selectedFilter='Cancelled'"

        >

            Cancelled ({{ summary.cancelled }})

        </button>

        <button
        class="btn btn-outline-success export-btn"
        @click="exportBookingHistory"
    >
        <i class="bi bi-download me-2"></i>
        Export CSV
    </button>

    </div>

    <div class="booking-header">

    <h4 class="page-title">
        My Trek Bookings
    </h4>

    <div class="header-actions">

        <span class="booking-count">

            Showing {{ filteredBookings.length }} Trek(s)

        </span>


    </div>

</div>

    <div

        v-if="filteredBookings.length"

        class="row g-4"

    >

        <div

            class="col-lg-4 col-md-6"

            v-for="booking in filteredBookings"

            :key="booking.booking_id"

        >

            <BookingCard

                :booking="booking"

                @view="viewDetails"

                @cancel="cancelBookingAction"

                @pay="payBookingAction"

                @review="reviewBooking"

                @bookAgain="bookAgain"

            />

        </div>

    </div>

    <div

    v-else

    class="text-center py-5"

>

    <i

        class="bi bi-search"

        style="font-size:70px;color:#adb5bd"

    ></i>

    <h3 class="mt-3 fw-bold">

        No Treks Found

    </h3>

    <p class="text-muted">

        <span v-if="selectedFilter==='All'">

            No trek matched your search.

        </span>

        <span v-else>

            No {{ selectedFilter.toLowerCase() }} trek matched your search.

        </span>

    </p>

    <button

        class="btn btn-success mt-2"

        @click="$router.push('/trekker/browse')"

    >

        Browse Treks

    </button>

</div>

    <TrekDetailsPanel

        v-if="selectedTrek"

        :trekId="selectedTrek"

        @close="selectedTrek = null"
        @refresh="refreshTreks"

    />

    <ReviewModal

        v-if="showReview"
    
        :booking="selectedBooking"
    
        @close="closeReview"
    
        @refresh="refreshBookings"

    />

</TrekkerLayout>

</template>

<script>

import TrekkerLayout from "../../layouts/TrekkerLayout.vue";
import BookingCard from "../../components/trekker/BookingCard.vue";
import { getMyBookings, cancelBooking, payBooking, submitReview, bookTrek, exportBookings } from "../../services/trekker.js"; 
import TrekDetailsPanel from "../../components/trek/TrekDetailsPanel.vue";
import ReviewModal from "../../components/trekker/ReviewModal.vue";


export default{

    name:"MyTreks",

    components:{

        TrekkerLayout,
        BookingCard,
        TrekDetailsPanel,
        ReviewModal

    },

    data(){

        return{

            bookings:[],

            searchText:"",

            selectedFilter:"All",

            summary:{

                all:0,

                upcoming:0,
            
                ongoing:0,
            
                completed:0,
            
                cancelled:0

            },

            selectedTrek:null,
            selectedBooking:null,

            showReview:false,
            loading:false

        }

    },

    computed:{

        filteredBookings(){

            return this.bookings.filter(

                booking=>
                   this.selectedFilter==="All" || booking.status===this.selectedFilter


            );

        }

    },

    methods:{

        async loadBookings(search=""){
            this.loading=true;

            try{

                const response = await getMyBookings(search);

                this.bookings = response.data.bookings;
                this.summary = response.data.summary;

            }

            catch(error){

                console.error(error);

            }
            finally{
                this.loading=false;
            }
        },
        async cancelBookingAction(bookingId){

            if(!confirm("Cancel this booking?")){
        
                return;
        
            }
        
            try{
        
                const response=await cancelBooking(
        
                    bookingId
        
                );
        
                alert(
        
                    response.data.message
        
                );
        
                await this.loadBookings();
                window.dispatchEvent(
                    new CustomEvent("trek-updated")
                );
        
            }
        
            catch(error){
        
                alert(
        
                    error.response?.data?.message ||
        
                    "Unable to cancel booking."
        
                );
        
            }
        
        }, 
        
        async payBookingAction(bookingId){

            if(!confirm("Proceed with payment?")){
        
                return;
        
            }
        
            try{
        
                const response=await payBooking(
        
                    bookingId
        
                );
        
                alert(
        
                    response.data.message
        
                );
        
                await this.loadBookings();
        
            }
        
            catch(error){
        
                alert(
        
                    error.response?.data?.message ||
        
                    "Payment failed."
        
                );
        
            }

        },

        async bookAgain(trekId){

            try{
        
                const response=await bookTrek(
        
                    trekId
        
                );
        
                alert(
        
                    response.data.message
        
                );
        
                await this.loadBookings();
                window.dispatchEvent(
                    new CustomEvent("trek-updated")
                );
        
            }
        
            catch(error){
        
                alert(
        
                    error.response?.data?.message ||
        
                    "Unable to book."
        
                );
        
            }

        },

        reviewBooking(booking){

            this.selectedBooking = booking;

            this.showReview = true;

        },
        async searchBookings(keyword){
            await this.loadBookings(  keyword   );

        },
        viewDetails(trekId){

            this.selectedTrek = trekId;

        },

        async refreshBookings(){

            this.showReview = false;

            this.selectedBooking = null;

            await this.loadBookings();

        },

        closeReview(){

            this.showReview = false;

            this.selectedBooking = null;

        },

        async exportBookingHistory(){

            try{
        
                const response = await exportBookings();
        
                alert(
        
                    response.data.message
        
                );
        
            }
        
            catch(error){
        
                alert(
        
                    error.response?.data?.message ||
        
                    "Unable to export booking history."
        
                );
        
            }
        
        }

    },

    mounted(){

        this.loadBookings();

    }

}

</script>

<style scoped>

.booking-header{

    display:flex;

    justify-content:space-between;

    align-items:center;

    margin-bottom:28px;

    flex-wrap:wrap;

    gap:15px;

}

.page-title{

    font-weight:700;

    color:#212529;

    margin:0;

}

.header-actions{

    display:flex;

    align-items:center;

    gap:18px;

}

.booking-count{

    color:#6c757d;

    font-size:15px;

    font-weight:500;

}

.export-btn{

    border-radius:12px;

    padding:10px 18px;

    font-weight:600;

    transition:.3s;

}

.export-btn:hover{

    transform:translateY(-2px);

    box-shadow:0 8px 20px rgba(25,135,84,.18);

}

.btn{

    border-radius:12px;

    font-weight:600;

}

.text-center{

    animation:fadeIn .4s ease;

}

.text-center h3{

    font-weight:700;

}

.text-center p{

    font-size:15px;

}

@media(max-width:768px){

    .booking-header{

        flex-direction:column;

        align-items:flex-start;

    }

    .header-actions{

        width:100%;

        justify-content:space-between;

    }

}

@keyframes fadeIn{

    from{

        opacity:0;

        transform:translateY(10px);

    }

    to{

        opacity:1;

        transform:translateY(0);

    }

}

</style>