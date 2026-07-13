import api from "./api";

export function getDashboardStatistics(){

    return api.get("/user/dashboard");

}

export function getTreks(){

    return api.get("/user/treks");

}

export function bookTrek(trekId){

    return api.post(

        `/user/treks/${trekId}/book`

    );

}


export function getMyBookings(){

    return api.get(

        "/user/bookings"

    );

}

export function cancelBooking(bookingId){

    return api.put(

        `/user/bookings/${bookingId}/cancel`

    );

}

export function payBooking(bookingId){

    return api.put(

        `/user/bookings/${bookingId}/pay`

    );

}

export function submitReview(bookingId, data){

    return api.post(

        `/user/bookings/${bookingId}/review`,

        data

    );

}

export function getReview(trekId){

    return api.get(

        `/user/reviews/${trekId}`

    );

}

export function updateReview(trekId, data){

    return api.put(

        `/user/reviews/${trekId}`,

        data

    );

}

