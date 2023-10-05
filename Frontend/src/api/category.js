import request from '@/utils/request'

// category api
export function getCategory(params) {
  console.log(params)
  return request({
    url: '/api/category/',
    method: 'get',
    params,
  })
}

export function getCategoryDetail(id) {
  console.log(id)
  return request({
    url: '/api/category/' + id + '/',
    method: 'get',
  })
}
