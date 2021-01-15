import { faUniversalAccess } from '@fortawesome/free-solid-svg-icons';

export default {
  // Disable server-side rendering (https://go.nuxtjs.dev/ssr-mode)
  mode: "universal",
  ssr: false,

  // Target (https://go.nuxtjs.dev/config-target)
  target: "static",

  // Global page headers (https://go.nuxtjs.dev/config-head)
  head: {
    title: "LanPlay Records",
    meta: [
      { hid: "twitter:card", name: "twitter:card", content: "summary" },
      { hid: "twitter:site", name: "twitter:site", content: "tkgling" },
      { hid: "og:type", property: "og:type", content: "website" },
      {
        hid: "og:title",
        property: "og:title",
        content: "LanPlay Records"
      },
      {
        hid: "og:url",
        property: "og:url",
        content: "https://salmonrun-records.netlify.app/"
      },
      {
        hid: "og:description",
        property: "og:description",
        content: "The records of Salmon Run on LanPlay"
      },
      {
        hid: "og:image",
        property: "og:image",
        content:
          "https://app.splatoon2.nintendo.net/images/bundled/3aa6fb4ec1534196ede450667c1183dc.png"
      },
      { hid: "og:site_name", name: "og:site_name", contents: "LanPlay Records" }
    ],
    link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }]
  },

  // Global CSS (https://go.nuxtjs.dev/config-css)
  css: ["vuesax/dist/vuesax.css"],

  // Plugins to run before rendering page (https://go.nuxtjs.dev/config-plugins)
  plugins: ["@/plugins/vuesax"],

  // Auto import components (https://go.nuxtjs.dev/config-components)
  components: true,

  // Modules for dev and build (recommended) (https://go.nuxtjs.dev/config-modules)
  buildModules: [],

  // Modules (https://go.nuxtjs.dev/config-modules)
  modules: [
    // https://go.nuxtjs.dev/axios
    "@nuxtjs/axios",
    // https://go.nuxtjs.dev/pwa
    "@nuxtjs/pwa",
    // https://go.nuxtjs.dev/content
    "@nuxt/content",
    "nuxt-fontawesome",
    "nuxt-i18n"
  ],

  // Axios module configuration (https://go.nuxtjs.dev/config-axios)
  axios: {},

  // Content module configuration (https://go.nuxtjs.dev/config-content)
  content: {},

  i18n: {
    locales: ["ja", "en"],
    defaultLocale: "ja",
    // Doc: https://kazupon.github.io/vue-i18n/api/#properties
    vueI18n: {
      fallbackLocale: "en",
      // silentTranslationWarn: true,
      silentFallbackWarn: true,
      messages: {
        ja: require("./locales/ja.json"),
        en: require("./locales/en.json")
      }
    }
  },
  // Build Configuration (https://go.nuxtjs.dev/config-build)
  build: {},
  fontawesome: {
    imports: [
      {
        set: "@fortawesome/free-solid-svg-icons",
        icons: ["fas"]
      }
    ]
  }
};
