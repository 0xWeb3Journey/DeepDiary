const state = {
  imgs: {
    title: 'Img List',
    loading: false,
    checkedId: -1,
    checkedIndex: -1,
    totalCnt: 0,
    links: null,
    curCnt: 0,
    data: [],
    queryForm: {
      page: 1,
      search: '',
      id: '',
      fc_nums: -1, //-1 ,means all, 6 means the fc_nums > 6
      fc_name: '',
      c_img: '',
      c_fore: '',
      c_back: '',

      address__is_located: '',
      address__city: '',
      address__longitude__range: '',
      address__latitude__range: '',
      user__username: '',
    },
  },
}

const getters = {
  imgs: (state) => state.imgs,
}

const mutations = {
  setImgQuery(state, newVal) {
    state.imgs = newVal
  },
}

const actions = {
  setImgQuery({ commit }, newVal) {
    commit('setImgQuery', newVal)
  },
}

export default {
  state,
  getters,
  mutations,
  actions,
}
