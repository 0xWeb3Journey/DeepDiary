const state = {
  gallery: [],
}

const mutations = {
  setGallery(state, gallery) {
    if (gallery) {
      state.gallery = gallery
    } else {
      state.gallery = []
    }
  },
}

const actions = {
  setGallery({ commit }, gallery) {
    commit('setGallery', gallery)
  },
}

export default {
  state,
  mutations,
  actions,
}
