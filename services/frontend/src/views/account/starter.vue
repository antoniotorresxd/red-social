<template>
    <Layout>
        <div class="chat-wrapper d-lg-flex gap-1 mx-n4 mt-n4 p-1 border">
            <!-- Sidebar -->
            <div class="chat-leftsidebar border d-flex flex-column">
                <div class="px-4 pt-4 mb-4">
                    <div class="d-flex align-items-start">
                        <div class="flex-grow-1">
                            <h5 class="mb-4">Usuario</h5>
                        </div>
                    </div>
                </div>

                <!-- Lista de foros o grupos -->
                <simplebar class="chat-room-list flex-fill" data-simplebar>
                    <div class="text-center mb-5 mt-5">
                        <div class="bg-secondary  mx-auto mb-2" style="width: 100px; height: 100px;"></div>
                        <div class="fw-semibold">{{ user.name }}</div>
                    </div>

                    <div class="d-flex align-items-center gap-2 px-3 py-2" @click="showProfile"
                        style="cursor: pointer; max-width: 200px;">
                        <i class="ri-profile-line fs-5"></i>
                        <span>Mi Perfil</span>
                    </div>
                </simplebar>
            </div>

            <!-- Área de trabajo -->
            <div class="user-chat w-100 overflow-auto p-4">
                <div class="d-flex align-items-center mb-4 d-lg-none ">
                    <BLink href="javascript:void(0)" class="user-chat-remove fs-18 p-1 me-3" @click="closeContent">
                        <i class="ri-arrow-left-s-line align-bottom"></i>
                    </BLink>
                    <h5 class="mb-0">{{ title }}</h5>
                </div>

                <!-- Aquí montamos el componente dinámico -->
                <component v-if="currentComponent" :is="currentComponent" @password="onPasswordChange" />
            </div>
        </div>
    </Layout>
</template>

<script>
import simplebar from 'simplebar-vue'
import Layout from '@/layouts/main.vue'
import UserProfile from './profile.vue'

export default {
    name: 'ForumMenuOnly',
    components: {
        Layout,
        simplebar,
        UserProfile
    },
    data() {
        return {
            user: {
                name: localStorage.getItem("user_name")
            },
            currentComponent: null,
            title: ''
        }
    },
    methods: {
        showProfile() {
            this.title = ''
            this.currentComponent = 'UserProfile'

            if (window.innerWidth < 992) {
                document.querySelector('.user-chat')?.classList.add('user-chat-show')
            }
        },
        closeContent() {
            this.currentComponent = null
            document.querySelector('.user-chat')?.classList.remove('user-chat-show')
        },
        onPasswordChange() {
            alert('Aquí puedes mostrar un modal o vista de cambio de contraseña')
        }
    }
}
</script>


<style scoped>
.chat-leftsidebar .dropdown-menu {
    box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

.chat-wrapper {
    position: relative;
}

.user-chat {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: #fff;
    transform: translateX(100%);
    transition: transform .3s ease-in-out;
    z-index: 5;
}

.user-chat.user-chat-show {
    transform: translateX(0);
}

@media(min-width: 992px) {
    .user-chat {
        position: relative;
        transform: none !important;
    }
}
</style>
