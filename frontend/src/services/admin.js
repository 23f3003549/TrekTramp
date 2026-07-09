import api from "./api";

export function getDashboardStats() {
    return api.get("/admin/dashboard");
}