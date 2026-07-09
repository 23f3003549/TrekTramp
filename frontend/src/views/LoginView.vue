<template>

  <div class="container-fluid bg-dark min-vh-100 d-flex justify-content-center align-items-center">

    <div class="card shadow p-4" style="width: 400px;">

      <!-- <div v-if="successmessage" class="alert alert-success">

        {{ successmessage }}

      </div> -->

      <h2 class="text-center mb-4">
        Login
      </h2>

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
        this.errorMessage = ""
        this.successmessage = "Login Successful"
        
        if (response.data.role === "admin") {

          this.$router.push("/admin")

        }

        else if (response.data.role === "staff") {

          this.$router.push("/staff")

        }

        else {

          this.$router.push("/user")

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