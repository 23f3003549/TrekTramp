<template>

  <div class="container-fluid bg-dark min-vh-100 d-flex justify-content-center align-items-center">

    <div class="card shadow p-4" style="width: 400px;">

      <div class="d-flex justify-content-between align-items-center mb-4">

          <h2 class="fw-bold mb-0" style="color: black;">
              Login
          </h2>
      
          <RouterLink
              to="/"
              class="btn btn-outline-dark btn-sm"
          >
              Home
          </RouterLink>

      </div>

      <div class="mb-3">

        <label class="form-label">
          Email
        </label>

        <input
          type="email"
          class="form-control"
          placeholder="Enter Email"
          v-model="email"
        />

      </div>

      <div class="mb-3">

        <label class="form-label">
          Password
        </label>

        <input
          type="password"
          class="form-control"
          placeholder="Enter Password"
          v-model="password"
        />

      </div>

      <div
        v-if="errorMessage"
        class="alert alert-danger"
      >
        {{ errorMessage }}
      </div>
      <div
        v-if="successmessage"
        class="alert alert-success"
      >
        {{ successmessage }}
      </div>

      <button
        class="btn btn-dark w-100"
        @click="loginUser"
      >
        Login
      </button>
      <div class="text-center mt-4">

    <small class="text-muted">
        New to TrekTramp?
    </small>

    <br>

    <RouterLink
        to="/register"
        class="text-decoration-none fw-semibold"
    >
        Register Here
    </RouterLink>

</div>

    </div>

  </div>

</template>

<script>

import axios from "axios"

export default {

  name: "LoginView",

  data() {

    return {

      email: "",
      password: "",
      errorMessage: "",
      successmessage:""

    }

  },

  methods: {

    async loginUser() {

      try {

        const response = await axios.post(

          "http://127.0.0.1:5000/api/auth/login",

          {
            email: this.email,
            password: this.password
          }

        )

        console.log(response.data)

        localStorage.setItem(
          "access_token",
          response.data.access_token
        )

        localStorage.setItem(
          "refresh_token",
          response.data.refresh_token
        )

        localStorage.setItem(
          "role",
          response.data.role
        )
        localStorage.setItem("name", response.data.name);
        this.errorMessage = ""
        this.successmessage = "Login Successful"
        
        if (response.data.role === "admin") {

          this.$router.push("/admin")

        }

        else if (response.data.role === "staff") {
          if(response.data.must_change_password){
             this.$router.push("/staff/complete-profile");

          }
          else{
            this.$router.push("/staff/dashboard");

          }

        }

        else {

          this.$router.push("/trekker/dashboard")

        }

      }

      catch(error) {

        console.log(error)

        if (error.response){
          this.errorMessage = error.response.data.message
        }
        else {
          this.errorMessage = "Unable to connect to server."
        }

      }

    }

  }

}

</script>

<style scoped>
.card{
    border-radius:8px;
}

.form-control{
    border-radius:10px;
}

.btn{
    border-radius:10px;
}

</style>
