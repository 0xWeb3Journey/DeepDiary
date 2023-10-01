import request from '@/utils/request'

// recontact api
export function getRecontact(params) {
  return request({
    url: '/api/recontact/',
    method: 'get',
    params,
  })
}

export function apiAddRelation(data) {
  console.log('apiAddRelation', data)

  return request({
    url: '/api/recontact/',
    method: 'post',
    // data,

    data: {
      re_from: 43,
      re_to: 1,
      label: 21,
    },

    // data: {
    //   data: [
    //     {
    //       re_from: 43,
    //       re_to: 1,
    //       label: 21,
    //     },
    //     {
    //       re_from: 42,
    //       re_to: 1,
    //       label: 21,
    //     },
    //   ],
    // },
  })
}
