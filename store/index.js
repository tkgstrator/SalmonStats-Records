export const state = () => ({
    locales: ['en', 'ja'],
    locale: 'ja'
})

export const mutations = {
    SET_LANG(state, locale) {
        if (state.locales.includes(locale)) {
            state.locale = locale
        }
    }
}