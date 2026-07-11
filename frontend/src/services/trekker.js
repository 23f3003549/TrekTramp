import api from "./api";

export function getDashboardStatistics(){

    return api.get("/user/dashboard");

}

export function getTreks(){

    return api.get("/user/treks");

}

