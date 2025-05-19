import store from "@/state/store";

export default [
  {
    path: "/login",
    name: "login",
    component: () => import("../views/auth/login.vue"),
    meta: {
      title: "Iniciar Sesión",
      beforeResolve(routeTo, routeFrom, next) {
        if (store.getters["auth/loggedIn"]) {
          next({ name: "default" });
        } else {
          next();
        }
      },
    },
  },

  {
    path: "/register",
    name: "register",
    component: () => import("../views/auth/register.vue"),
    meta: {
      title: "Registro",
      beforeResolve(routeTo, routeFrom, next) {
        if (store.getters["auth/loggedIn"]) {
          next({ name: "default" });
        } else {
          next();
        }
      },
    },
  },

  {
    path: "/reset-password",
    name: "reset-password",
    component: () => import("../views/auth/change-password.vue"),
    meta: {
      title: "Cambiar contraseña",
      beforeResolve(routeTo, routeFrom, next) {
        if (store.getters["auth/loggedIn"]) {
          next({ name: "default" });
        } else {
          next();
        }
      },
    },
  },

  // -----  Users  ------
  {
    path: "/usuario",
    name: "usuario",
    meta: { title: "Usuario", authRequired: true },
    component: () => import("../views/account/starter.vue"),
  },

  // -----  Home  ------
  {
    path: "/",
    name: "default",
    meta: {
      title: "Inicio",
      authRequired: true,
    },
    component: () => import("../views/starter/HomeLayout.vue"),
  },

  // -----  Community  ------
  {
    path: "/community",
    name: "community",
    component: () => import("../views/community/starter.vue"),
    meta: { title: "Foros", authRequired: true },
  },


  // -----  Chat  ------
  {
    path: "/chat",
    name: "chat",
    meta: { title: "Chat", authRequired: true },
    component: () => import("../views/chat/starter.vue"),
    children: [
      // {
      //   path: "/mi-profile",
      //   name: "user.profile",
      //   component: () => import("../views/account/pages/mi-profile.vue")
      // },
      // {
      //   path: "/reset-password",
      //   name: "user.reset-password",
      //   component: () => import("../views/account/pages/reset-password.vue")
      // },
    ]
  },

];