<template>

    <MainLayout>

        <!-- Page Header -->

        <div class="d-flex justify-content-between align-items-center mb-4">

            <h2 class="fw-bold">

                Reports & Analytics

            </h2>

        </div>

        <!-- Loading -->

        <div
            v-if="loading"
            class="text-center py-5"
        >

            <div class="spinner-border text-success"></div>

        </div>

        <template v-else>

            <!-- ====================================== -->
            <!-- Dashboard Summary -->
            <!-- ====================================== -->

            <div class="row g-4 mb-4">

                <div class="col-xl col-lg-4 col-md-6">

                    <SummaryCard

                        title="Treks"

                        :value="dashboard.treks"

                        icon="bi-map-fill"

                        color="success"

                    />

                </div>

                <div class="col-xl col-lg-4 col-md-6">

                    <SummaryCard

                        title="Users"

                        :value="dashboard.users"

                        icon="bi-people-fill"

                        color="primary"

                    />

                </div>

                <div class="col-xl col-lg-4 col-md-6">

                    <SummaryCard

                        title="Staff"

                        :value="dashboard.staff"

                        icon="bi-person-workspace"

                        color="warning"

                    />

                </div>

                <div class="col-xl col-lg-4 col-md-6">

                    <SummaryCard

                        title="Bookings"

                        :value="dashboard.bookings"

                        icon="bi-journal-check"

                        color="info"

                    />

                </div>

                <div class="col-xl col-lg-4 col-md-6">

                    <SummaryCard

                        title="Revenue"

                        :value="'₹ ' + dashboard.revenue"

                        icon="bi-currency-rupee"

                        color="dark"

                    />

                </div>

            </div>

            <!-- ====================================== -->
            <!-- Pie Charts -->
            <!-- ====================================== -->

            <div class="row g-4 mb-4">

                <div class="col-lg-6">

                    <BookingPieChart

                        :statistics="bookingStatistics"

                    />

                </div>

                <div class="col-lg-6">

                    <PaymentPieChart

                        :statistics="paymentStatistics"

                    />

                </div>

            </div>

            <!-- ====================================== -->
            <!-- Popular Treks -->
            <!-- ====================================== -->

            <div class="mb-4">

                <PopularTreksChart

                    :treks="popularTreks"

                />

            </div>

            <!-- ====================================== -->
            <!-- Staff Performance -->
            <!-- ====================================== -->

            <div class="mb-4">

                <StaffCharts

                    :staffStatistics="staffStatistics"

                />

            </div>

            <!-- ====================================== -->
            <!-- Monthly Booking -->
            <!-- ====================================== -->

            <div class="mb-4">

                <MonthlyBookingChart

                    :monthlyBookings="monthlyBookings"

                />

            </div>

            <!-- ====================================== -->
            <!-- Export Reports -->
            <!-- ====================================== -->

            <div class="card shadow-sm">

                <div class="card-header bg-success text-white">

                    Export Reports

                </div>

                <div class="card-body">

                    <div class="row g-4">

                        <div class="col-md-6 col-lg-3">

                            <ExportCard

                                title="Users"

                                description="Download all registered users."

                                icon="bi-people-fill"

                                color="primary"

                                @download="downloadUsers"

                            />

                        </div>

                        <div class="col-md-6 col-lg-3">

                            <ExportCard

                                title="Staff"

                                description="Download all staff details."

                                icon="bi-person-workspace"

                                color="warning"

                                @download="downloadStaff"

                            />

                        </div>

                        <div class="col-md-6 col-lg-3">

                            <ExportCard

                                title="Treks"

                                description="Download trek report."

                                icon="bi-map-fill"

                                color="success"

                                @download="downloadTreks"

                            />

                        </div>

                        <div class="col-md-6 col-lg-3">

                            <ExportCard

                                title="Bookings"

                                description="Download booking report."

                                icon="bi-journal-check"

                                color="info"

                                @download="downloadBookings"

                            />

                        </div>

                    </div>

                </div>

            </div>

        </template>

    </MainLayout>

</template>

<script>

import MainLayout from "../layouts/MainLayout.vue";

