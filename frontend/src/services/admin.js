import api from "./api";

export function getDashboardStats() {
    return api.get("/admin/dashboard");
}

export function getStaffDetails(staffId){

    return api.get(

        `/admin/staff/${staffId}/details`

    );

}

export function updateStaffStatus(staffId, data){

    return api.put(

        `/admin/staff/${staffId}/status`,

        data

    );

}

// ---------------------- Get User Details ----------------------

export function getUserDetails(userId){

    return api.get(

        `/admin/user/${userId}/details`

    );

}


// ---------------------- Update User Status ----------------------

export function updateUserStatus(userId, data){

    return api.put(

        `/admin/user/${userId}/status`,

        data

    );

}

//---------------------- Get All Users ----------------------

export function getAllUsers(search=""){

    return api.get(

        "/admin/users", {
            params:{
                search
            }
        }

    );

}


//---------------------- Get Single User ----------------------

export function getUser(userId){

    return api.get(

        `/admin/user/${userId}`

    );

}

// ---------------------- Get All Bookings ----------------------

export function getAllBookings(search=""){

    return api.get(

        "/admin/bookings", {
            params:{
                search
            }
        }

    );

}


// ---------------------- Get Booking Details ----------------------

export function getBookingDetails(bookingId){

    return api.get(

        `/admin/booking/${bookingId}`

    );

}


// ---------------------- Update Booking ----------------------

export function updateBooking(bookingId,data){

    return api.put(

        `/admin/booking/${bookingId}`,

        data

    );

}

//-------------------------------------------user reports-----------------
export function getReports(){

    return api.get(

        "/admin/reports"

    );

}

// ---------------------- Export Users Report ----------------------

export function exportUsersReport(){

    return api.get(

        "/admin/reports/users",

        {

            responseType:"blob"

        }

    );

}

// ---------------------- Export Staff Report ----------------------

export function exportStaffReport(){

    return api.get(

        "/admin/reports/staff",

        {

            responseType:"blob"

        }

    );

}

// ---------------------- Export Booking Report ----------------------

export function exportBookingReport(){

    return api.get(

        "/admin/reports/bookings",

        {

            responseType:"blob"

        }

    );

}

// ---------------------- Export Trek Report ----------------------

export function exportTrekReport(){

    return api.get(

        "/admin/reports/treks",

        {

            responseType:"blob"

        }

    );

}

// ---------------------- Get Admin Profile ----------------------

export function getAdminProfile(){

    return api.get(

        "/admin/profile"

    );

}

// ---------------------- Update Admin Profile ----------------------

export function updateAdminProfile(data){

    return api.put(

        "/admin/profile",

        data

    );

}

// ---------------------- Change Admin Password ----------------------

export function changeAdminPassword(data){

    return api.put(

        "/admin/change-password",

        data

    );

}