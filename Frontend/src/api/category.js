import request from '@/utils/request'

// category api
export function getGroup(params) {
  console.log(params)
  return request({
    url: '/api/category/',
    method: 'get',
    params,
  })
}

export function getGroupDetail(id) {
  console.log(id)
  return request({
    url: '/api/category/' + id + '/',
    method: 'get',
  })
}
