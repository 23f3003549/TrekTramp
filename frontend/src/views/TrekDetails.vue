<template>
    <div class="card shadow-sm mt-4">
    
        <div class="card-header">
    
            <h5>Actions</h5>
    
        </div>
    
        <div class="card-body">
    
            <div v-if="role==='admin'">
    
                <button class="btn btn-success">
                    Assign Staff
                </button>
    
            </div>
    
            <div v-else-if="role==='staff'">
    
                <button class="btn btn-primary">
                    Start Trek
                </button>
    
                <button class="btn btn-success ms-2">
                    Complete Trek
                </button>
    
                <button class="btn btn-danger ms-2">
                    Cancel Trek
                </button>
    
            </div>
    
            <div v-else>
    
                <button class="btn btn-success">
                    Book Trek
                </button>
    
            </div>
    
        </div>

    </div>
</template>