import SummaryCard from "../components/reports/SummaryCard.vue";
import BookingPieChart from "../components/reports/BookingPieChart.vue";
import PaymentPieChart from "../components/reports/PaymentPieChart.vue";
import PopularTreksChart from "../components/reports/PopularTreksChart.vue";
import StaffCharts from "../components/reports/StaffCharts.vue";
import MonthlyBookingChart from "../components/reports/MonthlyBookingChart.vue";
import ExportCard from "../components/reports/ExportCard.vue";

import{

    getReports,

    exportUsersReport,

    exportStaffReport,

    exportBookingReport,

    exportTrekReport

}from "../services/admin";

export default{

    name:"Reports",

    components:{

        MainLayout,

        SummaryCard,

        BookingPieChart,

        PaymentPieChart,

        PopularTreksChart,

        StaffCharts,

        MonthlyBookingChart,

        ExportCard

    },

    data(){

        return{
    
            loading:true,
    
            dashboard:{
    
                treks:0,
    
                users:0,
    
                staff:0,
    
                bookings:0,
    
                revenue:0
    
            },
    
            bookingStatistics:{
    
                booked:0,
    
                completed:0,
    
                cancelled:0
    
            },
    
            paymentStatistics:{
    
                paid:0,
    
                pending:0,
    
                refunded:0
    
            },
    
            popularTreks:[],
    
            staffStatistics:[],
    
            monthlyBookings:[]
    
        }

    },

    methods:{

        //--------------------------------------------------

        async loadReports(){

            this.loading=true;

            try{

                const response = await getReports();
                console.log(response.data);

                this.dashboard =

                    response.data.dashboard;

                this.bookingStatistics =

                    response.data.booking_statistics;

                this.paymentStatistics =

                    response.data.payment_statistics;

                this.popularTreks =

                    response.data.popular_treks;

                this.staffStatistics =

                    response.data.staff_statistics;

                this.monthlyBookings =

                    response.data.monthly_bookings;

            }

            catch(error){

                console.error(error);

                alert(

                    error.response?.data?.message ||

                    "Unable to load reports."

                );

            }

            finally{

                this.loading=false;

            }

        },

        //--------------------------------------------------

        downloadFile(blob,filename){

            const url = window.URL.createObjectURL(

                blob

            );

            const link = document.createElement(

                "a"

            );

            link.href = url;

            link.download = filename;

            document.body.appendChild(

                link

            );

            link.click();

            document.body.removeChild(

                link

            );

            window.URL.revokeObjectURL(

                url

            );

        },

        //--------------------------------------------------

        async downloadUsers(){

            try{

                const response =

                    await exportUsersReport();

                this.downloadFile(

                    response.data,

                    "users_report.csv"

                );

            }

            catch(error){

                console.error(error);

                alert(

                    "Unable to download users report."

                );

            }

        },

        //--------------------------------------------------

        async downloadStaff(){

            try{

                const response =

                    await exportStaffReport();

                this.downloadFile(

                    response.data,

                    "staff_report.csv"

                );

            }

            catch(error){

                console.error(error);

                alert(

                    "Unable to download staff report."

                );

            }

        },

        //--------------------------------------------------

        async downloadTreks(){

            try{

                const response =

                    await exportTrekReport();

                this.downloadFile(

                    response.data,

                    "trek_report.csv"

                );

            }

            catch(error){

                console.error(error);

                alert(

                    "Unable to download trek report."

                );

            }

        },

        //--------------------------------------------------

        async downloadBookings(){

            try{

                const response =

                    await exportBookingReport();

                this.downloadFile(

                    response.data,

                    "booking_report.csv"

                );

            }

            catch(error){

                console.error(error);

                alert(

                    "Unable to download booking report."

                );

            }

        }

    },

    mounted(){

        this.loadReports();

    }

}

</script>

<style scoped>

h2{

    color:#198754;

    font-weight:700;

}

/* ---------------- Summary Cards ---------------- */

.row{

    margin-bottom:0;

}

/* ---------------- Main Cards ---------------- */

.card{

    border:none;

    border-radius:14px;

}

.card-header{

    font-weight:600;

    font-size:1rem;

}

/* ---------------- Export Section ---------------- */

.card-body{

    background:#f8f9fa;

}

/* ---------------- Loading ---------------- */

.spinner-border{

    width:3rem;

    height:3rem;

}

/* ---------------- Responsive ---------------- */

@media (max-width:991px){

    .mb-4{

        margin-bottom:1.5rem !important;

    }

}

@media (max-width:768px){

    h2{

        font-size:1.6rem;

    }

}

</style>